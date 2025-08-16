FROM python:3.10-slim-bullseye

WORKDIR /app

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}
ARG REFLEX_API_URL
ENV REFLEX_API_URL=${REFLEX_API_URL}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y unzip curl --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000
EXPOSE 8000

RUN reflex export