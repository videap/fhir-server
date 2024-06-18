import subprocess, webbrowser, os
import toml
from enum import Enum
from typing import Callable

def _get_app_name_from_pyproject(file_path='pyproject.toml'):
    try:
        with open(file_path, 'r') as file:
            pyproject_data = toml.load(file)

        # Extract the application name
        app_name = pyproject_data['tool']['poetry']['name']
        return app_name
    except FileNotFoundError:
        return "pyproject.toml file not found"
    except KeyError:
        return "Application name not found in pyproject.toml"

class Envs(Enum):
    local="local"
    dev="dev"
    prod="prod"

APP_NAME = _get_app_name_from_pyproject()

def before_start(func:Callable):
    try:
        getattr(Envs, os.environ["ENV"])
        return func
    except KeyError:
        raise EnvironmentError("Please, ensure that the ENV variable is set")
    except AttributeError:
        raise ValueError(f"Please, ensure that the ENV Variable is one of {list(Envs.__members__.keys())}")

@before_start
def start():
    """Start app
    """
    app_name = _get_app_name_from_pyproject()
    command = f"python -m uvicorn {APP_NAME}.main:app --host 0.0.0.0 --port 7001"
    subprocess.run(command.split())

def start_local():
    """Start app
    """
    app_name = _get_app_name_from_pyproject()
    command = f"python -m uvicorn {APP_NAME}.main:app --host 0.0.0.0 --port 7001"
    subprocess.run(command.split())

def pytest():
    """Run Unit Tests with pytest
    """
    command = "python -u -m pytest --show-capture=all"
    subprocess.run(command.split())

def coverage():
    """Run Unit Tests with pytest and open coverage report on browser
    """
    command = f"python -m pytest --cov={_get_app_name_from_pyproject()} --cov-report html --cov-report term --cov-report xml:coverage"
    subprocess.run(command.split())

    app_dir = os.path.dirname(os.path.abspath(__file__))

    url = f"file:///{app_dir}/htmlcov/index.html"
    webbrowser.open(url, new=2)  # open in new tab

def coverage_ci():
    """Run Unit Tests with pytest and generate reports for CI
    """
    command = f"python -m pytest --cov={_get_app_name_from_pyproject()} --cov-report html --cov-report term-missing --cov-report xml:{_get_app_name_from_pyproject()}/coverage.xml"
    subprocess.run(command.split())

def pyright():
    """Run Type Checks with pyright
    """
    command = f"python -u -m pyright --dependencies --warnings {_get_app_name_from_pyproject()}"
    subprocess.run(command.split())
