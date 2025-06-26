# Code Rules

This is a project to extract emails or urls to linkedin accounts from web sites

### General Guidelines
- Use Python 3.10+ syntax.
- Follow PEP 8 coding standards.
- Include type hints for all function definitions.
- Add docstrings to all public classes and functions.
- Prefer `pathlib` over `os.path` for file system operations.
- Utilize f-strings for string formatting.
- Avoid using wildcard imports.
- Use `print(f"{var_name=}")` or `logger.debug(f"{var_name=}")` for debugging.
- Write idiomatic and readable code.
- Do not write comments for tests
- Do not write comments where you are describing what was changed
- Do not wtrite try/except blocks for large blocks of code, but only for specific lines where exceptions are expected.
- Do not use "from typing install List, Dict, Option", but use python 3.10+ syntax like `list`, `dict`, and `|`.
- Use "" (double quotes) for strings and '' (single quotes) for chars only

## Package management
- Use `uv add` to install python packages
- Use `uv run` to run the project or scripts
