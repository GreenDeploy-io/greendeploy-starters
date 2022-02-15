"""{{ cookiecutter.project_slug }} is a test project for demoing how to have layered requirements
while using pip-tools and setup.py.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("demo-public-python-project")
except PackageNotFoundError:
    # when initially start a project, there will be no runtime
    __version__ = "0.0.0"


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
