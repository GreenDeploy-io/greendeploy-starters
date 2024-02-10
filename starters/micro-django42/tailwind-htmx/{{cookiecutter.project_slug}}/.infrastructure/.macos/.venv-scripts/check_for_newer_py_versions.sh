#!/bin/bash

# Source the variables from .variables file
source .infrastructure/.macos/.venv-scripts/.variables

# Update pyenv based on the command in .variables
echo "Updating pyenv..."
eval $update_pyenv_command

# List all installed Python versions
installed_versions=$(pyenv versions --bare)

# Initialize variable to hold the latest version
latest_version="0"

# Loop through each installed version
for version in $installed_versions; do
  # Skip alpha, beta, rc versions
  if [[ $version =~ [a-zA-Z] ]]; then
    continue
  fi

  # Use sort -V to compare version numbers; if $version is greater, update $latest_version
  if [[ $(echo -e "$latest_version\n$version" | sort -V | tail -n1) == "$version" ]]; then
    latest_version=$version
  fi
done

# Check if latest_version is greater than current_version
if [[ $(echo -e "$current_version\n$latest_version" | sort -V | tail -n1) != "$current_version" ]]; then
  echo "A newer version is available: $latest_version"
else
  echo "You are using the latest version: $current_version"
fi
