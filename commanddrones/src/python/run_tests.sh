#!/bin/bash

# This makes sures output is shown in the terminal
export PYTHONUNBUFFERED=true

python -m unittest discover -s ../tests -t ..
