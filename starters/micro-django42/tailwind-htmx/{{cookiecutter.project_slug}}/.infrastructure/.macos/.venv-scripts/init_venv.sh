#!/bin/bash

# Source the variables from .variables file
source .infrastructure/.macos/.venv-scripts/.variables

# Find the project root directory
# Assuming the script is within the 'scripts' directory of the project
PROJECT_ROOT=$(git rev-parse --show-toplevel)

# Change to the project root directory
cd "$PROJECT_ROOT"

# Check if .venv directory exists at the project root. Create it if not.
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
  mkdir "$PROJECT_ROOT/.venv"
fi

# Check if venv_actual is empty
if [ -z "$venv_actual" ]; then
  # Read the Python version from .python-version
  target_version=$(cat $target_version_file)

  # Remove dots from the target version
  target_version_no_dots=$(echo "$target_version" | tr -d '.')

  # Build the actual venv name based on venv_symlink and target_version
  venv_actual="${venv_symlink}-${target_version_no_dots}"

  # Update .variables file with new venv_actual and current_version
  echo "venv_symlink=$venv_symlink" > $PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables
  echo "venv_actual=$venv_actual" >> $PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables
  echo "current_version=$target_version" >> $PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables
  echo "target_version_file=$target_version_file" >> $PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables
  echo "update_pyenv_command=\"$update_pyenv_command\"" >> $PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables

  echo "$PROJECT_ROOT/.infrastructure/.macos/.venv-scripts/.variables updated with new venv_actual and current_version."
fi

# Check if the virtual environment directory exists
if [ ! -d "$PROJECT_ROOT/.venv/$venv_actual" ]; then
  # Read the Python version from .python-version
  target_version=$(cat $target_version_file)

  # Build the path to the Python executable
  python_path="$(pyenv root)/versions/$target_version/bin/python"

  # Create the virtual environment
  $python_path -m venv $PROJECT_ROOT/.venv/$venv_actual

  # Create symlink
  ln -s $PROJECT_ROOT/.venv/$venv_actual $PROJECT_ROOT/.venv/$venv_symlink

  echo "Virtual environment $venv_actual created and symlinked as $venv_symlink."
else
  echo "Virtual environment $venv_actual already exists."
fi