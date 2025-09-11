#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Flask Hello World with Docker...${NC}"

# Create main directory
PROJECT_NAME="flask-hello-docker"
echo -e "${GREEN}Creating project directory: ${PROJECT_NAME}${NC}"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Create subdirectories
echo -e "${GREEN}Creating subdirectories...${NC}"
mkdir -p templates static

# Create app.py
echo -e "${GREEN}Creating app.py...${NC}"
cat > app.py << 'EOF'
from flask import Flask, render_template
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', 
                         hostname=os.environ.get('HOSTNAME', 'localhost'),
                         timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF

# Create requirements.txt
echo -e "${GREEN}Creating requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
Flask==3.0.0
gunicorn==21.2.0
EOF

# Create Dockerfile
echo -e "${GREEN}Creating Dockerfile...${NC}"
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 flaskuser && chown -R flaskuser:flaskuser /app
USER flaskuser

# Expose port
EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:app"]
EOF

# Create docker-compose.yml
echo -e "${GREEN}Creating docker-compose.yml...${NC}"
cat > docker-compose.yml << 'EOF'
services:
  web:
    build: .
    container_name: flask-hello-world
    ports:
      - "5001:5000"
    environment:
      - FLASK_ENV=development
      - PYTHONUNBUFFERED=1
    volumes:
      - ./:/app
    networks:
      - flask-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    container_name: flask-nginx
    ports:
      - "8000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - web
    networks:
      - flask-network
    restart: unless-stopped

networks:
  flask-network:
    driver: bridge
EOF

# Create nginx.conf
echo -e "${GREEN}Creating nginx.conf...${NC}"
cat > nginx.conf << 'EOF'
upstream flask_app {
    server web:5000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 30d;
    }
}
EOF

# Create templates/index.html
echo -e "${GREEN}Creating templates/index.html...${NC}"
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Hello World</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>🚀 Hello World from Flask!</h1>
        <div class="info-card">
            <p><strong>Container Hostname:</strong> {{ hostname }}</p>
            <p><strong>Current Time:</strong> {{ timestamp }}</p>
            <p><strong>Status:</strong> <span class="status">Running</span></p>
        </div>
        <div class="features">
            <h2>Features</h2>
            <ul>
                <li>✅ Auto-deployed with Docker</li>
                <li>✅ Production-ready with Gunicorn</li>
                <li>✅ Nginx reverse proxy</li>
                <li>✅ Health check endpoint</li>
                <li>✅ Hot-reload in development</li>
            </ul>
        </div>
        <div class="endpoints">
            <h2>Available Endpoints</h2>
            <ul>
                <li><a href="/">/</a> - This page</li>
                <li><a href="/health">/health</a> - Health check API</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

# Create static/style.css
echo -e "${GREEN}Creating static/style.css...${NC}"
cat > static/style.css << 'EOF'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #333;
}

.container {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    max-width: 600px;
    width: 90%;
}

h1 {
    color: #667eea;
    margin-bottom: 30px;
    text-align: center;
    font-size: 2.5em;
}

.info-card {
    background: #f7f9fc;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 30px;
}

.info-card p {
    margin: 10px 0;
    font-size: 1.1em;
}

.status {
    color: #10b981;
    font-weight: bold;
}

.features, .endpoints {
    margin-top: 30px;
}

h2 {
    color: #764ba2;
    margin-bottom: 15px;
    font-size: 1.5em;
}

ul {
    list-style: none;
    padding-left: 0;
}

li {
    padding: 8px 0;
    font-size: 1.05em;
}

a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

a:hover {
    text-decoration: underline;
}
EOF

# Create .env.example
echo -e "${GREEN}Creating .env.example...${NC}"
cat > .env.example << 'EOF'
FLASK_ENV=development
FLASK_DEBUG=1
EOF

# Create .env from .env.example
echo -e "${GREEN}Creating .env...${NC}"
cp .env.example .env

# Create .gitignore
echo -e "${GREEN}Creating .gitignore...${NC}"
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# Flask
instance/
.webassets-cache

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Docker
*.log
EOF

# Create README.md
echo -e "${GREEN}Creating README.md...${NC}"
cat > README.md << 'EOF'
# Flask Hello World with Docker Auto-Deployment

A simple Flask application that auto-deploys with Docker, featuring a production-ready setup with Gunicorn and Nginx.

## 🚀 Quick Start

Clone and run the application:

```bash
# Clone the repository
git clone https://github.com/yourusername/flask-hello-docker.git
cd flask-hello-docker

# Copy environment variables
cp .env.example .env

# Build and run with Docker Compose
docker-compose up -d