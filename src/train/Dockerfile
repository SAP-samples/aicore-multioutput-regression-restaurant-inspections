# Python base image has to match the python version
# that you use locally.
FROM python:3.8-slim

RUN apt-get update && apt-get install -y libgomp1
RUN pip3 install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/src/ && \
    mkdir -p /app/model && \
    mkdir -p /app/.cache

COPY train.py /app/src/
# To run container locally with data.

# Replace training-dataset.csv with the csv file
# you stored in AWS S3.
ENV DATA_SOURCE=/app/data
ENV OUTPUT_PATH=/app/model

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app && \
    # WORKAROUND: Allow sentence-transformers package to cache model.
    # Not to be used for production.
    chmod 777 /app/.cache