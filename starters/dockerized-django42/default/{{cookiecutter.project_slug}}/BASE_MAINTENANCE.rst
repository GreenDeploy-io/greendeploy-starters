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
---------

0.0.2 (2023-10-03 Tuesday)
^^^^^^^^^^^^^^^^^^^^^^^^^

- Add complements as a way to extend base


0.0.1 (2023-09-24 Sunday)
^^^^^^^^^^^^^^^^^^^^^^^^^

- Update argon2-cffi, django-allauth in the base-base.in
- Update pip, pip-tools in the Django dockerfiles
- Update all the dockerfiles to the latest versions
- Initial release