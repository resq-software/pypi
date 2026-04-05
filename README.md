# ResQ PyPI Packages

Python packages for the ResQ disaster response platform, published to [PyPI](https://pypi.org) under the [`resq-software`](https://pypi.org/org/resq-software/) organization.

## Packages

| Package | Description | PyPI |
|---------|-------------|------|
| [resq-mcp](packages/resq-mcp/) | FastMCP server for AI agent integration | [![PyPI](https://img.shields.io/pypi/v/resq-mcp)](https://pypi.org/project/resq-mcp/) |
| [resq-dsa](packages/resq-dsa/) | Zero-dependency data structures & algorithms | [![PyPI](https://img.shields.io/pypi/v/resq-dsa)](https://pypi.org/project/resq-dsa/) |

## Development

```bash
# Setup
./bootstrap.sh

# Work on a package
cd packages/resq-mcp && uv sync && uv run pytest
cd packages/resq-dsa && uv sync && uv run pytest
```

## License

[Apache-2.0](LICENSE)
