#!/bin/bash
result=0
trap 'result=1' ERR

flake8 {{ cookiecutter.module_name }} tests
pytest -sxv

exit "$result"
