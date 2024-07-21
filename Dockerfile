FROM python:3.12

ENV PYTHONWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /app/requirements.txt

COPY Django .

