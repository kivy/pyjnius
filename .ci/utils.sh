#!/bin/bash
set -e -x

ensure_python_version(){
    # This function ensures that the correct python version is selected.
    # It takes one argument, the python version to use.

    # On github-hosted runners, we use the setup-python action to install the correct python version,
    # so we don't need to do anything.

    python_version="$1"
    # if KIVY_SELF_HOSTED_USE_PYENV is set to 1, we use pyenv to select the python version
    if [[ "$KIVY_SELF_HOSTED_USE_PYENV" == "1" ]]; then
        source ~/.bashrc
        pyenv global $python_version
    fi
}