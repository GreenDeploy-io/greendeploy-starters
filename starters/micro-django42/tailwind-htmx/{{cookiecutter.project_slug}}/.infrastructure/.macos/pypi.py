import argparse
import configparser
import os
import subprocess

# Your utility functions
from utils import (
    ANSI,
    VERBOSE,
    check_installed_packages,
    print_blue_when_verbose_detailed,
    print_colored,
    print_fail,
    print_green_when_verbose_basic,
    print_yellow_when_verbose_basic,
)


def check_pypirc_exists():
    pypirc_path = os.path.expanduser("~/.pypirc")
    if not os.path.exists(pypirc_path):
        print_colored(
            "The ~/.pypirc file does not exist.",
            ANSI.BRIGHT_RED.value,
        )
        return False
    return True


def check_pypi_credentials(verbose_mode=VERBOSE.BASIC.value):
    if verbose_mode >= VERBOSE.BASIC.value:
        print_colored(
            "Checking for required pypi credentials...", ANSI.BRIGHT_YELLOW.value
        )

    if not check_pypirc_exists():
        return False

    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.pypirc"))

    try:
        username = config.get("pypi", "username")
        password = config.get("pypi", "password")
    except configparser.NoSectionError:
        print_colored("No [pypi] section found in ~/.pypirc", 91)
        return False

    if username != "__token__":
        print_colored("username in [pypi] should be '__token__'", 91)
        return False

    if not password:
        print_colored("password in [pypi] is missing", 91)
        return False

    if verbose_mode >= VERBOSE.BASIC.value:
        print_colored(
            "Credentials under [pypi] in $HOME/.pypirc are present.",
            ANSI.BRIGHT_GREEN.value,
        )

    return True


def run_main(args):
    # Your main functionality for PyPI handling here
    print_colored("Running PyPI command", ANSI.BRIGHT_YELLOW.value)


def build_package(verbose_mode):
    print_yellow_when_verbose_basic(
        "Building a new version of the package", verbose_mode
    )

    # RATIONALE: python -m build is the recommended way to build a package
    # https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives
    # PRE-REQUISITES:
    #  - setuptools >= 42.0.0, wheel, build
    #  - pyproject.toml need to set [build-system].build-backend = "setuptools.build_meta"
    #  - pyproject.toml need to set [build-system].requires = ["setuptools >= 42", "wheel"]
    #  - setup.cfg need to set package metadata, dependencies, and other settings
    cmd_setup = [
        "python",
        "-m",
        "build",
    ]

    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_setup)}", verbose_mode
    )
    try:
        subprocess.run(cmd_setup, check=True)
        print_green_when_verbose_basic("Package built!", verbose_mode)
    except subprocess.CalledProcessError as e:
        print_fail(f"Failed to build package: {e}")


def check_package_with_twine(verbose_mode):
    print_yellow_when_verbose_basic("Checking package with twine", verbose_mode)

    cmd_check = ["twine", "check", "dist/*"]

    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_check)}", verbose_mode
    )

    try:
        subprocess.run(cmd_check, check=True)
        print_green_when_verbose_basic("Package check passed!", verbose_mode)
    except subprocess.CalledProcessError:
        print_fail("Fix the errors from above then re-run the build command!!")
        print_fail(
            "build command: `python .infrastructure/pypi.py --verbose_mode 2 build`"
        )


def remove_dev_versions(verbose_mode):
    print_yellow_when_verbose_basic(
        "Removing all dev versions from dist/ folder", verbose_mode
    )

    # Prepare the find command to search and remove '*dev*' files in dist/
    cmd_remove = r"find dist/* -name '*dev*' -exec rm {} \;"
    print_blue_when_verbose_detailed(f"Executing command: {cmd_remove}", verbose_mode)

    try:
        subprocess.run(
            cmd_remove,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print_green_when_verbose_basic(
            "Successfully removed all dev versions from dist/", verbose_mode
        )
    except subprocess.CalledProcessError as e:
        print_fail(f"Failed to remove dev versions: {e}")


def create_pypirc(verbose_mode):
    print_yellow_when_verbose_basic("Creating .pypirc file", verbose_mode)

    pypirc_content = """[testpypi]
  username = __token__
  password = testpypi-token-here
  repository = https://test.pypi.org/legacy/

[pypi]
  username = __token__
  password = pypi-token-here
"""

    home_directory = os.path.expanduser("~")
    pypirc_path = os.path.join(home_directory, ".pypirc")

    print_blue_when_verbose_detailed(
        f"Creating .pypirc file at: {pypirc_path}", verbose_mode
    )

    try:
        with open(pypirc_path, "w") as f:
            f.write(pypirc_content)
        print_green_when_verbose_basic(".pypirc file created!", verbose_mode)
    except Exception as e:
        print_fail(f"Failed to create .pypirc file: {e}")


def upload_package(verbose_mode, repository=None):
    print_yellow_when_verbose_basic("Uploading package to repository", verbose_mode)

    # Build the command
    cmd_upload = ["twine", "upload", "--skip-existing"]

    # Specify the repository if provided
    if repository:
        cmd_upload.extend(["--repository", repository])

    cmd_upload.append("dist/*")

    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_upload)}", verbose_mode
    )

    try:
        subprocess.run(cmd_upload, check=True)
        print_green_when_verbose_basic("Package uploaded successfully!", verbose_mode)
    except subprocess.CalledProcessError as e:
        print_fail(f"Failed to upload package: {e}")


