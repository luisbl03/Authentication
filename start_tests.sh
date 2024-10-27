#!/bin/bash

# lanzamos los test

source .venv/bin/activate
pytest --cov=service --cov-report=html