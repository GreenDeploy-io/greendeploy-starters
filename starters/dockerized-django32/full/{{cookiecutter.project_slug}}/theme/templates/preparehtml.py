"""Small script to allow functions to be called from the command line.
Run this script without argument to list the available functions:

    $ python many_functions.py
    Available functions in many_functions.py:

    python many_functions.py a  : Do some stuff

    python many_functions.py b  : Do another stuff

    python many_functions.py c x y : Calculate x + y

    python many_functions.py d  : ?

Run this script with arguments to try to call the corresponding function:

    $ python many_functions.py a
    Function a

    $ python many_functions.py c 3 5
    3 + 5 = 8

    $ python many_functions.py z
    Function z not found
"""

import inspect
import os
import re
import sys


def prepare_html_for_cookiecutter(filepath):
    # Open the file in read mode
    with open(filepath, 'r') as file:
        # Read the contents of the file
        text = file.read()

    # Use regex to replace all occurrences of the word "apple" (case-insensitive) with "[apple]"
    text = re.sub(
        r'(?s)(?:{% raw %}).*?(?:{% endraw %})|({% [^%]+ %})',
        '{% raw %}\g<0>{% endraw %}', text, flags=re.IGNORECASE)
    text = re.sub(
        r'(?s)(?:{% raw %}).*?(?:{% endraw %})|({{[^%]+}})',
        '{% raw %}\g<0>{% endraw %}', text, flags=re.IGNORECASE)
    # because the g<0> will cause the existing {% raw %} to double
    # so need to remove the extra {% raw %} and {% endraw %}
    text = re.sub(
        r'({% raw %})+',
        '{% raw %}', text, flags=re.IGNORECASE)
    text = re.sub(
        r'({% endraw %})+',
        '{% endraw %}', text, flags=re.IGNORECASE)

    # Open the file in write mode
    with open(filepath, 'w') as file:
        # Write the modified content to the file
        file.write(text)

def prepare_html_in_dir(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                prepare_html_for_cookiecutter(filepath)

#######################################################################
#         Some logic to find and display available functions          #
#######################################################################

def _get_local_functions():
    return {
        name: obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isfunction(obj)
        and not name.startswith('_')
        and obj.__module__ == __name__
    }

def _list_functions(script_name):
    print(f"Available functions in {script_name}:")
    for name, f in _get_local_functions().items():
        print()
        arguments = inspect.signature(f).parameters
        print(f"python {script_name} {name} {' '.join(arguments)} : {f.__doc__ or '?'}")


#######################################################################
#         python preparehtml.py prepare_html_in_dir base/account          #
#######################################################################
if __name__ == '__main__':
    script_name, *args = sys.argv
    if args:
        functions = _get_local_functions()
        function_name = args.pop(0)
        if function_name in functions:
            function = functions[function_name]
            function(*args)
        else:
            print(f"Function {function_name} not found")
            _list_functions(script_name)
    else:
        _list_functions(script_name)