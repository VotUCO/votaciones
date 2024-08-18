# Dockerfile
FROM python:3.10

RUN apt-get update && \
    apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Instalar Gunicorn
RUN pip install gunicorn

# Exponer el puerto que usa Gunicorn
EXPOSE 8000

ENTRYPOINT ["bash", "-c", "/app/deploy/wait-for-it.sh postgres:5432 -- python manage.py migrate && gunicorn --bind 0.0.0.0:8000 src.votaciones.wsgi:application"]