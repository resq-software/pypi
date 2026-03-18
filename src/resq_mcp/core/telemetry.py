# Copyright 2026 ResQ
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Telemetry subsystem for the ResQ MCP server.

Provides unified OpenTelemetry tracing, Prometheus-compatible metrics,
and structured logging with automatic PII redaction.  The module is
designed to degrade gracefully: when the OTel SDK packages are absent
it falls back to no-op providers so call-sites never need conditional
imports.

Quickstart (no-op / dev)::

    from resq_mcp.core.telemetry import setup_telemetry, trace, meter

    setup_telemetry()          # safe to call multiple times

    @trace("hce.validate_incident")
    async def validate_incident(val: IncidentValidation) -> str:
        ...

Production activation::

    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc

    export OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    export OTEL_SERVICE_NAME=resq-mcp

    # The module auto-detects the SDK and configures exporters.

Architecture notes:
    * Every MCP tool invocation gets a root span with ``mcp.tool.*``
      semantic attributes, matching the conventions in the ResQ Python
      tools library (``tool_execution:<name>``).
    * Span attributes are scrubbed through :func:`_sanitize_attrs`
      before being set — API keys, private keys, and location PII are
      never persisted to the trace backend.
    * Metrics are registered on a module-level :data:`meter` so
      downstream code can create counters / histograms without
      importing the OTel API directly.
    * ``W3C TraceContext`` propagation is wired by default so traces
      survive the MCP server → upstream ResQ service boundary.
