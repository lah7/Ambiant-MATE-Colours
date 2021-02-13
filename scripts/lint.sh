#!/bin/bash
#
# Performs a lint check on the Python generator script.
#
# Requires pylint for Python 3 to be installed.
#   In Ubuntu that package is "pylint3".
#   Some distro/releases might use "pylint".
#

pylint=""

if [ ! -z "$(which pylint3 2>/dev/null)" ]; then
    pylint="pylint3"
elif [ ! -z "$(which pylint 2>/dev/null)" ]; then
    pylint="pylint"
fi

if [ -z "$pylint" ]; then
    echo "Please install 'pylint3' to use this script."
    exit 1
fi

$pylint generate-ambiant-mate-colour.py --errors-only
