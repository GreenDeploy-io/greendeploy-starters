"""Entry point when invoked with python -m {{ cookiecutter.project_slug }}."""  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    import sys

    from {{ cookiecutter.project_slug }}.framework import main

    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m {{ cookiecutter.project_slug }}"
    main()
