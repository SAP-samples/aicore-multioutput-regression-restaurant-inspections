# Python base image has to match the python version
# that you use locally.
FROM python:3.8-slim

RUN apt-get update && apt-get install -y libgomp1
RUN pip3 install --upgrade pip
COPY requirements.txt ./requirements.txt
# --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir

RUN mkdir -p /app/src/ && \
    mkdir -p /app/.cache

RUN chgrp -R nogroup /app && \
    chmod -R 770 /app

COPY serve.py /app/src/

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app && \
    # WORKAROUND: Allow sentence-transformers package to cache model.
    # Not to be used for production.
    chmod 777 /app/.cache

# Make sure that the gunicorn package is also listed in ./requirements.txt
CMD ["gunicorn", "--chdir", "/app/src", "serve:app", "-b", "0.0.0.0:9001"]