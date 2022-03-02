# {{ cookiecutter.project_name }}

## How to start

Prerequsites:

1. must be in the project directory
2. must have pyenv
3. must have venv
4. project directory must have git init locally, committed immediately upon clone, and tagged immediately as v0.0.0 upon clone.

```
cd {{ cookiecutter.full_path_to_your_project }}{{ cookiecutter.project_slug }}

{{ cookiecutter.full_path_to_pyenv }}/versions/3.10.1/bin/python3.10 -m venv {{ cookiecutter.full_path_to_venv }}{{ cookiecutter.project_slug }}-py3101

source {{ cookiecutter.full_path_to_venv }}{{ cookiecutter.project_slug }}-py3101/bin/activate

python -m pip install --upgrade "{{ cookiecutter.pip_version }}"

pip install pip-tools "{{ cookiecutter.pip_tools_version }}"

git init .

git add .
git commit -m '🎉 Initial commit'
git tag -a v0.0.0 -m '🔖 First tag v0.0.0'

pip-compile

pip-sync

pip install -e .
```

Now run

```
python -m {{ cookiecutter.project_slug }}
```

see as 0.0.0

Make some small change and press save for example by adding either a ✅ or ❌ here  under GETTING_STARTED

Then run `pip install -e` and then see `and python -m {{ cookiecutter.project_slug }}`

see `0.0.1.dev0+g3f858c4.d20220215`

YOU MUST MAKE AT LEAST 1 ACTUAL COMMIT that comes AFTER your v0.0.0 tag.
Now run `git add GETTING_STARTED.md`
Now run `git commit -m '♻️ REFACTOR: GETTING_STARTED.md'`

NOW MAKE v0.0.1 tag
Now run `git tag -a v0.0.1 -m '🔖 Second tag v0.0.1'`

Then run `pip install -e` and then see `and python -m {{ cookiecutter.project_slug }}`

see `0.0.1`


## Actual content

Warning! This is not a real Python project.

This Demo Public Python Project is meant to demonstrate the following:

1. setup a generic Python project,
2. how to version it,
3. how to have layered requirements using setup.py and setup.cfg,
4. and finally have it up on PyPi as a public package

## Expected Output

Using [Gherkin language](https://behave.readthedocs.io/en/stable/philosophy.html#the-gherkin-language)

Scenario: In commandline
```
    GIVEN commandline
    AND inside python 3.10 venv
    AND all the dependencies under requirements.txt are installed
    WHEN i run `python -m demopublicpythonproject` in commandline
    THEN i expect this output
```

Scenario: Calling this in python shell
```
    GIVEN commandline
    AND inside python 3.10 venv
    AND all the dependencies under requirements.txt are installed
    AND i run `python`
    WHEN i run `from demopublicpythonproject.framework import hello_world_output
    AND i call `hello_world_output`
    THEN i expect this output as string
```
https://stackoverflow.com/questions/60430112/single-sourcing-package-version-for-setup-cfg-python-projects
https://pythonrepo.com/repo/pypa-setuptools_scm-python-build-tools
https://stackoverflow.com/questions/56883909/setuptools-scm-current-version-instead-of-next-version
https://stackoverflow.com/questions/71090408/how-to-use-release-branch-to-increment-version-using-setuptools-scm?noredirect=1#comment125820779_71090408
https://realpython.com/pypi-publish-python-package/#versioning-your-package