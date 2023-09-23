"""
NOTE:
    This is for use with cookiecutter.
    Derived from https://github.com/cookiecutter/cookiecutter-django/blob/df0b2cac3f957a13c206bbf344dd28aa17888efb/hooks/post_gen_project.py
TODO:
    Regen the SECRET KEY
GOAL:
    1. SECRET KEY
    2. random admin user

"""

import json
import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])

def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value

def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)

def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return

def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    local_django_envs_path = os.path.join(".envs", ".local", ".django")
    production_django_envs_path = os.path.join(".envs", ".production", ".django")
    local_postgres_envs_path = os.path.join(".envs", ".local", ".postgres")
    production_postgres_envs_path = os.path.join(".envs", ".production", ".postgres")

    set_django_secret_key(production_django_envs_path)
    # set_django_admin_url(production_django_envs_path)

    # set_postgres_user(local_postgres_envs_path, value=postgres_user)
    # set_postgres_password(
    #     local_postgres_envs_path, value=DEBUG_VALUE if debug else None
    # )
    # set_postgres_user(production_postgres_envs_path, value=postgres_user)
    # set_postgres_password(
    #     production_postgres_envs_path, value=DEBUG_VALUE if debug else None
    # )

    # set_celery_flower_user(local_django_envs_path, value=celery_flower_user)
    # set_celery_flower_password(
    #     local_django_envs_path, value=DEBUG_VALUE if debug else None
    # )
    # set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    # set_celery_flower_password(
    #     production_django_envs_path, value=DEBUG_VALUE if debug else None
    # )

def set_flags_in_settings_files():
    set_django_secret_key(os.path.join("config", "settings", "local.py"))
    set_django_secret_key(os.path.join("config", "settings", "test.py"))

def main():
    debug = "y".lower() == "y"

    set_flags_in_envs(
        DEBUG_VALUE if debug else generate_random_user(),
        DEBUG_VALUE if debug else generate_random_user(),
        debug=debug,
    )
    set_flags_in_settings_files()

