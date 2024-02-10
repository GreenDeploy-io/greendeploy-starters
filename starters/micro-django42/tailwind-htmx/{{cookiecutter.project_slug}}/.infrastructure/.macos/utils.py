import glob
import os
import shutil
from enum import Enum
from importlib.metadata import distribution

from packaging.version import parse as parse_version


class VERBOSE(Enum):
    NONE = 0
    BASIC = 1
    DETAILED = 2


class ANSI(Enum):
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97


def print_colored(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")


def print_fail(msg):
    print_colored(msg, ANSI.BRIGHT_RED.value)


def print_yellow_when_verbose_basic(msg, verbose_mode):
    if verbose_mode >= VERBOSE.BASIC.value:
        print_colored(msg, ANSI.BRIGHT_YELLOW.value)


def print_green_when_verbose_basic(msg, verbose_mode):
    if verbose_mode >= VERBOSE.BASIC.value:
        print_colored(msg, ANSI.BRIGHT_GREEN.value)


def print_blue_when_verbose_detailed(msg, verbose_mode):
    if verbose_mode == VERBOSE.DETAILED.value:
        print_colored(msg, ANSI.BRIGHT_BLUE.value)


def list_and_remove(pattern, description, is_file=True, exclude_list=None):
    items = glob.glob(pattern)

    # Exclude certain items if necessary
    if exclude_list:
        items = [item for item in items if item not in exclude_list]

    item_type = "files" if is_file else "folders"

    if not items:
        print_colored(f"No {description} found.", 93)  # Yellow text
        return

    print_colored(f"Found the following {description}:", 93)  # Yellow text
    for item in items:
        print_colored(f"- {item}", 93)  # Yellow text

    print_colored(f"Delete these {item_type}? [Y/n]: ", 91)  # Red text
    decision = input()

    if decision.lower() == "y" or decision == "":
        for item in items:
            if is_file:
                os.remove(item)
            else:
                shutil.rmtree(
                    item
                )  # os.rmdir will remove an empty directory; for non-empty directories, you'll need to use shutil.rmtree

        print_colored(f"Deleted all {description}.", 92)  # Green text
    else:
        print_colored(f"Aborted. No {item_type} were deleted.", 92)  # Green text


def check_installed_packages(required_packages: dict, verbose_mode=VERBOSE.BASIC.value):
    """
    required_packages = {
        "setuptools": "42.0.0",
        "wheel": None,
        "twine": None,
        "build": None,
        # Add other packages here
    }

    if not check_installed_packages(required_packages, verbose_mode=verbose_mode):
        return

    """
    all_installed = True

    if verbose_mode >= VERBOSE.BASIC.value:
        print_colored("Checking for required packages...", ANSI.BRIGHT_YELLOW.value)

    for package, min_version_str in required_packages.items():
        try:
            dist = distribution(package)
            installed_version = parse_version(dist.version)

            if min_version_str:
                min_version_parsed = parse_version(min_version_str)
                if installed_version < min_version_parsed:
                    print_colored(
                        f"{package} is installed but the version is too old. Minimum required is {min_version}",
                        ANSI.BRIGHT_RED.value,
                    )
                    all_installed = False
                    continue

            if verbose_mode == VERBOSE.DETAILED.value:
                print_colored(f"{package} is installed.", ANSI.BRIGHT_GREEN.value)
        except Exception:
            print_colored(
                f"{package} is not installed. Please install it first.",
                ANSI.BRIGHT_RED.value,
            )
            all_installed = False

    if all_installed and verbose_mode >= VERBOSE.BASIC.value:
        print_colored(
            "All required packages are installed",
            ANSI.BRIGHT_GREEN.value,
        )
    elif all_installed is False:
        print_colored(
            "We will not proceed until the required packages are installed",
            ANSI.BRIGHT_YELLOW.value,
        )

    return all_installed
