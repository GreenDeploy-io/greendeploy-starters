// BEGIN_REPLACE
// {{ cookiecutter.project_name }} => {{ '{{ cookiecutter.project_name }}' }}
// {{ cookiecutter.project_slug }} => {{ '{{ cookiecutter.project_slug }}' }}
// REPLACE_START
# How to use .infrastructure to setup a virtual environment in macOS

Tested in ventura macOS 13.6

## Why need virtual environment

A virtual environment in Python is a self-contained directory that contains a Python installation for a particular version of Python, along with additional packages.

Using a virtual environment allows you to manage dependencies for your project without affecting the global Python installation or other projects.

This means you can have project-specific libraries and versions, avoiding conflicts and ensuring consistency across development, testing, and production environments.


## How to

Each howto is a pre-requisite for the subsequent howto.

You can do your own way to accomplish the same outcome, but if you're a complete newbie, I recommend you follow exactly.

### How to install pyenv

Objective: to have pyenv installed and a python version installed in `$(pyenv root)/versions/` that matches the one in `.python-version`

How to tell success:

To check, type in terminal `cd $(pyenv root)/versions/` and look for `3.12.5` for e.g.

If you haven't already installed `pyenv`, you can follow the steps here.

Steps:

- `brew update`
- `brew upgrade`
- `brew install pyenv`
- `pyenv install 3.x.x` (or whatever version stated in `.infrastructure/.macos/.python-version`) so in this case it should be `pyenv install 3.12.5`


### How to setup a specific virtual environment for this project

Pre-requisites:

- `pyenv` installed
- `.venv` folder created inside project folder (done for you)

Objective: to have a dedicated virtual environment for this project installed of a specific python version

How to tell success:

when inside `/path/to/your/project/.venv`, we have:

- `/path/to/your/project/.venv/your-project-3xx`
- `/path/to/your/project/.venv/your-project` as symlink to the above newly created virtual environment

Why do it this way:

I find it useful to have the _option_ of having multiple virtual environments for the same project.

Another thing I find useful is to have the python version stated in the virtual environment folder name.

Steps:

1. one-off: make sure ``.variables`` follows ``.variables.original`` with project name set correctly as `your-project`.

This repository uses `{{ cookiecutter.project_slug }}` as project name.

Do not change `.variables.original`. You may change `.variables`.

2. run `. .infrastructure/.macos/.venv-scripts/init_venv.sh` in project root.

This script MUST be executed at project root. And it saves you many steps.

This step will create the virtual environment (henceforth venv for short) `/path/to/your/project/.venv/{{ cookiecutter.project_slug }}-31013` and then create a symlink `/path/to/your/project/.venv/{{ cookiecutter.project_slug }}` pointing to this venv.


### How to turn on and turn off virtual environment

1. turn on

```bash
`source /path/to/your/project/.venv/your-project/bin/activate`
```

2. deactivate

```bash
deactivate
```

### How to install dependencies in the venv (or how to run locally)

Objective: install the necessary dependencies in the venv for the project.

How to tell if success: when visit http://localhost:8000 and gets redirected to /hello showing a JSON response.

1. pre-requisites: make sure the venv is turned on before doing anything with the project locally.
2. at the project root, `pip install -r .infrastructure/requirements/dev.txt`

The dependencies stated here are useful for debugging.

3. run ``pip install --upgrade pip`` if prompted
4.  run ``pip install -r requirements.txt``

The dependencies here are for the project.

5.  run ``python manage.py runserver`` for localhost

now you're ready to run the project. Go to http://localhost:8000 and you should see

Django + Tailwind = ❤️

This means all the dependencies are installed correctly. Congratulations!


## Other useful scripts


run `. .infrastructure/.macos/.venv-scripts/check_for_newer_py_versions.sh`

This step will try to find the latest patch version given the minor version stated in `.python-version`.

run `. .infrastructure/.macos/.venv-scripts/source_venv.sh`

This step will teach you how to turn on and turn off the virtual environment.

1. run `source .venv/{{ cookiecutter.project_slug }}/bin/activate` to turn on the virtual environment
2. run `deactivate`  to deactivate the virtual environment

// REPLACE_END