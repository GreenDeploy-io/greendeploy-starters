"""``{{ cookiecutter.project_slug }}.framework`` implements the logic for this project
"""
from pyfiglet import figlet_format
from {{cookiecutter.project_slug}} import __version__


def hello_world_logo():
    return figlet_format("Hello World", font="slant")

def main():  # pragma: no cover
    """Main entry point.
    """
    print(hello_world_logo())
    print(__version__)
    print("newer")