# typical command
# def some_command(verbose_mode, **kwargs):
#     print_yellow_when_verbose_basic("Doing this thing", verbose_mode)

#     some_cmd = ["the", "command", "to", "run"]

#     print_blue_when_verbose_detailed(
#         f"Executing command: {' '.join(some_cmd)}", verbose_mode
#     )

#     try:
#         subprocess.run(some_cmd, check=True)
#         print_green_when_verbose_basic("Success message! Command done!", verbose_mode)
#     except subprocess.CalledProcessError:
#         print_fail(f"Failed to do this command: {e}")


def get_pypirc_sections():
    pypirc_path = os.path.expanduser("~/.pypirc")
    if not os.path.exists(pypirc_path):
        return []

    config = configparser.ConfigParser()
    config.read(pypirc_path)
    return config.sections()


def parse_args():
    # Fetch available sections from ~/.pypirc
    available_sections = get_pypirc_sections()

    parser = argparse.ArgumentParser(
        description="1. Turn on your preferred virtual environment for developing this package.\n"
        "2. Run this script at the project root (Important!).\n"
        "3. Execute package-related tasks.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--verbose_mode",
        type=int,
        choices=[0, 1, 2],
        default=1,
        help="Set the verbosity level. 0: None, 1: Basic, 2: Detailed",
    )

    # Add a subparser to handle the different commands
    subparsers = parser.add_subparsers(dest="command")

    # Add a parser for the 'run' command
    run_parser = subparsers.add_parser("run", help="Run pypi upload")

    # Add argument for specifying the repository section from ~/.pypirc
    if available_sections:
        run_parser.add_argument(
            "repository",
            choices=available_sections,
            help="Specify the repository section to use from ~/.pypirc",
        )

    # Add a parser for the 'build' command
    subparsers.add_parser("build", help="Build package")

    # Add a parser for the 'check' command
    subparsers.add_parser("check", help="Check package with twine")

    # Add a parser for the 'remove_dev_versions' command
    subparsers.add_parser(
        "remove_dev_versions", help="Remove all dev versions from dist/ folder"
    )

    # Add a parser for the 'create_pypirc' command
    subparsers.add_parser("create_pypirc", help="Create .pypirc file")

    # Add a parser for the 'upload' command
    upload_parser = subparsers.add_parser("upload", help="Upload package")

    if available_sections:
        upload_parser.add_argument(
            "--repository",
            choices=available_sections,
            default="",
            help="Specify the repository section to use from ~/.pypirc",
        )

    # Add a parser for the 'some_cmd' command
    # subparsers.add_parser("some_cmd", help="Do something")

    return parser.parse_args()


def main(args):
    verbose_mode = args.verbose_mode

    required_packages = {
        "setuptools": "42.0.0",
        "wheel": None,
        "twine": None,
        "build": None,
        "packaging": None
        # Add other packages here
    }
    if not check_installed_packages(
        required_packages,
        verbose_mode=verbose_mode,
    ):
        return
    if not check_pypi_credentials(verbose_mode=verbose_mode):
        return

    if args.command == "run":
        run_main(args)
    elif args.command == "build":
        build_package(verbose_mode)
    elif args.command == "check":
        check_package_with_twine(verbose_mode)
    elif args.command == "remove_dev_versions":
        remove_dev_versions(verbose_mode)
    elif args.command == "create_pypirc":
        create_pypirc(verbose_mode)
    elif args.command == "upload":
        upload_package(verbose_mode, repository=args.repository)
    else:
        print_fail("Command not recognized")
    # Add more commands as needed


if __name__ == "__main__":
    args = parse_args()
    main(args)
