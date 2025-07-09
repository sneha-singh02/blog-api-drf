# syntax=docker/dockerfile:1.4

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn server
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
