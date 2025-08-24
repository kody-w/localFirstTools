#!/bin/bash

# ============================================================================
# VM ABSTRACTION LAB - Progressive Virtualization Deployment System
# Author: kody-w
# Date: 2025-08-23
# Description: Deploys VMs/containers with increasing levels of abstraction
# ============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="vm-abstraction-lab"
CURRENT_USER="kody-w"
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S')

# ASCII Art Banner
show_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗   ██╗███╗   ███╗     █████╗ ██████╗ ███████╗████████╗██████╗  █████╗  ║
║  ██║   ██║████╗ ████║    ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗ ║
║  ██║   ██║██╔████╔██║    ███████║██████╔╝███████╗   ██║   ██████╔╝███████║ ║
║  ╚██╗ ██╔╝██║╚██╔╝██║    ██╔══██║██╔══██╗╚════██║   ██║   ██╔══██╗██╔══██║ ║
║   ╚████╔╝ ██║ ╚═╝ ██║    ██║  ██║██████╔╝███████║   ██║   ██║  ██║██║  ██║ ║
║    ╚═══╝  ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ║
║                                                                              ║
║           C T I O N   L A B   -   P R O G R E S S I V E   D E P L O Y       ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    echo -e "${GREEN}User: ${CURRENT_USER} | Date: ${TIMESTAMP} UTC${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════════════${NC}"
}

# Progress indicator
show_progress() {
    local message=$1
    echo -e "${YELLOW}⏳ ${message}${NC}"
}

show_success() {
    local message=$1
    echo -e "${GREEN}✅ ${message}${NC}"
}

show_error() {
    local message=$1
    echo -e "${RED}❌ ${message}${NC}"
}

show_info() {
    local message=$1
    echo -e "${BLUE}ℹ️  ${message}${NC}"
}

# Check prerequisites
check_prerequisites() {
    echo -e "${CYAN}═══ Checking Prerequisites ═══${NC}"
    
    local missing_tools=()
    
    # Check for required tools
    for tool in docker docker-compose kubectl minikube vagrant virtualbox qemu-system-x86_64; do
        if ! command -v $tool &> /dev/null; then
            missing_tools+=($tool)
            show_error "$tool is not installed"
        else
            show_success "$tool is installed"
        fi
    done
    
    # Install missing tools if needed
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo -e "${YELLOW}Installing missing tools...${NC}"
        
        # Detect OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if ! command -v brew &> /dev/null; then
                show_error "Homebrew is required. Please install from https://brew.sh"
                exit 1
            fi
            
            for tool in "${missing_tools[@]}"; do
                case $tool in
                    docker)
                        brew install --cask docker
                        ;;
                    kubectl)
                        brew install kubernetes-cli
                        ;;
                    minikube)
                        brew install minikube
                        ;;
                    vagrant)
                        brew install --cask vagrant
                        ;;
                    virtualbox)
                        brew install --cask virtualbox
                        ;;
                    qemu-system-x86_64)
                        brew install qemu
                        ;;
                esac
            done
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            for tool in "${missing_tools[@]}"; do
                case $tool in
                    docker)
                        curl -fsSL https://get.docker.com -o get-docker.sh
                        sudo sh get-docker.sh
                        sudo usermod -aG docker $USER
                        rm get-docker.sh
                        ;;
                    docker-compose)
                        sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                        ;;
                    kubectl)
                        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                        sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                        rm kubectl
                        ;;
                    minikube)
                        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                        sudo install minikube-linux-amd64 /usr/local/bin/minikube
                        rm minikube-linux-amd64
                        ;;
                    vagrant)
                        wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
                        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
                        sudo apt update && sudo apt install vagrant
                        ;;
                    virtualbox)
                        sudo apt update
                        sudo apt install virtualbox virtualbox-ext-pack
                        ;;
                    qemu-system-x86_64)
                        sudo apt update
                        sudo apt install qemu-kvm libvirt-daemon-system
                        ;;
                esac
            done
        fi
    fi
}

# Create project structure
create_project_structure() {
    show_progress "Creating project structure..."
    
    mkdir -p $PROJECT_NAME
    cd $PROJECT_NAME
    
    # Create directory structure for each abstraction level
    mkdir -p {level-0-process,level-1-container,level-2-compose,level-3-kubernetes,level-4-vm,level-5-nested,level-6-cloud,monitoring,scripts,configs}
    
    show_success "Project structure created"
}

