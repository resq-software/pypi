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

"""Extended tests for timeout module covering edge cases."""

from __future__ import annotations

import os
from unittest.mock import patch


class TestSafeFloat:
    def test_nan_returns_default(self) -> None:
        from resq_mcp.core.timeout import _safe_float

        with patch.dict(os.environ, {"TEST_VAR": "nan"}):
            assert _safe_float("TEST_VAR", "5.0") == 5.0

    def test_inf_returns_default(self) -> None:
        from resq_mcp.core.timeout import _safe_float

        with patch.dict(os.environ, {"TEST_VAR": "inf"}):
            assert _safe_float("TEST_VAR", "5.0") == 5.0


class TestGetMaxPollingAttempts:
    def test_invalid_env_returns_default(self) -> None:
        from resq_mcp.core.timeout import get_max_polling_attempts

        with patch.dict(os.environ, {"RESQ_MAX_POLLING_ATTEMPTS": "not_a_number"}):
            assert get_max_polling_attempts() == 30
