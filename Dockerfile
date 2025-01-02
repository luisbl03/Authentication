FROM ubuntu:latest

RUN groupadd -r user && useradd -r -g user user
ENV token_endpoint="http://172.17.0.3:3002/api/v1/token"
ENV STORAGE_FOLDER="storage"
ENV ADMINPASS="admin"
ENV PYTHONPATH="/app"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    sqlite3 

WORKDIR /app

COPY service/__init__.py /app/service/__init__.py
COPY service/command_handlers.py /app/service/command_handlers.py
COPY service/authentication.py /app/service/authentication.py
COPY service/db_manager.py /app/service/db_manager.py
COPY service/service.py /app/service/service.py
COPY service/user.py /app/service/user.py
COPY bootstrap.py /app/bootstrap.py
COPY requirements.txt /app/requirements.txt
COPY pyproject.toml /app/pyproject.toml

RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
EXPOSE 3001


RUN python3 bootstrap.py
RUN chown -R user:user /app
RUN venv/bin/pip install -e .
USER user

CMD ["venv/bin/auth_service"]

