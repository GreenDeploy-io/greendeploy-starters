#!/bin/bash

# Source the variables from .variables file
source .infrastructure/.macos/.venv-scripts/.variables

# Define colors and styles
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2)

if [ -n "$venv_symlink" ]; then
  echo "To activate the virtual environment, run the following command:"
  echo "${BOLD}${GREEN}source /path/to/your/project/.venv/$venv_symlink/bin/activate${NORMAL}"
  echo ""
  echo "OR go to PROJECT ROOT:"
  echo "${BOLD}${GREEN}source .venv/$venv_symlink/bin/activate${NORMAL}"
  echo ""
  echo "To deactivate the virtual environment, simply run:"
  echo "${BOLD}${GREEN}deactivate${NORMAL}"
  echo ""
  echo "Note: This script prints the 'source' command rather than running it directly "
  echo "because sourcing within a script won't affect the parent shell. "
  echo "Therefore, to make changes to the current shell, you'll need to run the 'source' command manually."
else
  echo "Error: venv_symlink is not set in .variables"
  exit 1
fi