"""

from __future__ import annotations

import asyncio
import functools
import logging
import re
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar, overload

from resq_mcp.core.config import settings

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

# ---------------------------------------------------------------------------
# Type variables
# ---------------------------------------------------------------------------

P = ParamSpec("P")
R = TypeVar("R")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("resq_mcp.telemetry")

# ---------------------------------------------------------------------------
# PII / secret patterns — compiled once at import time
# ---------------------------------------------------------------------------

_REDACT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)(api[_-]?key|token|secret|password|private[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"(?i)bearer\s+\S+"),
    # Coarse lat/lon — redact to 2-decimal precision (~1 km) in log
    # messages.  Full precision is kept in structured span attributes
    # behind the :func:`_sanitize_attrs` gate.
    # Matches comma-separated pair: "37.3417, -121.9751"
    re.compile(r"(-?\d{1,3}\.\d{3,})\s*,\s*(-?\d{1,3}\.\d{3,})"),
    # Matches labelled individual coordinate: lat=37.3417 or latitude: -121.975
    re.compile(r"(?i)(?:lat(?:itude)?|lon(?:gitude)?|lng)\s*[:=]\s*(-?\d{1,3}\.\d{3,})"),
)

_SENSITIVE_ATTR_KEYS: frozenset[str] = frozenset(
    {
        "api_key",
        "token",
        "secret",
        "password",
        "private_key",
        "authorization",
        "credential",
        "resq.api_key",
    }
)

# ---------------------------------------------------------------------------
# Lazy OTel imports — degrade to no-ops when SDK is absent
# ---------------------------------------------------------------------------

try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.context import attach, detach
    from opentelemetry.context import get_current as get_otel_context
    from opentelemetry.metrics import get_meter_provider, set_meter_provider
    from opentelemetry.propagate import set_global_textmap
    from opentelemetry.propagators.composite import CompositePropagator
    from opentelemetry.sdk.metrics import MeterProvider as SdkMeterProvider
    from opentelemetry.sdk.metrics.export import (
        ConsoleMetricExporter,
        PeriodicExportingMetricReader,
    )
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider as SdkTracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
    )
    from opentelemetry.trace import StatusCode
    from opentelemetry.trace.propagation import TraceContextTextMapPropagator

    _HAS_OTEL_SDK = True
except ImportError:
    _HAS_OTEL_SDK = False

    # Minimal shims so the rest of the module compiles without the SDK.
    class _NoOpStatusCode:  # type: ignore[no-redef]
        OK = "OK"
        ERROR = "ERROR"
        UNSET = "UNSET"

    StatusCode = _NoOpStatusCode  # type: ignore[assignment,misc]

try:
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )

    _HAS_OTLP = True
except ImportError:
    _HAS_OTLP = False

# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------

_initialized: bool = False

# These are set during :func:`setup_telemetry`.  Before that call they
# resolve to OTel no-op implementations, which is safe.
tracer: Any = None  # opentelemetry.trace.Tracer  (or no-op)
meter: Any = None  # opentelemetry.metrics.Meter  (or no-op)


# ---------------------------------------------------------------------------
# PII / secret sanitisation
# ---------------------------------------------------------------------------


def _sanitize_attrs(attrs: dict[str, Any]) -> dict[str, Any]:
    """Strip secrets and coarsen PII from span/metric attributes.

    Rules (aligned with AGENTS.md safety contract):
        * Keys matching :data:`_SENSITIVE_ATTR_KEYS` are replaced with
          ``[REDACTED]``.
        * Latitude / longitude floats are truncated to 2 decimal places
          (~1.1 km precision) — enough for operational dashboards,
          insufficient for individual tracking.
        * String values are scrubbed against :data:`_REDACT_PATTERNS`.
    """
    clean: dict[str, Any] = {}
    for key, value in attrs.items():
        key_lower = key.lower().replace(".", "_").replace("-", "_")

        # ---- secret keys ----
        if key_lower in _SENSITIVE_ATTR_KEYS or any(
            s in key_lower for s in ("key", "token", "secret", "password", "credential")
        ):
            clean[key] = "[REDACTED]"
            continue

        # ---- coarsen coordinates ----
        if key_lower in ("latitude", "longitude", "lat", "lon", "lng") and isinstance(
            value, float
        ):
            clean[key] = round(value, 2)
            continue

        # ---- scrub string values ----
        if isinstance(value, str):
            sanitized = value
            for pattern in _REDACT_PATTERNS:
                sanitized = pattern.sub("[REDACTED]", sanitized)
            clean[key] = sanitized
            continue

        clean[key] = value
    return clean


def _redact_log_message(msg: str) -> str:
    """Apply :data:`_REDACT_PATTERNS` to a free-form log string."""
    for pattern in _REDACT_PATTERNS:
        msg = pattern.sub("[REDACTED]", msg)
    return msg


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def _build_resource() -> Any:
    """Build an OTel Resource describing this service instance."""
    if not _HAS_OTEL_SDK:
        return None

    return Resource.create(
        {
            "service.name": settings.PROJECT_NAME,
            "service.version": settings.VERSION,
            "deployment.environment": "development" if settings.DEBUG else "production",
            "resq.safe_mode": str(settings.SAFE_MODE),
        }
    )


def setup_telemetry() -> None:
    """Initialize the OpenTelemetry tracing and metrics pipeline.

    Behaviour varies by environment:

    **SDK + OTLP exporter installed** (production):
        Configures ``BatchSpanProcessor`` → OTLP gRPC exporter and
        ``PeriodicExportingMetricReader`` → OTLP gRPC exporter.  W3C
        TraceContext propagation is enabled.

    **SDK installed, no OTLP** (staging / local):
        Falls back to ``ConsoleSpanExporter`` and
        ``ConsoleMetricExporter`` so traces are visible in stdout.

    **No SDK** (minimal / CI):
        No-op providers.  Zero overhead.  All decorators and context
        managers become pass-throughs.

    Safe to call multiple times; subsequent calls are no-ops.
    """
    global _initialized, tracer, meter

    if _initialized:
        return
    _initialized = True

    if _HAS_OTEL_SDK:
        resource = _build_resource()

        # -- Tracing -------------------------------------------------------
        provider = SdkTracerProvider(resource=resource)

        if _HAS_OTLP:
            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
            logger.info("Tracing → OTLP gRPC exporter")
        elif settings.DEBUG:
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
            logger.info("Tracing → console exporter (debug)")
        else:
            logger.info("Tracing → SDK loaded, no exporter configured")

        otel_trace.set_tracer_provider(provider)

        # -- Metrics -------------------------------------------------------
        if _HAS_OTLP:
            metric_reader = PeriodicExportingMetricReader(
                OTLPMetricExporter(),
                export_interval_millis=15_000,
            )
        elif settings.DEBUG:
            metric_reader = PeriodicExportingMetricReader(
                ConsoleMetricExporter(),
                export_interval_millis=30_000,
            )
        else:
            metric_reader = None

        if metric_reader is not None:
            meter_provider = SdkMeterProvider(
                resource=resource,
                metric_readers=[metric_reader],
            )
            set_meter_provider(meter_provider)

        # -- Propagation ---------------------------------------------------
        set_global_textmap(
            CompositePropagator([TraceContextTextMapPropagator()])
        )

        tracer = otel_trace.get_tracer("resq-mcp", settings.VERSION)
        meter = get_meter_provider().get_meter("resq-mcp", settings.VERSION)

        logger.info(
            "Telemetry initialized (sdk=true, otlp=%s, env=%s)",
            _HAS_OTLP,
            "development" if settings.DEBUG else "production",
        )
    else:
        # No-op path — import the API-only stubs.
        try:
            from opentelemetry import trace as _api_trace
            from opentelemetry.metrics import get_meter_provider as _get_mp

            tracer = _api_trace.get_tracer("resq-mcp", settings.VERSION)
            meter = _get_mp().get_meter("resq-mcp", settings.VERSION)
        except ImportError:
            tracer = _NoOpTracer()
            meter = _NoOpMeter()

        if settings.DEBUG:
            logger.info("Telemetry initialized (no-op mode, SDK not installed)")


# ---------------------------------------------------------------------------
# No-op fallbacks when even opentelemetry-api is missing
# ---------------------------------------------------------------------------


class _NoOpSpan:
    """Minimal span shim that satisfies the context-manager protocol."""

    def set_attribute(self, key: str, value: Any) -> None: ...
    def set_status(self, status: Any, description: str | None = None) -> None: ...
    def record_exception(self, exception: BaseException) -> None: ...
    def end(self) -> None: ...
    def __enter__(self) -> _NoOpSpan:
        return self
    def __exit__(self, *args: object) -> None: ...


class _NoOpTracer:
    """Tracer that yields :class:`_NoOpSpan` instances."""

    def start_as_current_span(
        self, name: str, **kwargs: Any
    ) -> _NoOpSpan:
        return _NoOpSpan()

    @contextmanager
    def start_span(self, name: str, **kwargs: Any) -> Generator[_NoOpSpan]:
        yield _NoOpSpan()


class _NoOpMeter:
    """Meter that returns dummy instruments."""

    def create_counter(self, name: str, **kw: Any) -> _NoOpCounter:
        return _NoOpCounter()

    def create_histogram(self, name: str, **kw: Any) -> _NoOpHistogram:
        return _NoOpHistogram()

    def create_up_down_counter(self, name: str, **kw: Any) -> _NoOpCounter:
        return _NoOpCounter()


class _NoOpCounter:
    def add(self, amount: int | float, attributes: dict[str, Any] | None = None) -> None: ...


class _NoOpHistogram:
    def record(self, amount: int | float, attributes: dict[str, Any] | None = None) -> None: ...


# ---------------------------------------------------------------------------
# Pre-built metrics (lazy-init after setup_telemetry)
# ---------------------------------------------------------------------------


class _Metrics:
    """Lazy container for application-level metrics instruments.

    Instruments are created on first access so they pick up the
    meter configured by :func:`setup_telemetry`.

    Usage::

        from resq_mcp.core.telemetry import metrics

        metrics.tool_invocations.add(1, {"tool": "validate_incident"})
        metrics.tool_duration.record(elapsed, {"tool": "validate_incident"})
    """

    _tool_invocations: Any = None
    _tool_errors: Any = None
    _tool_duration: Any = None
    _active_spans: Any = None

    @property
    def tool_invocations(self) -> Any:
        if self._tool_invocations is None:
            self._tool_invocations = meter.create_counter(
                "resq.mcp.tool.invocations",
                description="Total MCP tool invocations",
                unit="1",
            )
        return self._tool_invocations

    @property
    def tool_errors(self) -> Any:
        if self._tool_errors is None:
            self._tool_errors = meter.create_counter(
                "resq.mcp.tool.errors",
                description="Total MCP tool errors",
                unit="1",
            )
        return self._tool_errors

    @property
    def tool_duration(self) -> Any:
        if self._tool_duration is None:
            self._tool_duration = meter.create_histogram(
                "resq.mcp.tool.duration",
                description="MCP tool execution duration",
                unit="s",
            )
        return self._tool_duration

    @property
    def active_spans(self) -> Any:
        if self._active_spans is None:
            self._active_spans = meter.create_up_down_counter(
                "resq.mcp.spans.active",
                description="Currently active trace spans",
                unit="1",
            )
        return self._active_spans


metrics = _Metrics()


# ---------------------------------------------------------------------------
# Trace decorator — sync & async aware
# ---------------------------------------------------------------------------


@overload
def trace(func: Callable[P, R], /) -> Callable[P, R]: ...


@overload
def trace(
    name: str | None = ...,
    *,
    record_args: bool = ...,
    record_result: bool = ...,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def trace(
    _func_or_name: Callable[P, R] | str | None = None,
    /,
    *,
    record_args: bool = False,
    record_result: bool = False,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """Instrument a function with an OpenTelemetry span.

    Can be used as a bare decorator or with arguments::

        @trace
        async def fast_path(): ...

        @trace("hce.validate_incident", record_args=True)
        async def validate_incident(val): ...

    Args:
        _func_or_name: Either the function to wrap (bare ``@trace``) or
            an explicit span name string.
        record_args: If ``True``, function kwargs are added as sanitised
            span attributes.  Positional args are skipped to avoid
            leaking large Pydantic models.
        record_result: If ``True``, the string representation of the
            return value (truncated to 1 KiB) is stored as
            ``resq.result``.

    Returns:
        The decorated function with identical signature.  Async
        functions remain async.
    """
    # Bare @trace usage (no parentheses)
    if callable(_func_or_name):
        return _apply_trace(None, False, False, _func_or_name)

    # Called with arguments: @trace("name") or @trace(record_args=True)
    span_name = _func_or_name

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        return _apply_trace(span_name, record_args, record_result, func)

    return decorator


def _apply_trace(
    span_name: str | None,
    record_args: bool,
    record_result: bool,
    func: Callable[P, R],
) -> Callable[P, R]:
    """Wrap *func* with tracing, supporting both sync and async."""
    resolved_name = span_name or f"{func.__module__}.{func.__qualname__}"

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            span_ctx = tracer.start_as_current_span(resolved_name)
            span = span_ctx.__enter__()
            metrics.active_spans.add(1)
            start = time.monotonic()
            try:
                _set_entry_attrs(span, func, record_args, kwargs)
                result = await func(*args, **kwargs)  # type: ignore[misc]
                _set_exit_attrs(span, result, record_result)
                span.set_status(StatusCode.OK)
                return result  # type: ignore[return-value]
            except Exception as exc:
                span.set_status(StatusCode.ERROR, str(exc))
                span.record_exception(exc)
                metrics.tool_errors.add(
                    1, {"tool": resolved_name, "error.type": type(exc).__name__}
                )
                raise
            finally:
                elapsed = time.monotonic() - start
                metrics.tool_duration.record(elapsed, {"tool": resolved_name})
                metrics.tool_invocations.add(1, {"tool": resolved_name})
                metrics.active_spans.add(-1)
                span_ctx.__exit__(None, None, None)

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        span_ctx = tracer.start_as_current_span(resolved_name)
        span = span_ctx.__enter__()
        metrics.active_spans.add(1)
        start = time.monotonic()
        try:
            _set_entry_attrs(span, func, record_args, kwargs)
            result = func(*args, **kwargs)
            _set_exit_attrs(span, result, record_result)
            span.set_status(StatusCode.OK)
            return result
        except Exception as exc:
            span.set_status(StatusCode.ERROR, str(exc))
            span.record_exception(exc)
            metrics.tool_errors.add(
                1, {"tool": resolved_name, "error.type": type(exc).__name__}
            )
            raise
        finally:
            elapsed = time.monotonic() - start
            metrics.tool_duration.record(elapsed, {"tool": resolved_name})
            metrics.tool_invocations.add(1, {"tool": resolved_name})
            metrics.active_spans.add(-1)
            span_ctx.__exit__(None, None, None)

    return sync_wrapper  # type: ignore[return-value]


def _set_entry_attrs(
    span: Any,
    func: Callable[..., object],
    record_args: bool,
    kwargs: dict[str, Any],
) -> None:
    """Set standard span attributes on entry."""
    span.set_attribute("code.function", func.__qualname__)
    span.set_attribute("code.namespace", func.__module__)
    if record_args and kwargs:
        safe = _sanitize_attrs(
            {f"resq.arg.{k}": _truncate(v) for k, v in kwargs.items()}
        )
        for k, v in safe.items():
            span.set_attribute(k, v)


def _set_exit_attrs(span: Any, result: Any, record_result: bool) -> None:
    """Optionally record the return value on the span."""
    if record_result and result is not None:
        span.set_attribute("resq.result", _truncate(result))


def _truncate(value: Any, max_len: int = 1024) -> str:
    """Convert *value* to a string, truncating to *max_len* characters."""
    s = str(value)
    return s[:max_len] + "…" if len(s) > max_len else s


# ---------------------------------------------------------------------------
# Context-manager span for manual instrumentation
# ---------------------------------------------------------------------------


@contextmanager
def span(
    name: str,
    attributes: dict[str, Any] | None = None,
) -> Generator[Any]:
    """Open a child span with sanitised attributes.

    Use this for fine-grained instrumentation inside a traced function
    where the decorator granularity is too coarse::

        with span("hce.http_call", {"http.url": url}) as s:
            resp = await session.get(url)
            s.set_attribute("http.status_code", resp.status)
    """
    safe = _sanitize_attrs(attributes) if attributes else {}
    with tracer.start_as_current_span(name, attributes=safe) as s:
        yield s


# ---------------------------------------------------------------------------
# Structured logging helpers
# ---------------------------------------------------------------------------


def log_event(
    event: str,
    *,
    level: int = logging.INFO,
    **attrs: Any,
) -> None:
    """Emit a structured log line with PII scrubbing.

    Attaches the current trace/span IDs when available so log
    aggregators can correlate logs ↔ traces.

    Args:
        event: Short event identifier (e.g. ``"tool.invoked"``).
        level: Python logging level.
        **attrs: Arbitrary key-value pairs (sanitised before logging).
    """
    safe = _sanitize_attrs(attrs)
    trace_ctx = _get_trace_context()
    extra = {**safe, **trace_ctx, "event": event}
    logger.log(level, _redact_log_message(event), extra=extra)


def _get_trace_context() -> dict[str, str]:
    """Extract trace_id and span_id from the current OTel context."""
    if not _HAS_OTEL_SDK:
        return {}
    try:
        current_span = otel_trace.get_current_span()
        ctx = current_span.get_span_context()
        if ctx and ctx.trace_id:
            return {
                "trace_id": format(ctx.trace_id, "032x"),
                "span_id": format(ctx.span_id, "016x"),
            }
    except Exception:
        pass
    return {}


# ---------------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------------


def shutdown_telemetry(timeout_ms: int = 5_000) -> None:
    """Flush pending spans/metrics and release exporter resources.

    Call this from the FastMCP server ``lifespan`` shutdown hook to
    avoid data loss on graceful termination.
    """
    if not _HAS_OTEL_SDK:
        return
    try:
        provider = otel_trace.get_tracer_provider()
        if hasattr(provider, "shutdown"):
            provider.shutdown()  # type: ignore[union-attr]
        mp = get_meter_provider()
        if hasattr(mp, "shutdown"):
            mp.shutdown(timeout_millis=timeout_ms)  # type: ignore[union-attr]
        logger.info("Telemetry shut down cleanly")
    except Exception:
        logger.warning("Telemetry shutdown encountered an error", exc_info=True)
