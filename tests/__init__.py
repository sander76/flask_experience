"""Adding this file to the tests folder makes it a package.

Without it imports will fail when trying to import from the package.
Adding this allows for running `pytest`

An alternative would be to run `python -m pytest` which adds the current
folder to `sys.path` which is used by python for package discovery.

For more info:

https://docs.pytest.org/en/6.2.x/pythonpath.html#import-modes
"""
