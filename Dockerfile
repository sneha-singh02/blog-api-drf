# Use official Python base image
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies for mysqlclient (or psycopg2 if using PostgreSQL)
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run DB migrations
RUN python manage.py migrate

# Start the server
CMD gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
