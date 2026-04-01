FROM python:3.11-slim

LABEL maintainer="afsh4ck" \
      description="HackLabs – Intentionally Vulnerable Labs" \
      version="1.0"

WORKDIR /app

# Install system dependencies for real SSH, SMB and FTP services
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    samba \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create required directories and init DB
RUN mkdir -p uploads logs static/files && python init_db.py

# HTTP / FTP / SSH / SMB (+ PASV ports for vsftpd)
EXPOSE 21 22 80 445 40000-40010

# Run on port 80 inside the container (macvlan – IP propia)
# docker-compose bridge sobreescribe con APP_PORT=5000
ENV APP_PORT=80

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
