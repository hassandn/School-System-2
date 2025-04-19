FROM docker.arvancloud.ir/python:3.12.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working directory
WORKDIR /code

# install system dependencies for GDAL
RUN apt-get update && \
    apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# set environment variables for GDAL
ENV GDAL_VERSION=3.8.1
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/gdal

# set environment variables for django
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# copy requirements.txt to working directory
COPY requirements.txt /code/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project files to working directory
COPY . /code/