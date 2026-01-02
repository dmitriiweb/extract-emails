# Google-Style Docstring Rules

This module demonstrates documentation as specified by the Google Python Style Guide. Docstrings may extend over multiple lines. Sections are created with a section header and a colon followed by a block of indented text. Section breaks are created by resuming unindented text; a new section also implicitly creates a break.

**Examples**
```text
Examples can be given using either the `Example` or `Examples` sections. Sections support any reStructuredText formatting, including literal blocks::

    $ python example_google.py
```

**Attributes**
- Document module-level variables either in an `Attributes` section of the module docstring or inline after the variable. Choose one convention and stay consistent.

**Todo**
- List TODOs in a `Todo` section.  
- Use `sphinx.ext.todo` if building docs with Sphinx.  

**Reference snippet**
```python
\"\"\"Module demonstrating Google-style docstrings.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension
\"\"\"

module_level_variable1 = 12345

module_level_variable2 = 98765
\"\"\"int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
\"\"\"


def function_with_types_in_docstring(param1, param2):
    \"\"\"Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    \"\"\"


def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
    \"\"\"Example function with PEP 484 type annotations.

    Args:
        param1: The first parameter.
        param2: The second parameter.
    \"\"\"
```
