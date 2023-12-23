import argparse
import glob
import os
import subprocess
import webbrowser
from datetime import datetime

# Your utility functions
from utils import (
    check_installed_packages,
    list_and_remove,
    print_blue_when_verbose_detailed,
    print_green_when_verbose_basic,
    print_yellow_when_verbose_basic,
)


def main(args):
    verbose_mode = args.verbose_mode

    required_packages = {
        # "package": "minimum version",
        # as e.g.
        # "setuptools": "42.0.0",
        "pytest": None,
        "coverage": None,
    }
    if not check_installed_packages(
        required_packages,
        verbose_mode=verbose_mode,
    ):
        return

    if args.command == "run":
        env_name = args.env_name
        pytest_args = args.pytest_args

        run_main(env_name, pytest_args, verbose_mode)

        if args.auto_open_coverage.lower() == "yes":
            open_latest_coverage_report()

    elif args.command == "open_latest_coverage":
        open_latest_coverage_report()

    elif args.command == "remove_htmlcov_folders":
        list_and_remove("htmlcov*", "HTML coverage folders", is_file=False)

    elif args.command == "remove_coverage_files":
        list_and_remove(".coverage*", "Coverage files", exclude_list=[".coveragerc"])


def run_main(env_name, pytest_args, verbose_mode):
    """
    how to run

    `python .infrastructure/pytest.py --verbose_mode 2 run -- py310-django42 -s `

    anything after -- is for run and not pytest.py itself
    """
    print_yellow_when_verbose_basic(
        "Setting COVERAGE_FILE as environment variable", verbose_mode
    )
    os.environ["COVERAGE_FILE"] = f".coverage.{env_name}"
    print_green_when_verbose_basic(
        f"COVERAGE_FILE is set to .coverage.{env_name}", verbose_mode
    )

    print_yellow_when_verbose_basic(
        "Running pytest with specified arguments", verbose_mode
    )
    cmd_pytest = [
        "python",
        "-W",
        "error::ResourceWarning",
        "-W",
        "error::DeprecationWarning",
        "-W",
        "error::PendingDeprecationWarning",
        "-m",
        "coverage",
        "run",
        "-m",
        "pytest",
        "tests/",
    ] + pytest_args
    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_pytest)}", verbose_mode
    )
    subprocess.run(cmd_pytest)

    print_yellow_when_verbose_basic("Combining coverage reports", verbose_mode)
    cmd_combine = ["coverage", "combine"]
    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_combine)}", verbose_mode
    )
    subprocess.run(cmd_combine)

    print_yellow_when_verbose_basic("Generating coverage report", verbose_mode)
    cmd_report = ["coverage", "report", "--show-missing"]
    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_report)}", verbose_mode
    )
    subprocess.run(cmd_report)

    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y%m%d")
    epoch_timestamp = int(current_datetime.timestamp())

    folder_name = f"htmlcov-{env_name}-{date_str}-{epoch_timestamp}"

    print_yellow_when_verbose_basic(
        f"Generating HTML coverage report in {folder_name}", verbose_mode
    )
    cmd_html = ["coverage", "html", "-d", folder_name]
    print_blue_when_verbose_detailed(
        f"Executing command: {' '.join(cmd_html)}", verbose_mode
    )
    subprocess.run(cmd_html)


def open_latest_coverage_report():
    coverage_folders = glob.glob("htmlcov*")
    if not coverage_folders:
        print("No coverage folders found.")
        return
    latest_folder = max(coverage_folders, key=os.path.getctime)
    print(f"Opening the latest coverage report in folder {latest_folder}")
    webbrowser.open(f"file://{os.getcwd()}/{latest_folder}/index.html")


def parse_args():
    parser = argparse.ArgumentParser(
        description="1. Turn on your preferred virtual environment for developing this package.\n"
        "2. Run this script at the project root (Important!).\n"
        "3. Watch as a new htmlcov folder is created.",
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
    run_parser = subparsers.add_parser("run", help="Run tests")
    run_parser.add_argument("env_name", help="Name of the environment")
    run_parser.add_argument(
        "pytest_args", nargs="*", help="Arguments to pass to pytest", default=[]
    )

    run_parser.add_argument(
        "--auto_open_coverage",
        default="no",
        choices=["yes", "no"],
        help="Automatically open the HTML coverage report in the default browser",
    )

    # Add a parser for the 'open_latest_coverage' command
    subparsers.add_parser(
        "open_latest_coverage", help="Open the latest HTML coverage report"
    )

    # Add a parser for the 'remove_htmlcov_folders' command
    subparsers.add_parser("remove_htmlcov_folders", help="Remove HTML coverage folders")

    # Add a parser for the 'remove_coverage_files' command
    subparsers.add_parser(
        "remove_coverage_files", help="Remove .coverage, .coverage.* files"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
