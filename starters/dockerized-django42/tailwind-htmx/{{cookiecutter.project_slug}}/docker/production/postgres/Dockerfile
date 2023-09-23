# https://endoflife.date/postgresql
# 2023 Aug https://www.postgresql.org/docs/release/15.4/
FROM postgres:15.4

COPY ./maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

USER postgres