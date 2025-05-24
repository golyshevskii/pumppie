## Linter

[![Python Version](https://img.shields.io/badge/python-3.12-2241b3)](https://docs.python.org/3.12/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A linter based on `ruff` with `black` code styler that runs through `Makefile` commands to enforce code quality and style consistency.

### Quick start

1. Clone the repository.
2. From the root of the cloned repository run the `make lint.init` command in the terminal. _It will install the Poetry package manager and the necessary dependencies for using Ruff in the activated virtual development environment (venv)._

> WARNING. The next step will automatically lint and format Python files that are located at the path specified in the do-lint command in the Makefile (located in the root of the repository).

3. In the terminal enter the `make lint` command. It will run linting and formatting on those Python files that are specified in the [Makefile](../Makefile).