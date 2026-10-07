FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY test_app.py .

ARG BUILD_NUMBER=unknown
ARG GIT_COMMIT=unknown
ARG BRANCH_NAME=unknown
ARG APP_VERSION=unknown
ARG DOCKER_IMAGE=unknown

ENV BUILD_NUMBER=$BUILD_NUMBER
ENV GIT_COMMIT=$GIT_COMMIT
ENV BRANCH_NAME=$BRANCH_NAME
ENV APP_VERSION=$APP_VERSION
ENV DOCKER_IMAGE=$DOCKER_IMAGE

EXPOSE 8080

CMD ["python", "app.py"]
