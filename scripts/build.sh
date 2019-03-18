#!/usr/bin/env bash

echo "Detect merge markers..."
./scripts/merge-markers-detect.sh || exit 1

echo "Run tests with coverage..."
coverage erase
coverage run --branch --source='.' manage.py test || exit 1
coverage xml -i || exit 1

echo "Run pylint..."
./scripts/run-pylint.sh --file || exit 1
cat pylint_report_file.txt || exit 1