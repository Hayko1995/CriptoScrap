FROM mcr.microsoft.com/playwright/python:v1.30.0-focal


WORKDIR /app
COPY requirements.txt /app/


RUN pip install --no-cache-dir --upgrade pip   && pip install --no-cache-dir -r requirements.txt

COPY . /app