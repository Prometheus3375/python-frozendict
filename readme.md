# Development

## Workspace initialization

Repeat steps below for Python 3.9, 3.10 and 3.11.

1. Install [Python](https://www.python.org/downloads/).
2. Change current working directory in terminal to the root of this repository.
3. Initialize virtual environment at directory `.venv3.*` (replace `*` with Python minor version)
   and activate it according to the [tutorial](https://docs.python.org/3/library/venv.html).
4. Run `python -m pip install -U pip setuptools wheel`.
5. Run `pip install build mypy`.
6. Deactivate virtual environment.

When working in PyCharm, go to Setting > Editor > Natural Languages > Spelling and add file
`dictionary.dic` to the list of custom dictionaries.
