# Infrastructure

This folder consists of useful scripts to make life easier for the python developer when developing on a local machine.

It's not part of the actual project itself.

## Explaining Folder Structure

Currently, `.infrastructure` has a few main parts.

1. `.macos`
2. `requirements`
3. `.doap`


``.macos`` is for developers developing on macOS machines.

It contains a bunch of useful bash and python scripts.

There's a plan to have a `.windows` for developers on Windows machines.

`requirements` holds the dependencies needed for debugging.

`.doap` holds files useful for DigitalOcean App Platform.

## FAQs

1. Why are you using 3.12.3 as the default python version for the virtual environment?

I follow the cadence of Ubuntu Long Term Support (LTS) versions.

Ubuntu releases a LTS every two years and the last one was in 2024 April. Hence, version 24.04.

Each Ubuntu version comes with a default Python version.

In Ubuntu 24.04, the default Python is 3.12.

I just make sure that I keep to the latest patch version of 3.12 using ``check_for_newer_py_versions.sh``.



