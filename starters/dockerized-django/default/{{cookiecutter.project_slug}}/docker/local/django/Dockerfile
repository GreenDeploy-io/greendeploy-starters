FROM ubuntu:focal-20211006
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

RUN apt-get install python3-pip -y

# for other standard libraries
RUN apt-get install -y --no-install-recommends \
    # psycopg2 dependencies
    libpq-dev gcc python3-dev

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get -y clean

# ubuntu does not have /code by default
RUN mkdir /code
WORKDIR /code
# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip3 install pip-tools
RUN pip-sync /requirements/base.txt /requirements/local.txt

COPY . /code/

# Copy the entrypoint to allow DATABASE_URL available
COPY ./docker/production/django/entrypoint /entrypoint
COPY ./docker/production/django/ /

# RUN for n in entrypoint start-*; do \
#     sed -i 's/\r//' /$n; \
#     chmod +x /$n; \
#     done

RUN ["chmod", "+x", "/entrypoint"]

# copy out /start-web
# start-web executes `migrate` and `runserver 0.0.0.0:8000`
COPY ./docker/local/django/start-web /start-web
RUN sed -i 's/\r//' /start-web
RUN chmod +x /start-web

ENTRYPOINT ["/entrypoint"]