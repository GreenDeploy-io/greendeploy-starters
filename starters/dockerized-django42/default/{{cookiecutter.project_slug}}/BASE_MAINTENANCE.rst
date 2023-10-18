=================
Base Maintenance
=================

The following needs to be updated regularly in the starter template.

1. in the 2 Dockerfiles (docker/local/django, docker/production/django)
    1. pip
    2. pip-tools
    3. the base image
2. in the other Dockerfiles (docker/local/nginx, docker/local/postgres, docker/local/redis)
    1. the base image
2. in the base-base.in,
    1. all the packages
    2. remember to run `pip-compile`

Changelog
=========

0.0.4 (2023-10-21 Saturday)
---------------------------

- Add output_cookiecutter.json
- Add python-benedict, webargs, marshmallow to base-base.in
- Update .skip-reverse
- Add .skip-overwrite
- Update dependencies in the base-local.in
- Improve `config/settings/complements` with new files: `.complements`, and `__init__.py`


0.0.3 (2023-10-14 Saturday)
---------------------------

- Update django, psycopg, pytz, django-allauth, and redis in the base-base.in
- Update ubuntu-jammy version in Dockerfiles


0.0.2 (2023-10-03 Tuesday)
---------------------------

- Add complements as a way to extend base


0.0.1 (2023-09-24 Sunday)
-------------------------

- Update argon2-cffi, django-allauth in the base-base.in
- Update pip, pip-tools in the Django dockerfiles
- Update all the dockerfiles to the latest versions
- Initial release


