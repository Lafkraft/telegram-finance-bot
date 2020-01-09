FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""
ENV TELEGRAM_ACCESS_ID=""
ENV TELEGRAM_PROXY_URL=""

COPY *.py ./
COPY createdb.sql ./
COPY pip_requirements.txt ./

RUN pip install -r pip_requirements.txt

ENTRYPOINT ["python", "server.py"]

