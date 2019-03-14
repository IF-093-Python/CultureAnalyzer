#!/usr/bin/env bash

changed=$(git diff --cached --name-only)

echo ${changed} | xargs egrep '^[><=]{7}( |$)' -H -I --line-number

# If the egrep command has any hits - echo a warning and exit with non-zero status.
if [ $? == 0 ]; then
    echo "WARNING: You have merge markers in the above files. Fix them before committing."
    exit 1
else
    egrep '^[><=]{7}( |$)' -H -I --line-number -lr . | grep -v 'venv/'
    if [ $? == 0 ]; then
        echo "WARNING: You have merge markers in the above files. Fix them before committing."
        exit 1
    fi
    echo "No merge markers found. Fine..."
fi