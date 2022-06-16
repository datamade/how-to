#!/bin/bash
result=0
trap 'result=1' ERR

flake8 {{cookiecutter.module_name}} tests
npx eslint {{cookiecutter.module_name}}/static/js/*.js
pytest -sxv

exit "$result"
