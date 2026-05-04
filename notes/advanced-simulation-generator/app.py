from flask import Flask, render_template, request, jsonify, send_file
import json
import re
import io
from datetime import datetime

app = Flask(__name__)

def extract_repo_info(url):
    """Extract owner and repo name from GitHub URL"""
    m = re.match(r"https?://github.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url.strip())
    if m:
        return {"owner": m.group(1), "repo": m.group(2), "full_url": url.strip()}
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_script():
    config = request.json
    script = generate_bash_script(config)
    return jsonify({"script": script, "success": True})

@app.route("/download", methods=["POST"])
def download_script():
    config = request.json
    script = generate_bash_script(config)
    
    # Create in-memory file
    output = io.BytesIO()
    output.write(script.encode('utf-8'))
    output.seek(0)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"simulation_setup_{timestamp}.sh"
    
    return send_file(
        output,
        mimetype='text/x-sh',
        as_attachment=True,
        download_name=filename
    )

def generate_bash_script(config):
    """Generate a customized bash script based on user configuration"""
    repos = config.get("repositories", [])
    sim_config = config.get("simulation", {})
    docker_config = config.get("docker", {})
    resources = config.get("resources", {})
    monitoring = config.get("monitoring", {})
    
    script = "#!/bin/bash\n\n"
    script += "# Advanced Simulation Setup Script\n"
    script += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    script += f"# User: {config.get('user', 'kody-w')}\n\n"
    
    script += "set -e\n\n"
    script += "# Color definitions\n"
    script += "GREEN='\\033[0;32m'\n"
    script += "BLUE='\\033[0;34m'\n"
    script += "YELLOW='\\033[1;33m'\n"
    script += "NC='\\033[0m'\n\n"
    
    script += "echo -e \"${BLUE}Starting Advanced Simulation Setup...${NC}\\n\"\n\n"
    
    # Create workspace
    workspace = config.get("workspace", "simulations")
    script += f"# Create workspace\n"
    script += f"WORKSPACE=\"{workspace}\"\n"
    script += "mkdir -p $WORKSPACE\n"
    script += "cd $WORKSPACE\n\n"
    
    # Process each repository
    for repo_url in repos:
        repo_info = extract_repo_info(repo_url)
        if not repo_info:
            continue
            
        repo_name = repo_info["repo"]
        script += f"# ========== Repository: {repo_name} ==========\n"
        script += f"echo -e \"${{GREEN}}Processing {repo_name}...${{NC}}\"\n\n"
        
        # Clone repository
        script += f"if [ ! -d \"{repo_name}\" ]; then\n"
        script += f"    git clone {repo_info['full_url']} {repo_name}\n"
        script += f"else\n"
        script += f"    echo \"Repository {repo_name} already exists, pulling latest changes...\"\n"
        script += f"    cd {repo_name} && git pull && cd ..\n"
        script += f"fi\n\n"
        
        script += f"cd {repo_name}\n\n"
        
        # Generate Dockerfile based on language
        language = sim_config.get("language", "python")
        script += generate_dockerfile_section(language, sim_config, docker_config, resources)
        
        # Generate docker-compose.yml
        script += generate_docker_compose_section(repo_name, sim_config, docker_config, resources, monitoring)
        
        # Generate configuration files
        if sim_config.get("config_files"):
            script += generate_config_files_section(sim_config)
        
        # Build and run
        script += "# Build and run containers\n"
        if docker_config.get("build_cache", True):
            script += "docker-compose build\n"
        else:
            script += "docker-compose build --no-cache\n"
        
        if docker_config.get("auto_start", True):
            script += "docker-compose up -d\n"
            script += "echo -e \"${GREEN}✓ Container started${NC}\"\n"
        
        script += "\ncd ..\n\n"
    
    # Add monitoring setup if enabled
    if monitoring.get("enabled"):
        script += generate_monitoring_section(monitoring)
    
    script += "echo -e \"\\n${BLUE}═══════════════════════════════════════${NC}\"\n"
    script += "echo -e \"${GREEN}✓ All simulations have been set up!${NC}\"\n"
    script += "echo -e \"${BLUE}═══════════════════════════════════════${NC}\\n\"\n"
    
    # Add helper commands
    script += generate_helper_commands_section(workspace)
    
    return script

def generate_dockerfile_section(language, sim_config, docker_config, resources):
    """Generate Dockerfile content based on language and configuration"""
    section = "# Create Dockerfile\n"
    section += "cat > Dockerfile << 'DOCKERFILE_EOF'\n"
    
    if language == "python":
        python_version = sim_config.get("python_version", "3.11")
        section += f"FROM python:{python_version}-slim\n\n"
        section += "WORKDIR /app\n\n"
        
        # System dependencies
        if sim_config.get("system_deps"):
            section += "# Install system dependencies\n"
            section += "RUN apt-get update && apt-get install -y \\\n"
            for dep in sim_config.get("system_deps", []):
                section += f"    {dep} \\\n"
            section += "    && rm -rf /var/lib/apt/lists/*\n\n"
        
        # Python dependencies
        section += "# Install Python dependencies\n"
        section += "COPY requirements.txt .\n"
        section += "RUN pip install --no-cache-dir -r requirements.txt\n\n"
        
        # Additional pip packages
        if sim_config.get("pip_packages"):
            section += "# Install additional packages\n"
            packages = " ".join(sim_config.get("pip_packages", []))
            section += f"RUN pip install {packages}\n\n"
        
        # Copy application
        section += "# Copy application\n"
        section += "COPY . .\n\n"
        
        # Environment variables
        if sim_config.get("env_vars"):
            section += "# Set environment variables\n"
            for key, value in sim_config.get("env_vars", {}).items():
                section += f"ENV {key}={value}\n"
            section += "\n"
        
        # Entry point
        entry_point = sim_config.get("entry_point", "main.py")
        section += f"CMD [\"python\", \"{entry_point}\"]\n"
        
    elif language == "nodejs":
        node_version = sim_config.get("node_version", "18")
        section += f"FROM node:{node_version}-alpine\n\n"
        section += "WORKDIR /app\n\n"
        section += "COPY package*.json ./\n"
        section += "RUN npm ci --only=production\n"
        section += "COPY . .\n"
        entry_point = sim_config.get("entry_point", "index.js")
        section += f"CMD [\"node\", \"{entry_point}\"]\n"
        
    elif language == "java":
        java_version = sim_config.get("java_version", "17")
        section += f"FROM openjdk:{java_version}-slim\n\n"
        section += "WORKDIR /app\n"
        section += "COPY . .\n"
        section += "RUN javac *.java\n"
        entry_point = sim_config.get("entry_point", "Main")
        section += f"CMD [\"java\", \"{entry_point}\"]\n"
        
    elif language == "custom":
        section += sim_config.get("custom_dockerfile", "FROM ubuntu:22.04\nWORKDIR /app\nCOPY . .\n")
    
    section += "DOCKERFILE_EOF\n\n"
    return section

def generate_docker_compose_section(repo_name, sim_config, docker_config, resources, monitoring):
    """Generate docker-compose.yml content"""
    section = "# Create docker-compose.yml\n"
    section += "cat > docker-compose.yml << 'COMPOSE_EOF'\n"
    section += "version: '3.8'\n\n"
    section += "services:\n"
    section += f"  {repo_name}:\n"
    section += "    build: .\n"
    section += f"    container_name: {repo_name}-simulation\n"
    
    # Resources
    if resources.get("memory_limit"):
        section += f"    mem_limit: {resources['memory_limit']}\n"
    if resources.get("cpu_limit"):
        section += f"    cpus: '{resources['cpu_limit']}'\n"
    
    # GPU support
    if resources.get("gpu_enabled"):
        section += "    deploy:\n"
        section += "      resources:\n"
        section += "        reservations:\n"
        section += "          devices:\n"
        section += "            - driver: nvidia\n"
        section += "              count: all\n"
        section += "              capabilities: [gpu]\n"
    
    # Volumes
    section += "    volumes:\n"
    section += "      - ./data:/app/data\n"
    section += "      - ./logs:/app/logs\n"
    if sim_config.get("mount_source"):
        section += "      - ./:/app\n"
    
    # Environment
    section += "    environment:\n"
    section += "      - PYTHONUNBUFFERED=1\n"
    for key, value in sim_config.get("env_vars", {}).items():
        section += f"      - {key}={value}\n"
    
    # Networks
    if docker_config.get("network_mode"):
        section += f"    network_mode: {docker_config['network_mode']}\n"
    else:
        section += "    networks:\n"
        section += "      - simulation-network\n"
    
    # Restart policy
    restart_policy = docker_config.get("restart_policy", "unless-stopped")
    section += f"    restart: {restart_policy}\n"
    
    # Ports
    if docker_config.get("expose_ports"):
        section += "    ports:\n"
        for port in docker_config.get("ports", []):
            section += f"      - \"{port}\"\n"
    
    # Logging
    if monitoring.get("logging"):
        section += "    logging:\n"
        section += "      driver: json-file\n"
        section += "      options:\n"
        section += "        max-size: \"10m\"\n"
        section += "        max-file: \"3\"\n"
    
    # Networks definition
    if not docker_config.get("network_mode"):
        section += "\nnetworks:\n"
        section += "  simulation-network:\n"
        section += "    driver: bridge\n"
    
    # Volumes definition
    section += "\nvolumes:\n"
    section += "  data:\n"
    section += "  logs:\n"
    
    section += "COMPOSE_EOF\n\n"
    return section

def generate_config_files_section(sim_config):
    """Generate additional configuration files"""
    section = "# Create configuration files\n"
    
    # Create config directory
    section += "mkdir -p config\n\n"
    
    # Create simulation config
    section += "cat > config/simulation.json << 'CONFIG_EOF'\n"
    config_data = {
        "simulation": {
            "iterations": sim_config.get("iterations", 1000),
            "time_step": sim_config.get("time_step", 0.01),
            "output_frequency": sim_config.get("output_frequency", 100),
            "seed": sim_config.get("seed", 42)
        }
    }
    section += json.dumps(config_data, indent=2)
    section += "\nCONFIG_EOF\n\n"
    
    return section

def generate_monitoring_section(monitoring):
    """Generate monitoring setup"""
    section = "\n# ========== Monitoring Setup ==========\n"
    section += "echo -e \"${BLUE}Setting up monitoring...${NC}\"\n\n"
    
    if monitoring.get("prometheus"):
        section += "# Prometheus configuration\n"
        section += "docker run -d \\\n"
        section += "  --name prometheus \\\n"
        section += "  -p 9090:9090 \\\n"
        section += "  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \\\n"
        section += "  prom/prometheus\n\n"
    
    if monitoring.get("grafana"):
        section += "# Grafana configuration\n"
        section += "docker run -d \\\n"
        section += "  --name grafana \\\n"
        section += "  -p 3000:3000 \\\n"
        section += "  grafana/grafana\n\n"
    
    return section

def generate_helper_commands_section(workspace):
    """Generate helper commands section"""
    section = "\n# ========== Helper Commands ==========\n"
    section += "echo -e \"${YELLOW}Useful commands:${NC}\"\n"
    section += f"echo \"  View logs:         docker-compose logs -f\"\n"
    section += f"echo \"  Stop all:          cd {workspace} && docker-compose down\"\n"
    section += f"echo \"  Restart:           cd {workspace} && docker-compose restart\"\n"
    section += f"echo \"  View status:       docker ps\"\n"
    section += f"echo \"  Clean up:          docker system prune -a\"\n\n"
    return section

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
