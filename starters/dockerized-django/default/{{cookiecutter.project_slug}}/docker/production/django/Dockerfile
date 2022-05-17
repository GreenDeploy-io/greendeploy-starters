FROM ubuntu:focal-20220426
# because ubuntu-focal uses python3 for latest python3.9 and pip3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# needed for universe repository
RUN apt-get install -y software-properties-common

# this is needed for the adding of ppa apt-add-repository
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# needed for pip3
RUN add-apt-repository universe

# cause everytime add apt-reposutory need to update to work
RUN apt-get update

RUN apt-get install git  -y

RUN apt-get install python3-pip -y

#########################################
#
# Postgres
#   needs psycopg2-binary
#     which needs libpq-dev gcc python3-dev
#########################################

# This is needed with --fix-missing
RUN apt-get update

# for other standard libraries
# --fix-missing is crucial as sometimes, the dependencies are missing such as libpq-dev on
# 2022-01-08 Saturday
RUN apt-get install -y --fix-missing \
    # psycopg2 dependencies
    libpq-dev gcc python3-dev

# End of Postgres requirement

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get -y clean


# ubuntu does not have /code by default
RUN mkdir /code
WORKDIR /code


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip3 install pip-tools
RUN pip-sync /requirements/base.txt /requirements/production.txt

COPY . /code/


# copy out /start-web
# start-web executes `migrate` and `runserver 0.0.0.0:8000`
# COPY ./docker/local/django/start-web /start-web
# RUN sed -i 's/\r//' /start-web
# RUN chmod +x /start-web

COPY ./docker/production/django/entrypoint /entrypoint
COPY ./docker/production/django/ /

RUN ["chmod", "+x", "/entrypoint"]

ENTRYPOINT ["/entrypoint"]