#!/bin/bash
echo "-------------------------------------------------------"
ls
echo "-------------------------------------------------------"
ls -a | grep msg
echo "-------------------------------------------------------"
pip install pipenv
pipenv install
pipenv run python main.py

