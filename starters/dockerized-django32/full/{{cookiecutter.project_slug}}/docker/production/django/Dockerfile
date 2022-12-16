FROM ubuntu:jammy-20221101
# because ubuntu-focal uses python3 for latest python3.9 and pip3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# needed for universe repository
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

RUN pip install --upgrade pip==22.0.4

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

# As of 2022-12-08 Thursday LTS node 18.12.1 (includes npm 8.19.2)
# check at https://nodejs.org/en/download/
RUN npm install -g npm@8.19.2

# End of Tailwind requirement

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get -y clean

RUN mkdir /code
WORKDIR /code

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install pip-tools
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