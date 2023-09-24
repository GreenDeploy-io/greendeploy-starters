from .base import *  # noqa

THIRD_PARTY_APPS_IN_BASE_LOCAL = ["django_browser_reload"]

MIDDLEWARE_IN_BASE_LOCAL = ["django_browser_reload.middleware.BrowserReloadMiddleware"]
