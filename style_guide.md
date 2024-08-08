# style guide for bot 


- **Indentation**: 
  - Use 4 spaces per indentation level.

- **Line Length**: 
  - Limit lines to 79 characters.

- **Blank Lines**:
  - Use blank lines to separate top-level functions, classes, and method definitions.

- **Imports**:
  - Group imports into standard library, third-party, and local imports.
  - Separate groups with a blank line.
 
    ```python
    import os
    import sys

    from requests import get
    from flask import Flask

    from my_module
    import my_function

- **Naming Conventions**:
  - **Variables**: cabab_case which means to Use lowercase words separated by underscores (e.g., `variable_name`).
  - **Functions**: Use lowercase words separated by underscores (e.g., `function_name`).
    ```python
    def my_function():
        if True:
      x = 5  # This is an inline comment
      print("Hello, world!")
  - **Classes**: Use CapitalizedWords convention (e.g., `ClassName`).
    ```python
      class ClassName:
        pass

  - **Constants**: Use uppercase words separated by underscores (e.g., `CONSTANT_NAME`).
    ```python
      CONSTANT_NAME = "value"


- **Spaces**:
  - Avoid extra spaces in expressions and statements (e.g., `a = 1` not `a=1`).

- **Comments**:
  - **Block Comments**: Use block comments for explanations, properly indented.
  - **Inline Comments**: Use inline comments sparingly, separated by at least two spaces from the statement.
    ```python
    # This is a block comment
    # explaining the following code.
    def example_function():
      pass


- **Docstrings**:
  - Use triple quotes for docstrings to document modules, classes, and functions.
 
    ```python
    def example_function():
    """
    This function does nothing.
    """
    pass


- **Exceptions**:
  - Use `try` and `except` blocks to handle exceptions.
  - Avoid using bare `except`.
    ```python
    try:
      risky_operation()
    except SomeException as e:
      handle_exception(e)
