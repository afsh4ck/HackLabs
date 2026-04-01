FROM python:3.11-slim

LABEL maintainer="afsh4ck" \
      description="HackLabs – Intentionally Vulnerable Labs" \
      version="1.0"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create required directories
RUN mkdir -p uploads logs static/files

# Initialize database
RUN python init_db.py

EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
