FROM mcr.microsoft.com/playwright/python:v1.30.0-focal

RUN apt-get update
RUN apt-get install libgdal-dev -y 
RUN apt install gdal-bin python3-gdal -y
RUN pip install --upgrade pip
RUN pip install numpy


WORKDIR /app
COPY requirements.txt /app/


RUN pip install --no-cache-dir --upgrade pip 
RUN pip install  -r requirements.txt

COPY . /app

CMD [ "python3", "run.py" ]