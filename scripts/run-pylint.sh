#!/usr/bin/env bash

touch __init__.py

if [ "$1" = "--file" ]; then
    pylint ../CultureAnalyzer --rcfile=.pylintrc -r n \
    --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint_report_file.txt
else
    pylint ../CultureAnalyzer --rcfile=.pylintrc
fi

rm __init__.py