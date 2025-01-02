#!/bin/bash

#ejecutamos el entrono virtual creado
venv/bin/pip install -e adi_token_srv-main

#ejecutamos el servidor
venv/bin/token_service

exec "$@"