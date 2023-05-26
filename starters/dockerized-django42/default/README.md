# Dockerized Django Default Starter

All GreenDeploy Starters are basically Cookiecutter Templates.

This specific Starter is the default for dockerized-django.

the users app and therefore User model is hard-determined in `base`

in future allow users app to be in `domains` and rename `users` app in `base` is to provide the abstract classes instead under the name `users_base`

we want to use django-improved-user and django-allauth by default going forward
