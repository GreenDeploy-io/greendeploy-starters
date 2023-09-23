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

