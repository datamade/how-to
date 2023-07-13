#!/bin/bash
result=0
trap 'result=1' ERR

pytest -sxv

exit "$result"
