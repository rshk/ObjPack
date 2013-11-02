#!/bin/bash

# To install requirements:
# pip install tox pytest pytest-pep8 pytest-cov

py.test --ignore=build --pep8 -v --cov=objpack --cov-report=term-missing objpack "$@"
