#!/bin/bash

# lanzamos los test

source .venv/bin/activate
pytest --cov=service --cov-report=html

#abrimos el reporte html
xdg-open htmlcov/index.html