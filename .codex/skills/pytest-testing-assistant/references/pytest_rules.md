# Pytest Testing Rules

## Structure
- Tests must be standalone functions; do **not** create test classes.  
- One test should cover one function/behavior. Keep arrange/act/assert visible.  
- Name tests descriptively: `test_<function>_<behavior>` (or similar behavior-focused names).  

## Writing tests
- Prefer one primary assertion; add minimal secondary checks only when they aid clarity.  
- Use parametrization for small input/output tables instead of loops inside tests.  
- Keep setup simple; use fixtures only when they clearly reduce repetition without hiding intent.  
- Avoid global state; clean up side effects inside the test or via fixtures/finalizers.  

## Running tests
- Run all tests with `pytest`.  
- Scope runs with `pytest path/to/test_file.py` or selectors like `pytest -k "keyword"` when iterating.  

## Example
```python
import pytest

def test_parse_user_returns_id_and_name():
    raw = {"id": 1, "name": "Ada"}
    user = parse_user(raw)

    assert user.id == 1
    assert user.name == "Ada"
```
