FROM python:3.10.13-bookworm

WORKDIR /app

COPY ./docker/Dockerfile /app
COPY ./requirements.txt /app
COPY ./app.py /app


RUN pip install --upgrade pip && \
    pip install -r requirements.txt


CMD ["python3", "-u", "app.py"]
