from config.settings.base.base import *  # noqa

# You MUST use wildcard imports as written above.
# The settings are in the following inheritance depending if `local` or `production`
#
# For `local`:
# `config/settings/base/base.py`
#            |
#            |-------------------------> `config/settings/base/local.py`
#            |--> `config/settings/domains/base.py` .     |
#                           |                             V
#                           |--------> `config/settings/domains/local.py`
# The same is true for `production`

# And extend them in here
# E.g. to extend THIRD_PARTY_APPS, you :
#
# from config.settings.base.base import *  # noqa
#
# THIRD_PARTY_APPS += ["some_third_party_app"] # because THIRD_PARTY_APPS is a list

