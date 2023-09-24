from config.settings.base.local import *  # noqa
from config.settings.domains.base import *  # noqa

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS += THIRD_PARTY_APPS_IN_BASE_LOCAL  # noqa
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE += MIDDLEWARE_IN_BASE_LOCAL  # noqa

# You MUST use wildcard imports as written above.
# You SHOULD import from `config.settings.base.local` and `.base`.
# Either one or both using wildcard.
#
# The order is up to you.
#
# The settings have a specific structure for imports.
#
# For `local`:
# `config/settings/base/base.py`
#            |
#            |-------------------------> `config/settings/base/local.py`
#            |--> `config/settings/domains/base.py` .     |
#                           |                             V
#                           |--------> `config/settings/domains/local.py`
#
# The same structure is true for `production`. Just swap `local` for `production`.

# In this file you can override any setting from `.base`, or `config/settings/base.py`
# E.g. to extend THIRD_PARTY_APPS, you :
#
# from config.settings.base.local import *  # noqa
# from .base import *  # noqa
#
# THIRD_PARTY_APPS += ["some_third_party_app"] # because THIRD_PARTY_APPS is a list


