# README - Local


## How to run project locally

Objective: install the necessary dependencies in the venv for the project.

Assumptions: you've correctly setup the venv for this project (if not cmd+f for "How to setup a specific virtual environment for this project")

How to tell if success: when visit http://localhost:8000 and gets redirected to /hello showing a JSON response.

1. pre-requisites: make sure the venv is turned on before doing anything with the project locally.
2. at the project root, `pip install -r .infrastructure/requirements/dev.txt`

The dependencies stated here are useful for debugging.

3. run ``pip install --upgrade pip`` if prompted
4.  run ``pip install -r requirements.txt``

The dependencies here are for the project.

5.  run ``python manage.py runserver "[::]:8000"`` for localhost

now you're ready to run the project. Go to http://localhost:8000 and you should see a json response in your browser after being redirected.

This means all the dependencies are installed correctly. Congratulations!

## How to get tailwind htmx working locally

1. stop ``python manage.py runserver "[::]:8000"`` if you're running it
2. ``python manage.py tailwind install``
3. run ``python manage.py runserver "[::]:8000"`` in current terminal tab
4. open new tab and activate the venv
5. run ``python manage.py tailwind start``
6. go to http://localhost:8000 and you should see `Django + Tailwind = ❤️` in middle of page and this means it works