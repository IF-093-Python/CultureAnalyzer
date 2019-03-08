#!/usr/bin/env bash

echo "Detect merge markers..."
./merge-markers-detect.sh

echo "Run tests with coverage..."
coverage erase
coverage run --branch --source='.' manage.py test
coverage xml -i

echo "Run pylint..."
touch __init__.py
pylint ../CultureAnalyzer --rcfile=.pylintrc -r n \
--msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint_report_file.txt
rm __init__.py