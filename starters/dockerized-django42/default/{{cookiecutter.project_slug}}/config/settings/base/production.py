from .base import *  # noqa
from .base import env

# BEGIN_REPLACE
# {{ cookiecutter.domain_name }} => {{ '{{ cookiecutter.domain_name }}' }}
# REPLACE_START
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["{{ cookiecutter.domain_name }}"])
# REPLACE_END
