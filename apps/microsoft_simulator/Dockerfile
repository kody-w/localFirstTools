# Macrohard AI Simulation Docker Container
# Autonomous Microsoft Simulation Based on Elon Musk's Vision

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY macrohard_agents.py .
COPY index.html /usr/share/nginx/html/

# Configure nginx to serve the frontend
RUN echo 'server { \
    listen 8080; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
    } \
    location /api/ { \
        proxy_pass http://localhost:5000/api/; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
    } \
}' > /etc/nginx/sites-available/default

# Supervisor configuration
RUN echo '[supervisord] \n\
nodaemon=true \n\
\n\
[program:nginx] \n\
command=nginx -g "daemon off;" \n\
priority=10 \n\
\n\
[program:macrohard] \n\
command=python macrohard_agents.py \n\
priority=20 \n\
autorestart=true' > /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 5000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:5000/api/status || exit 1

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]