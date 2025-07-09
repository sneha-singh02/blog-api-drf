# syntax=docker/dockerfile:1.4

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional for API-only projects)
# RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the server using gunicorn (good for production)
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
