import importlib
import os
import warnings


def merge_constants(src_module_name, dest_module):
    src_module = importlib.import_module(src_module_name)

    if custom_merge_func := getattr(src_module, "custom_merge", None):
        custom_merge_func(dest_module)

    print(f"merging constants from: {src_module_name}")

    for attr_name in dir(src_module):
        attr_value = getattr(src_module, attr_name)

        if attr_name in dest_module and isinstance(dest_module[attr_name], list):
            # Append items to the list
            dest_module[attr_name].extend(attr_value)
        else:
            # Override the value
            dest_module[attr_name] = attr_value


# Start by merging from the base config
globals_dict = {}
merge_constants("config.settings.base.base", globals_dict)

# Read the .complements file for the list of sub-modules to process
complements_file_path = os.path.join(os.path.dirname(__file__), ".complements")

try:
    with open(complements_file_path, "r") as f:
        module_order = []
        for line in f:
            module_name = line.strip()
            module_path = os.path.join(
                os.path.dirname(__file__), module_name, "base.py"
            )
            if os.path.exists(module_path):
                module_order.append(module_name)
            else:
                warnings.warn(
                    f"Path for module {module_name} does not exist: {module_path}"
                )
except FileNotFoundError:
    warnings.warn(".complements file not found. Using an empty list.")
    module_order = []

# Import and reload the base.py files in the specified order
for module_name in module_order:
    try:
        module_path = f"config.settings.complements.{module_name}.base"
        merge_constants(module_path, globals_dict)
    except ImportError as e:
        warnings.warn(f"Failed to import module {module_name}: {e}")

# Finally, set the globals
globals().update(globals_dict)
