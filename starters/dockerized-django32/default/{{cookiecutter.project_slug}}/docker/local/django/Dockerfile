# because ubuntu-jammy uses python3 for latest python3.10 and pip3
FROM ubuntu:jammy-20230624

# Create it as a "system" user without a home directory (-r)
# Do not force a specific numeric uid
# see https://stackoverflow.com/a/76850816/80353 for details
RUN useradd -r app_user

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# needed for universe repository
RUN apt-get install -y software-properties-common build-essential python3.10-venv

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

# To ensure pip3 works
RUN apt-get install python3-pip -y

# April 2023 pip==23.1.2
RUN pip3 install --upgrade pip==23.1.2

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
    libpq-dev gcc python3.10-dev

# End of Postgres requirement

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get -y clean

RUN mkdir /code
WORKDIR /code

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

# July 2023 pip-tools==6.14.0
RUN pip3 install pip-tools==6.14.0
RUN pip-sync /requirements/base-base.txt /requirements/base-local.txt /requirements/domains-base.txt /requirements/domains-local.txt

COPY . /code/

# Copy the entrypoint to allow DATABASE_URL available
COPY ./docker/production/django/entrypoint /entrypoint
COPY ./docker/production/django/ /

# RUN for n in entrypoint start-*; do \
#     sed -i 's/\r//' /$n; \
#     chmod +x /$n; \
#     done

RUN chmod +x /entrypoint

# copy out /start-web
# start-web executes `migrate` and `runserver 0.0.0.0:8000`
COPY ./docker/local/django/start-web_django /start-web_django
RUN sed -i 's/\r//' /start-web_django
RUN chmod +x /start-web_django

# Specify the alternate user with the rest of the runtime metadata
# Prevent CWE ID 020
# Dockerfile Misconfiguration: Default User Privilege
USER app_user
ENTRYPOINT ["/entrypoint"]