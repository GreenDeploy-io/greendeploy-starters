// BEGIN_REPLACE
// {{ cookiecutter.project_name }} => {{ '{{ cookiecutter.project_name }}' }}
// {{ cookiecutter.project_slug }} => {{ '{{ cookiecutter.project_slug }}' }}
// REPLACE_START
# {{ cookiecutter.project_name }}

Your one-liner explainer
// REPLACE_END

## GET STARTED

1. turn on terminal
2. at root of project, run `. .infrastructure/.macos/.venv-scripts/init_venv.sh`
3. run `source .venv/{{ cookiecutter.project_slug }}/bin/activate` to turn on virtual environment ( to turn off use `deactivate`)
4. run `pip install -r .infrastructure/requirements/dev.txt` to install development dependencies in the virtual environment
5. run ``pip install --upgrade pip`` if prompted in the virtual environment
6. run ``pip install -r requirements.txt`` to install app dependencies in the virtual environment
7. run `python manage.py runserver "[::]:8000"` to run the django app. (to turn off use `Ctrl+C`)
8. go to localhost:8000 to see `Django + Tailwind = ❤️` (this means working)
9. to test the pages, go to `http://localhost:8000/web_enterprise/quotation_approval` (you can then see the componentized versions)
10. the originally skinned html files are under original_html


## Questions

- scroll-smooth (universal or quotation_approval only?)
- body class (universal or quotation-approval only?)

![alt text](image.png)