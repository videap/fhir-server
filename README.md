# FHIR
Test server for FHIR integration

# Requirements

Python 3.10+

# To run a local copy, for development, use virtual environment:

Install virtualenv with `pip3 install virtualenv` and:

```
virtualenv venv
source venv/bin/activate
```

This will create a python virtual env and will guarantee that your python installation is running on an isolated directory.
This allows for you to install dependencies without impacting the global python installation.

To deactivate a virtualenv, run `deactivate`.

## Install dependencies:
To run a local environment, you will need (poetry)[https://python-poetry.org/] as package manager. This allows you to install a dependency from the local directory.
To install poetry and the dependencies, run:

```
# from a virtual environment
pip install poetry

#Set up a dev environment inside the virtualenv and install all dependencies
poetry install

#Optionally install only dev dependencies
poetry install --only dev
```

# Tests
Make sure you have all dependencies installed and that you ran "poetry install"
```
poetry run pytest

# or from the virtual env
pytest
```

# Check Types
Make sure you have all dependencies installed and that you ran "poetry install"
```
poetry run pyright

# or from the virtual env
pyright
```

# Check Test Coverage
Make sure you have all dependencies installed and that you ran "poetry install"
```
poetry run coverage

# or from the virtual env
coverage
```

if you just need to refresh an "existing" coverage report, or if you will run coverage in CI environment, run:

```
poetry run coverage_ci

# or from the virtual env
coverage_ci
```

## Docstrings:
All functions should have docstrings

## Unit Tests:
All functions need unit tests

# Good Practices:

## Test Driven Development:
Before creating a function, create the unit test. Validate the behavior of the function.

## Side-effects are the last
When creating a function, the first thing that should be executed is validation of inputs, then logic, such as data manipulation, variables creation.
The last thing is the side-effect, or the stuff that produces consequences. The side effect can be mocked in unit tests, but the logic must be entirely tested.

# Architecture

Hexagonal Architecture has 3 main elements:

- Connectors (or Ports): Interface for external communication and has no business rules. Dependency injections are suggested for decoupling. These alements are mocked/emulated for unit/integration tests but they are used on E2E tests.

- Adapters: Do not have business rules, but consume services from the core. It also communicate with Connectors and use Dependency injection. It executes data validations, specific data transformation and can should not reuse other adaptors, as they are isolated from each other. These elements can be mocked for unit tests but must be used for integration/contracts tests.

- Core: Only business logic, and has all data required coming as inputs. Inputs and outputs are primitives. It should only have pure functions and should be only accessed by adapters. Extensively tested by unit tests.