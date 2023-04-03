from .base import *  # noqa
from .base import env

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[".localhost", "0.0.0.0", "127.0.0.1"])
