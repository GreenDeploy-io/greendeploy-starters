django42/default-20230526 (2023-05-26)
**************************************

Note worthy changes
-------------------

- Rename the `CustomUser` model to `User` in `base.users`.
- Fix bugs that prevent the starter from immediately working when `docker compose -f local.yml up`. The cause appears to be related to the `base` folder renaming.