FROM ubuntu:jammy-20230308

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# Needed for universe repository
# Django 3.2 LTS supports up to python 3.10
RUN apt-get install -y software-properties-common python3.10-venv

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# this is needed for the adding of ppa apt-add-repository
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# needed for pip3
RUN add-apt-repository universe

# cause everytime add apt-reposutory need to update to work
RUN apt-get update

RUN apt-get install git -y

RUN apt-get install vim -y

RUN pip install --upgrade pip==23.0.1

RUN apt-get update

#########################################
#
# Postgres
#   needs psycopg2-binary
#     which needs libpq-dev gcc python3-dev
#########################################


# for other standard libraries
RUN apt-get install -y --no-install-recommends \
    # psycopg2 dependencies
    libpq-dev gcc python3-dev

# End of Postgres requirement

#########################################
#
# Tailwind needs
#   node and npm
#     and node needs curl
#########################################
RUN apt-get update

# to install node
RUN apt-get install -y curl

# for getting latest LTS version
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash

RUN apt-get install -y --fix-missing \
    # for tailwind and no need to install npm cause node now comes with it prepackaged
    nodejs

# As of 2023-04-03 Latest LTS Version: 18.15.0 (includes npm 9.5.0)
# check at https://nodejs.org/en/download/
RUN npm install -g npm@9.5.0

# End of Tailwind requirement

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get -y clean

RUN mkdir /code
WORKDIR /code

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install pip-tools==6.12.3
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