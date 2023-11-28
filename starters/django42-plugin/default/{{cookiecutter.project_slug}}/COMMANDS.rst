
Sometimes, the POSTGRES is updated, so need to upgrade the collation

.. code-block:: bash

    cpopv2-django42-db_postgres-1  | 2023-10-25 05:07:09.172 UTC [24] WARNING:  database "cpopv2_django42" has a collation version mismatch
    cpopv2-django42-db_postgres-1  | 2023-10-25 05:07:09.172 UTC [24] DETAIL:  The database was created using collation version 2.31, but the operating system provides version 2.36.
    cpopv2-django42-db_postgres-1  | 2023-10-25 05:07:09.172 UTC [24] HINT:  Rebuild all objects in this database that use the default collation and run ALTER DATABASE cpopv2_django42 REFRESH COLLATION VERSION, or build PostgreSQL with the right library version.

How to actually refresh collation version

.. code-block:: postgresql

    ALTER DATABASE cpopv2_django42 REFRESH COLLATION VERSION