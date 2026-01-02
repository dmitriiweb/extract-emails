# Package Management with `uv`

These rules define strict guidelines for managing Python dependencies in this project using the `uv` dependency manager.

## Use `uv` exclusively
- All Python dependencies must be installed, synchronized, and locked using `uv`.  
- Never use `pip`, `pip-tools`, or `poetry` directly for dependency management.  

## Managing dependencies
```bash
# Add or upgrade dependencies
uv add <package>

# Remove dependencies
uv remove <package>

# Reinstall all dependencies from lock file
uv sync

# Reinstall all dependencies from lock file including optional/development extras
uv sync --all-extras
```

## Scripts
```bash
# Run script with proper dependencies
uv run script.py
```

You can edit inline metadata manually:
```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "torch",
#     "torchvision",
#     "opencv-python",
#     "numpy",
#     "matplotlib",
#     "Pillow",
#     "timm",
# ]
# ///

print("some python code")
```

Or use the `uv` CLI to manage script dependencies:
```bash
# Add or upgrade script dependencies
uv add package-name --script script.py

# Remove script dependencies
uv remove package-name --script script.py

# Reinstall all script dependencies from lock file
uv sync --script script.py
```