# ============================================================================
# LEVEL 0: BASIC PROCESS (Direct execution)
# ============================================================================
setup_level_0_process() {
    echo -e "${CYAN}═══ LEVEL 0: Basic Process Execution ═══${NC}"
    show_info "Simplest form - running processes directly on the host"
    
    cd level-0-process
    
    # Create simple Python web server
    cat > simple_server.py << 'EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
from datetime import datetime

PORT = 8000
HOSTNAME = os.uname().nodename

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            info = {
                'level': 0,
                'type': 'Direct Process',
                'hostname': HOSTNAME,
                'timestamp': datetime.now().isoformat(),
                'message': 'Running directly on host OS'
            }
            self.wfile.write(json.dumps(info).encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    httpd.serve_forever()
EOF
    
    chmod +x simple_server.py
    
    # Create systemd service file
    cat > simple-server.service << EOF
[Unit]
Description=Level 0 Simple Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/simple_server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    show_success "Level 0 process setup complete"
    cd ..
}

# ============================================================================
# LEVEL 1: CONTAINER (Docker)
# ============================================================================
setup_level_1_container() {
    echo -e "${CYAN}═══ LEVEL 1: Container (Docker) ═══${NC}"
    show_info "Basic containerization with Docker"
    
    cd level-1-container
    
    # Create Node.js application
    cat > app.js << 'EOF'
const express = require('express');
const os = require('os');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    res.json({
        level: 1,
        type: 'Docker Container',
        hostname: os.hostname(),
        platform: os.platform(),
        timestamp: new Date().toISOString(),
        message: 'Running in isolated container'
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Level 1 Container running on port ${PORT}`);
});
EOF
    
    cat > package.json << 'EOF'
{
  "name": "level-1-container",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF
    
    # Create Dockerfile
    cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
USER node
CMD ["npm", "start"]
EOF
    
    # Build and run script
    cat > run.sh << 'EOF'
#!/bin/bash
docker build -t level-1-container .
docker run -d --name level-1-app -p 3001:3000 level-1-container
echo "Level 1 Container running at http://localhost:3001"
EOF
    
    chmod +x run.sh
    show_success "Level 1 container setup complete"
    cd ..
}

# ============================================================================
# LEVEL 2: DOCKER COMPOSE (Multi-container)
# ============================================================================
setup_level_2_compose() {
    echo -e "${CYAN}═══ LEVEL 2: Docker Compose (Multi-container) ═══${NC}"
    show_info "Orchestrating multiple containers with Docker Compose"
    
    cd level-2-compose
    
    # Create Flask API
    mkdir -p api
    cat > api/app.py << 'EOF'
from flask import Flask, jsonify
from redis import Redis
import os
from datetime import datetime

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def index():
    visits = redis.incr('visits')
    return jsonify({
        'level': 2,
        'type': 'Docker Compose',
        'service': 'API',
        'visits': visits,
        'hostname': os.environ.get('HOSTNAME'),
        'timestamp': datetime.now().isoformat(),
        'message': 'Multi-container orchestration'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'redis': redis.ping()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
    
    cat > api/requirements.txt << 'EOF'
Flask==3.0.0
redis==5.0.1
gunicorn==21.2.0
EOF
    
    cat > api/Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EOF
    
    # Create Frontend
    mkdir -p frontend
    cat > frontend/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Level 2 - Docker Compose</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
        }
        h1 { color: #667eea; }
        .info { 
            background: #f7f9fc; 
            padding: 20px; 
            border-radius: 8px;
            margin: 20px 0;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .label { font-weight: bold; }
        .value { color: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Level 2: Docker Compose</h1>
        <div class="info">
            <div class="metric">
                <span class="label">Architecture:</span>
                <span class="value">Multi-Container</span>
            </div>
            <div class="metric">
                <span class="label">Services:</span>
                <span class="value">API + Redis + Nginx</span>
            </div>
            <div class="metric">
                <span class="label">Orchestration:</span>
                <span class="value">Docker Compose</span>
            </div>
            <div class="metric">
                <span class="label">API Endpoint:</span>
                <span class="value">/api/</span>
            </div>
        </div>
        <div id="api-data"></div>
    </div>
    
    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/');
                const data = await response.json();
                document.getElementById('api-data').innerHTML = `
                    <div class="info">
                        <h3>Live API Data:</h3>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    </div>
                `;
            } catch (error) {
                console.error('Error fetching API data:', error);
            }
        }
        
        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>
EOF
    
    # Create Nginx config
    mkdir -p nginx
    cat > nginx/nginx.conf << 'EOF'
upstream api {
    server api:5000;
}

server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF
    
    # Create docker-compose.yml
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: ./api
    container_name: level2-api
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    networks:
      - level2-network
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    container_name: level2-redis
    volumes:
      - redis-data:/data
    networks:
      - level2-network
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    container_name: level2-nginx
    ports:
      - "3002:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - api
    networks:
      - level2-network
    restart: unless-stopped

networks:
  level2-network:
    driver: bridge

volumes:
  redis-data:
EOF
    
    show_success "Level 2 Docker Compose setup complete"
    cd ..
}

# ============================================================================
# LEVEL 3: KUBERNETES (Container Orchestration)
# ============================================================================
setup_level_3_kubernetes() {
    echo -e "${CYAN}═══ LEVEL 3: Kubernetes (Container Orchestration) ═══${NC}"
    show_info "Enterprise-grade container orchestration with Kubernetes"
    
    cd level-3-kubernetes
    
    # Create Go microservice
    cat > main.go << 'EOF'
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
)

type Response struct {
    Level     int       `json:"level"`
    Type      string    `json:"type"`
    Pod       string    `json:"pod"`
    Node      string    `json:"node"`
    Namespace string    `json:"namespace"`
    Timestamp time.Time `json:"timestamp"`
    Message   string    `json:"message"`
}

func main() {
    http.HandleFunc("/", handler)
    http.HandleFunc("/health", health)
    
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    
    log.Printf("Level 3 Kubernetes service starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
    response := Response{
        Level:     3,
        Type:      "Kubernetes",
        Pod:       os.Getenv("HOSTNAME"),
        Node:      os.Getenv("NODE_NAME"),
        Namespace: os.Getenv("POD_NAMESPACE"),
        Timestamp: time.Now(),
        Message:   "Container orchestration at scale",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func health(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, "OK")
}
EOF
    
    cat > go.mod << 'EOF'
module level3-k8s

go 1.20
EOF
    
    # Create Dockerfile
    cat > Dockerfile << 'EOF'
FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.mod ./
COPY main.go ./
RUN go build -o server main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]
EOF
    
    # Create Kubernetes manifests
    cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: level3-app
  labels:
    app: level3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: level3
  template:
    metadata:
      labels:
        app: level3
    spec:
      containers:
      - name: app
        image: level3-k8s:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          limits:
            memory: "128Mi"
            cpu: "100m"
          requests:
            memory: "64Mi"
            cpu: "50m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: level3-service
spec:
  selector:
    app: level3
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: level3-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: level3-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
EOF
    
    # Create deployment script
    cat > deploy.sh << 'EOF'
#!/bin/bash
echo "Starting Minikube..."
minikube start --driver=docker --cpus=2 --memory=4096

echo "Building Docker image..."
eval $(minikube docker-env)
docker build -t level3-k8s:latest .

echo "Deploying to Kubernetes..."
kubectl apply -f deployment.yaml

echo "Waiting for deployment..."
kubectl wait --for=condition=available --timeout=300s deployment/level3-app

echo "Getting service URL..."
minikube service level3-service --url
EOF
    
    chmod +x deploy.sh
    show_success "Level 3 Kubernetes setup complete"
    cd ..
}

# ============================================================================
# LEVEL 4: VIRTUAL MACHINES (Vagrant)
# ============================================================================
setup_level_4_vm() {
    echo -e "${CYAN}═══ LEVEL 4: Virtual Machines (Vagrant) ═══${NC}"
    show_info "Full OS virtualization with Vagrant and VirtualBox"
    
    cd level-4-vm
    
    # Create Vagrantfile
    cat > Vagrantfile << 'EOF'
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Multi-VM setup
  
  # Web Server VM
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/jammy64"
    web.vm.hostname = "level4-web"
    web.vm.network "private_network", ip: "192.168.56.10"
    web.vm.network "forwarded_port", guest: 80, host: 3004
    
    web.vm.provider "virtualbox" do |vb|
      vb.name = "level4-web"
      vb.memory = "1024"
      vb.cpus = 1
    end
    
    web.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y nginx python3 python3-pip
      
      # Configure Nginx
      cat > /etc/nginx/sites-available/default <<-'NGINX'
server {
    listen 80 default_server;
    server_name _;
    
    location / {
        proxy_pass http://192.168.56.11:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX
      
      systemctl restart nginx
      echo "Web VM provisioned successfully"
    SHELL
  end
  
  # Application Server VM
  config.vm.define "app" do |app|
    app.vm.box = "ubuntu/jammy64"
    app.vm.hostname = "level4-app"
    app.vm.network "private_network", ip: "192.168.56.11"
    
    app.vm.provider "virtualbox" do |vb|
      vb.name = "level4-app"
      vb.memory = "1024"
      vb.cpus = 1
    end
    
    app.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y python3 python3-pip
      pip3 install flask gunicorn
      
      # Create Flask app
      cat > /home/vagrant/app.py <<-'PYTHON'
from flask import Flask, jsonify
import socket
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'level': 4,
        'type': 'Virtual Machine',
        'vm_name': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'os': os.uname().sysname,
        'timestamp': datetime.now().isoformat(),
        'message': 'Full OS virtualization with Vagrant'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
PYTHON
      
      # Create systemd service
      cat > /etc/systemd/system/flask-app.service <<-'SERVICE'
[Unit]
Description=Flask Application
After=network.target

[Service]
User=vagrant
WorkingDirectory=/home/vagrant
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE
      
      systemctl daemon-reload
      systemctl enable flask-app
      systemctl start flask-app
      
      echo "App VM provisioned successfully"
    SHELL
  end
  
  # Database VM
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/jammy64"
    db.vm.hostname = "level4-db"
    db.vm.network "private_network", ip: "192.168.56.12"
    
    db.vm.provider "virtualbox" do |vb|
      vb.name = "level4-db"
      vb.memory = "1024"
      vb.cpus = 1
    end
    
    db.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y postgresql postgresql-contrib
      
      # Configure PostgreSQL
      sudo -u postgres psql -c "CREATE USER appuser WITH PASSWORD 'apppass';"
      sudo -u postgres createdb -O appuser appdb
      
      # Allow remote connections
      echo "host all all 192.168.56.0/24 md5" >> /etc/postgresql/14/main/pg_hba.conf
      echo "listen_addresses = '*'" >> /etc/postgresql/14/main/postgresql.conf
      
      systemctl restart postgresql
      echo "Database VM provisioned successfully"
    SHELL
  end
end
EOF
    
    # Create management script
    cat > manage.sh << 'EOF'
#!/bin/bash

case "$1" in
  start)
    echo "Starting VMs..."
    vagrant up
    echo "VMs started. Access web at http://localhost:3004"
    ;;
  stop)
    echo "Stopping VMs..."
    vagrant halt
    ;;
  destroy)
    echo "Destroying VMs..."
    vagrant destroy -f
    ;;
  ssh)
    vagrant ssh $2
    ;;
  status)
    vagrant status
    ;;
  *)
    echo "Usage: $0 {start|stop|destroy|ssh|status}"
    exit 1
    ;;
esac
EOF
    
    chmod +x manage.sh
    show_success "Level 4 VM setup complete"
    cd ..
}

# ============================================================================
# LEVEL 5: NESTED VIRTUALIZATION (VM in Container)
# ============================================================================
setup_level_5_nested() {
    echo -e "${CYAN}═══ LEVEL 5: Nested Virtualization (VM in Container) ═══${NC}"
    show_info "Running VMs inside containers with QEMU"
    
    cd level-5-nested
    
    # Create QEMU container Dockerfile
    cat > Dockerfile << 'EOF'
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    cloud-image-utils \
    bridge-utils \
    cpu-checker \
    libvirt-daemon-system \
    libvirt-clients \
    virtinst \
    curl \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Flask for API
RUN pip3 install flask

# Create VM management API
COPY vm_manager.py /app/vm_manager.py
COPY start.sh /app/start.sh

WORKDIR /app

# Download a minimal Linux image
RUN wget -q http://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img -O /app/vm-disk.img

EXPOSE 5000 5900

CMD ["/app/start.sh"]
EOF
    
    # Create VM manager API
    cat > vm_manager.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, jsonify, request
import subprocess
import os
import json
from datetime import datetime

app = Flask(__name__)

class VMManager:
    def __init__(self):
        self.vms = {}
        self.next_port = 5901
        
    def create_vm(self, name, memory="512", cpus="1"):
        if name in self.vms:
            return {'error': 'VM already exists'}
        
        vnc_port = self.next_port
        self.next_port += 1
        
        cmd = [
            'qemu-system-x86_64',
            '-name', name,
            '-m', memory,
            '-smp', cpus,
            '-drive', f'file=/app/vm-disk.img,format=qcow2',
            '-vnc', f':{vnc_port - 5900}',
            '-daemonize',
            '-enable-kvm' if os.path.exists('/dev/kvm') else '-accel', 'tcg'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            self.vms[name] = {
                'status': 'running',
                'vnc_port': vnc_port,
                'memory': memory,
                'cpus': cpus,
                'created_at': datetime.now().isoformat()
            }
            return {'success': True, 'vm': self.vms[name]}
        except Exception as e:
            return {'error': str(e)}
    
    def list_vms(self):
        return self.vms
    
    def stop_vm(self, name):
        if name not in self.vms:
            return {'error': 'VM not found'}
        
        try:
            subprocess.run(['pkill', '-f', f'-name {name}'], check=True)
            self.vms[name]['status'] = 'stopped'
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}

vm_manager = VMManager()

@app.route('/')
def index():
    return jsonify({
        'level': 5,
        'type': 'Nested Virtualization',
        'platform': 'QEMU in Docker',
        'timestamp': datetime.now().isoformat(),
        'message': 'VMs running inside containers',
        'capabilities': {
            'kvm': os.path.exists('/dev/kvm'),
            'nested': True
        }
    })

@app.route('/vms', methods=['GET'])
def list_vms():
    return jsonify(vm_manager.list_vms())

@app.route('/vms', methods=['POST'])
def create_vm():
    data = request.json or {}
    name = data.get('name', f'vm-{len(vm_manager.vms)}')
    memory = data.get('memory', '512')
    cpus = data.get('cpus', '1')
    
    result = vm_manager.create_vm(name, memory, cpus)
    return jsonify(result)

@app.route('/vms/<name>', methods=['DELETE'])
def stop_vm(name):
    result = vm_manager.stop_vm(name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
    
    # Create start script
    cat > start.sh << 'EOF'
#!/bin/bash
# Check KVM support
if [ -e /dev/kvm ]; then
    echo "KVM acceleration available"
else
    echo "KVM not available, using TCG acceleration"
fi

# Start libvirtd if available
if command -v libvirtd &> /dev/null; then
    libvirtd -d
fi

# Start VM manager API
python3 /app/vm_manager.py
EOF
    
    chmod +x start.sh
    
    # Create docker-compose for nested setup
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  vm-host:
    build: .
    container_name: level5-vm-host
    privileged: true
    ports:
      - "3005:5000"
      - "5900-5910:5900-5910"
    volumes:
      - /dev/kvm:/dev/kvm
      - vm-data:/app/vms
    devices:
      - /dev/kvm:/dev/kvm
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    security_opt:
      - apparmor:unconfined
    restart: unless-stopped

volumes:
  vm-data:
EOF
    
    show_success "Level 5 nested virtualization setup complete"
    cd ..
}

# ============================================================================
# LEVEL 6: CLOUD SIMULATION (LocalStack)
# ============================================================================
setup_level_6_cloud() {
    echo -e "${CYAN}═══ LEVEL 6: Cloud Simulation (LocalStack) ═══${NC}"
    show_info "Simulating cloud services locally"
    
    cd level-6-cloud
    
    # Create serverless application
    cat > lambda_function.py << 'EOF'
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'level': 6,
            'type': 'Cloud Simulation',
            'service': 'AWS Lambda (LocalStack)',
            'timestamp': datetime.now().isoformat(),
            'message': 'Serverless computing simulation',
            'event': event
        })
    }
EOF
    
    # Create Terraform configuration
    cat > main.tf << 'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    lambda         = "http://localhost:4566"
    s3             = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"
    apigateway     = "http://localhost:4566"
    iam            = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "app_bucket" {
  bucket = "level6-app-bucket"
}

# DynamoDB Table
resource "aws_dynamodb_table" "app_table" {
  name           = "level6-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# Lambda Function
resource "aws_lambda_function" "app_function" {
  filename         = "lambda.zip"
  function_name    = "level6-function"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda.zip")
  runtime         = "python3.9"
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "level6-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# API Gateway
resource "aws_api_gateway_rest_api" "app_api" {
  name = "level6-api"
}

resource "aws_api_gateway_resource" "app_resource" {
  rest_api_id = aws_api_gateway_rest_api.app_api.id
  parent_id   = aws_api_gateway_rest_api.app_api.root_resource_id
  path_part   = "app"
}

resource "aws_api_gateway_method" "app_method" {
  rest_api_id   = aws_api_gateway_rest_api.app_api.id
  resource_id   = aws_api_gateway_resource.app_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.app_api.id
  resource_id = aws_api_gateway_resource.app_resource.id
  http_method = aws_api_gateway_method.app_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app_function.invoke_arn
}
EOF
    
    # Create docker-compose for LocalStack
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  localstack:
    image: localstack/localstack:latest
    container_name: level6-localstack
    ports:
      - "4566:4566"
      - "4571:4571"
      - "3006:8080"
    environment:
      - SERVICES=lambda,s3,dynamodb,apigateway,iam,cloudformation,cloudwatch
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
      - LAMBDA_EXECUTOR=docker
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - localstack-data:/tmp/localstack
    networks:
      - cloud-network

  terraform:
    image: hashicorp/terraform:latest
    container_name: level6-terraform
    working_dir: /workspace
    volumes:
      - ./:/workspace
    networks:
      - cloud-network
    depends_on:
      - localstack
    entrypoint: ["sh", "-c", "sleep infinity"]

networks:
  cloud-network:
    driver: bridge

volumes:
  localstack-data:
EOF
    
    # Create deployment script
    cat > deploy.sh << 'EOF'
#!/bin/bash
echo "Creating Lambda deployment package..."
zip lambda.zip lambda_function.py

echo "Starting LocalStack..."
docker-compose up -d

echo "Waiting for LocalStack to be ready..."
sleep 10

echo "Initializing Terraform..."
docker-compose exec terraform terraform init

echo "Applying Terraform configuration..."
docker-compose exec terraform terraform apply -auto-approve

echo "Cloud simulation ready!"
echo "LocalStack Dashboard: http://localhost:3006"
echo "Services endpoint: http://localhost:4566"
EOF
    
    chmod +x deploy.sh
    show_success "Level 6 cloud simulation setup complete"
    cd ..
}

# ============================================================================
# MONITORING SETUP
# ============================================================================
setup_monitoring() {
    echo -e "${CYAN}═══ Setting Up Monitoring Stack ═══${NC}"
    show_info "Deploying Prometheus, Grafana, and monitoring tools"
    
    cd monitoring
    
    # Create Prometheus configuration
    cat > prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'level-0-process'
    static_configs:
      - targets: ['host.docker.internal:8000']
        labels:
          level: '0'
          type: 'process'

  - job_name: 'level-1-container'
    static_configs:
      - targets: ['level-1-app:3000']
        labels:
          level: '1'
          type: 'container'

  - job_name: 'level-2-compose'
    static_configs:
      - targets: ['level2-api:5000']
        labels:
          level: '2'
          type: 'compose'

  - job_name: 'level-3-kubernetes'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - default
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: level3

  - job_name: 'docker'
    static_configs:
      - targets: ['host.docker.internal:9323']
EOF
    
    # Create Grafana dashboard
    cat > dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "VM Abstraction Levels",
    "panels": [
      {
        "title": "Abstraction Levels Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up",
            "legendFormat": "{{level}} - {{type}}"
          }
        ]
      },
      {
        "title": "Resource Usage by Level",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes",
            "legendFormat": "Memory - {{name}}"
          }
        ]
      }
    ]
  }
}
EOF
    
    # Create monitoring docker-compose
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: monitoring-prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: monitoring-grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
      - ./dashboard.json:/var/lib/grafana/dashboards/dashboard.json
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=redis-datasource
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: monitoring-node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: monitoring-cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
EOF
    
    show_success "Monitoring stack setup complete"
    cd ..
}

# ============================================================================
# MASTER CONTROL SCRIPT
# ============================================================================
create_master_control() {
    echo -e "${CYAN}═══ Creating Master Control Script ═══${NC}"
    
    cat > control.sh << 'EOF'
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         VM ABSTRACTION LAB - MASTER CONTROL                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${GREEN}ABSTRACTION LEVELS:${NC}"
    echo "  0) Level 0 - Basic Process"
    echo "  1) Level 1 - Docker Container"
    echo "  2) Level 2 - Docker Compose"
    echo "  3) Level 3 - Kubernetes"
    echo "  4) Level 4 - Virtual Machines"
    echo "  5) Level 5 - Nested Virtualization"
    echo "  6) Level 6 - Cloud Simulation"
    echo
    echo -e "${BLUE}CONTROL OPTIONS:${NC}"
    echo "  a) Start ALL levels"
    echo "  s) Stop ALL levels"
    echo "  m) Launch Monitoring"
    echo "  t) Show Status"
    echo "  l) View Logs"
    echo "  q) Quit"
    echo
    echo -n "Select option: "
}

start_level() {
    case $1 in
        0)
            echo -e "${GREEN}Starting Level 0 - Basic Process...${NC}"
            cd level-0-process
            python3 simple_server.py &
            cd ..
            ;;
        1)
            echo -e "${GREEN}Starting Level 1 - Docker Container...${NC}"
            cd level-1-container
            ./run.sh
            cd ..
            ;;
        2)
            echo -e "${GREEN}Starting Level 2 - Docker Compose...${NC}"
            cd level-2-compose
            docker-compose up -d
            cd ..
            ;;
        3)
            echo -e "${GREEN}Starting Level 3 - Kubernetes...${NC}"
            cd level-3-kubernetes
            ./deploy.sh
            cd ..
            ;;
        4)
            echo -e "${GREEN}Starting Level 4 - Virtual Machines...${NC}"
            cd level-4-vm
            ./manage.sh start
            cd ..
            ;;
        5)
            echo -e "${GREEN}Starting Level 5 - Nested Virtualization...${NC}"
            cd level-5-nested
            docker-compose up -d
            cd ..
            ;;
        6)
            echo -e "${GREEN}Starting Level 6 - Cloud Simulation...${NC}"
            cd level-6-cloud
            ./deploy.sh
            cd ..
            ;;
        all)
            for i in {0..6}; do
                start_level $i
                sleep 2
            done
            ;;
    esac
}

stop_level() {
    case $1 in
        0)
            echo -e "${RED}Stopping Level 0...${NC}"
            pkill -f simple_server.py
            ;;
        1)
            echo -e "${RED}Stopping Level 1...${NC}"
            docker stop level-1-app
            docker rm level-1-app
            ;;
        2)
            echo -e "${RED}Stopping Level 2...${NC}"
            cd level-2-compose
            docker-compose down
            cd ..
            ;;
        3)
            echo -e "${RED}Stopping Level 3...${NC}"
            kubectl delete -f level-3-kubernetes/deployment.yaml
            minikube stop
            ;;
        4)
            echo -e "${RED}Stopping Level 4...${NC}"
            cd level-4-vm
            ./manage.sh stop
            cd ..
            ;;
        5)
            echo -e "${RED}Stopping Level 5...${NC}"
            cd level-5-nested
            docker-compose down
            cd ..
            ;;
        6)
            echo -e "${RED}Stopping Level 6...${NC}"
            cd level-6-cloud
            docker-compose down
            cd ..
            ;;
        all)
            for i in {0..6}; do
                stop_level $i
            done
            ;;
    esac
}

show_status() {
    echo -e "${CYAN}═══ System Status ═══${NC}"
    
    # Check Level 0
    if pgrep -f simple_server.py > /dev/null; then
        echo -e "Level 0: ${GREEN}●${NC} Running"
    else
        echo -e "Level 0: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 1
    if docker ps | grep -q level-1-app; then
        echo -e "Level 1: ${GREEN}●${NC} Running"
    else
        echo -e "Level 1: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 2
    if docker ps | grep -q level2; then
        echo -e "Level 2: ${GREEN}●${NC} Running"
    else
        echo -e "Level 2: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 3
    if kubectl get pods 2>/dev/null | grep -q level3; then
        echo -e "Level 3: ${GREEN}●${NC} Running"
    else
        echo -e "Level 3: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 4
    if vagrant status 2>/dev/null | grep -q running; then
        echo -e "Level 4: ${GREEN}●${NC} Running"
    else
        echo -e "Level 4: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 5
    if docker ps | grep -q level5; then
        echo -e "Level 5: ${GREEN}●${NC} Running"
    else
        echo -e "Level 5: ${RED}●${NC} Stopped"
    fi
    
    # Check Level 6
    if docker ps | grep -q localstack; then
        echo -e "Level 6: ${GREEN}●${NC} Running"
    else
        echo -e "Level 6: ${RED}●${NC} Stopped"
    fi
    
    echo
    echo -e "${BLUE}Access URLs:${NC}"
    echo "  Level 0: http://localhost:8000"
    echo "  Level 1: http://localhost:3001"
    echo "  Level 2: http://localhost:3002"
    echo "  Level 3: $(minikube service level3-service --url 2>/dev/null || echo 'Not running')"
    echo "  Level 4: http://localhost:3004"
    echo "  Level 5: http://localhost:3005"
    echo "  Level 6: http://localhost:3006"
    echo "  Monitoring: http://localhost:3000 (Grafana)"
}

# Main loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        [0-6])
            start_level $choice
            ;;
        a)
            start_level all
            ;;
        s)
            stop_level all
            ;;
        m)
            cd monitoring
            docker-compose up -d
            cd ..
            echo -e "${GREEN}Monitoring started at http://localhost:3000${NC}"
            ;;
        t)
            show_status
            ;;
        l)
            echo "Select level for logs (0-6): "
            read -r level
            case $level in
                1) docker logs -f level-1-app ;;
                2) cd level-2-compose && docker-compose logs -f && cd .. ;;
                3) kubectl logs -f deployment/level3-app ;;
                *) echo "Logs not available for this level" ;;
            esac
            ;;
        q)
            echo -e "${YELLOW}Shutting down...${NC}"
            stop_level all
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            sleep 2
            ;;
    esac
    
    echo
    echo "Press Enter to continue..."
    read
done
EOF
    
    chmod +x control.sh
    show_success "Master control script created"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================
main() {
    show_banner
    
    echo -e "${CYAN}Starting VM Abstraction Lab Setup...${NC}"
    echo
    
    # Check prerequisites
    check_prerequisites
    
    # Create project structure
    create_project_structure
    
    # Setup each level
    setup_level_0_process
    setup_level_1_container
    setup_level_2_compose
    setup_level_3_kubernetes
    setup_level_4_vm
    setup_level_5_nested
    setup_level_6_cloud
    
    # Setup monitoring
    setup_monitoring
    
    # Create master control
    create_master_control
    
    # Final summary
    echo
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ VM ABSTRACTION LAB SETUP COMPLETE!${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${YELLOW}Project Location:${NC} $(pwd)"
    echo
    echo -e "${BLUE}Quick Start:${NC}"
    echo "  1. cd $PROJECT_NAME"
    echo "  2. ./control.sh"
    echo
    echo -e "${BLUE}Abstraction Levels:${NC}"
    echo "  Level 0: Basic Process - Direct OS execution"
    echo "  Level 1: Container - Docker isolation"
    echo "  Level 2: Compose - Multi-container orchestration"
    echo "  Level 3: Kubernetes - Enterprise orchestration"
    echo "  Level 4: VMs - Full OS virtualization"
    echo "  Level 5: Nested - VMs in containers"
    echo "  Level 6: Cloud - AWS simulation"
    echo
    echo -e "${BLUE}Access Points:${NC}"
    echo "  Control Panel: ./control.sh"
    echo "  Monitoring: http://localhost:3000 (Grafana)"
    echo "  Metrics: http://localhost:9090 (Prometheus)"
    echo
    echo -e "${GREEN}User: ${CURRENT_USER}${NC}"
    echo -e "${GREEN}Timestamp: ${TIMESTAMP} UTC${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════════════════${NC}"
}

# Run main function
main "$@"