#!/usr/bin/env bash

set -e
set -x

mypy src
black src tests -l 120 --check
isort src scripts --check-only