FROM ubuntu:latest


RUN groupadd -r user && useradd -r -g user user


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl

WORKDIR /app

COPY config/ /app/config
COPY requirements.txt /app
COPY service /app/service
COPY pyproject.toml /app
COPY bootstrap.py /app
COPY test /app/tests
COPY start_tests.sh /app
COPY delete_tests.sh /app

RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
EXPOSE 3001

RUN chmod +x start_tests.sh
RUN chmod +x delete_tests.sh
RUN python3 bootstrap.py
RUN chown -R user:user /app

USER user
ENV token_endpoint="http://192.168.0.5:3002/api/v1/token"

CMD ["venv/bin/python", "service/command_handlers.py"]

