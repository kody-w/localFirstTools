#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🚀 Advanced Simulation Configuration Generator 🚀         ║${NC}"
echo -e "${BLUE}╠═══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║  Created by: kody-w                                          ║${NC}"
echo -e "${BLUE}║  Date: 2025-08-23 17:14:55                                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

# Create main directory
PROJECT_NAME="advanced-simulation-generator"
echo -e "${GREEN}➤ Creating project directory: ${PROJECT_NAME}${NC}"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Create subdirectories
echo -e "${GREEN}➤ Creating subdirectories...${NC}"
mkdir -p templates static/js static/css

# Create app.py
echo -e "${GREEN}➤ Creating app.py...${NC}"
cat > app.py << 'EOF'
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
EOF

# Create templates/index.html
echo -e "${GREEN}➤ Creating templates/index.html...${NC}"
cat > templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Simulation Configuration Generator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Advanced Simulation Configuration Generator</h1>
            <p class="subtitle">Configure and deploy Docker-based simulations with ease</p>
            <div class="user-info">
                <span>👤 User: kody-w</span>
                <span>📅 Date: <span id="current-date"></span></span>
            </div>
        </header>

        <main>
            <form id="config-form">
                <!-- Step 1: Repositories -->
                <section class="config-section" id="step-1">
                    <h2>📦 Step 1: GitHub Repositories</h2>
                    <div class="form-group">
                        <label for="repositories">Repository URLs (one per line)</label>
                        <textarea id="repositories" rows="4" placeholder="https://github.com/user/repo1&#10;https://github.com/user/repo2"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="workspace">Workspace Directory</label>
                        <input type="text" id="workspace" value="simulations" />
                    </div>
                </section>

                <!-- Step 2: Simulation Configuration -->
                <section class="config-section" id="step-2">
                    <h2>⚙️ Step 2: Simulation Configuration</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="language">Programming Language</label>
                            <select id="language">
                                <option value="python">Python</option>
                                <option value="nodejs">Node.js</option>
                                <option value="java">Java</option>
                                <option value="custom">Custom</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="version">Language Version</label>
                            <input type="text" id="version" value="3.11" />
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="entry-point">Entry Point File</label>
                        <input type="text" id="entry-point" value="main.py" />
                    </div>
                    
                    <div class="form-group">
                        <label for="system-deps">System Dependencies (comma-separated)</label>
                        <input type="text" id="system-deps" placeholder="gcc, curl, git" />
                    </div>
                    
                    <div class="form-group">
                        <label for="pip-packages">Additional Packages (comma-separated)</label>
                        <input type="text" id="pip-packages" placeholder="numpy, pandas, matplotlib" />
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" id="mount-source" checked>
                            Mount source code (for development)
                        </label>
                        <label>
                            <input type="checkbox" id="config-files">
                            Generate configuration files
                        </label>
                    </div>
                    
                    <div class="form-group">
                        <label>Environment Variables</label>
                        <div id="env-vars">
                            <div class="env-var-row">
                                <input type="text" placeholder="KEY" class="env-key">
                                <input type="text" placeholder="VALUE" class="env-value">
                                <button type="button" class="btn-remove" onclick="removeEnvVar(this)">×</button>
                            </div>
                        </div>
                        <button type="button" class="btn-secondary" onclick="addEnvVar()">+ Add Variable</button>
                    </div>
                </section>

                <!-- Step 3: Docker Configuration -->
                <section class="config-section" id="step-3">
                    <h2>🐳 Step 3: Docker Configuration</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="restart-policy">Restart Policy</label>
                            <select id="restart-policy">
                                <option value="unless-stopped">Unless Stopped</option>
                                <option value="always">Always</option>
                                <option value="on-failure">On Failure</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="network-mode">Network Mode</label>
                            <select id="network-mode">
                                <option value="">Bridge (default)</option>
                                <option value="host">Host</option>
                                <option value="none">None</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" id="build-cache" checked>
                            Use build cache
                        </label>
                        <label>
                            <input type="checkbox" id="auto-start" checked>
                            Auto-start containers
                        </label>
                        <label>
                            <input type="checkbox" id="expose-ports">
                            Expose ports
                        </label>
                    </div>
                    
                    <div class="form-group" id="ports-group" style="display: none;">
                        <label>Port Mappings</label>
                        <div id="ports">
                            <div class="port-row">
                                <input type="text" placeholder="8080:80" class="port-mapping">
                                <button type="button" class="btn-remove" onclick="removePort(this)">×</button>
                            </div>
                        </div>
                        <button type="button" class="btn-secondary" onclick="addPort()">+ Add Port</button>
                    </div>
                </section>

                <!-- Step 4: Resources -->
                <section class="config-section" id="step-4">
                    <h2>💪 Step 4: Resource Configuration</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="memory-limit">Memory Limit</label>
                            <input type="text" id="memory-limit" placeholder="512m, 2g, etc." />
                        </div>
                        <div class="form-group">
                            <label for="cpu-limit">CPU Limit</label>
                            <input type="text" id="cpu-limit" placeholder="0.5, 1, 2, etc." />
                        </div>
                    </div>
                    
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" id="gpu-enabled">
                            Enable GPU support (NVIDIA)
                        </label>
                    </div>
                </section>

                <!-- Step 5: Monitoring -->
                <section class="config-section" id="step-5">
                    <h2>📊 Step 5: Monitoring & Logging</h2>
                    <div class="checkbox-group">
                        <label>
                            <input type="checkbox" id="monitoring-enabled">
                            Enable monitoring
                        </label>
                        <label>
                            <input type="checkbox" id="logging">
                            Enable logging
                        </label>
                        <label>
                            <input type="checkbox" id="prometheus">
                            Setup Prometheus
                        </label>
                        <label>
                            <input type="checkbox" id="grafana">
                            Setup Grafana
                        </label>
                    </div>
                </section>

                <!-- Action Buttons -->
                <div class="action-buttons">
                    <button type="button" class="btn-primary" onclick="generateScript()">
                        🚀 Generate Script
                    </button>
                    <button type="button" class="btn-secondary" onclick="resetForm()">
                        🔄 Reset
                    </button>
                </div>
            </form>

            <!-- Output Section -->
            <section id="output-section" style="display: none;">
                <h2>📝 Generated Bash Script</h2>
                <div class="output-actions">
                    <button class="btn-secondary" onclick="copyScript()">📋 Copy</button>
                    <button class="btn-primary" onclick="downloadScript()">💾 Download</button>
                    <button class="btn-secondary" onclick="newConfiguration()">🆕 New Configuration</button>
                </div>
                <pre id="script-output"></pre>
            </section>
        </main>

        <footer>
            <p>Created with ❤️ by kody-w | Advanced Simulation Generator v2.0</p>
        </footer>
    </div>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
EOF

# Create static/css/style.css
echo -e "${GREEN}➤ Creating static/css/style.css...${NC}"
cat > static/css/style.css << 'EOF'
:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --dark: #1f2937;
    --light: #f9fafb;
    --border: #e5e7eb;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: var(--dark);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: white;
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    text-align: center;
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.subtitle {
    color: #6b7280;
    font-size: 1.125rem;
    margin-bottom: 16px;
}

.user-info {
    display: flex;
    justify-content: center;
    gap: 24px;
    color: #6b7280;
    font-size: 0.875rem;
}

main {
    background: white;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.config-section {
    margin-bottom: 32px;
    padding-bottom: 32px;
    border-bottom: 1px solid var(--border);
}

.config-section:last-of-type {
    border-bottom: none;
}

.config-section h2 {
    color: var(--dark);
    margin-bottom: 24px;
    font-size: 1.5rem;
    font-weight: 600;
}

.form-group {
    margin-bottom: 20px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--dark);
    font-size: 0.875rem;
}

input[type="text"],
input[type="number"],
select,
textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s;
    font-family: inherit;
}

input[type="text"]:focus,
input[type="number"]:focus,
select:focus,
textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

textarea {
    resize: vertical;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.875rem;
}

.checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 16px 0;
}

.checkbox-group label {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-weight: 400;
}

.checkbox-group input[type="checkbox"] {
    margin-right: 8px;
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.env-var-row,
.port-row {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}

.env-var-row input {
    flex: 1;
}

.env-key {
    max-width: 200px;
}

.btn-remove {
    background: var(--danger);
    color: white;
    border: none;
    border-radius: 4px;
    width: 32px;
    height: 38px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: background 0.3s;
}

.btn-remove:hover {
    background: #dc2626;
}

.btn-primary,
.btn-secondary {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.btn-secondary {
    background: var(--light);
    color: var(--dark);
    border: 1px solid var(--border);
}

.btn-secondary:hover {
    background: #f3f4f6;
}

.action-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 32px;
}

#output-section {
    margin-top: 32px;
    padding-top: 32px;
    border-top: 2px solid var(--border);
}

.output-actions {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}

#script-output {
    background: #1e1e1e;
    color: #e0e0e0;
    padding: 24px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.875rem;
    line-height: 1.6;
    max-height: 600px;
    overflow-y: auto;
}

footer {
    text-align: center;
    color: white;
    margin-top: 32px;
    padding: 20px;
}

@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .checkbox-group {
        flex-direction: column;
    }
    
    .action-buttons {
        flex-direction: column;
    }
}
EOF

# Create static/js/app.js
echo -e "${GREEN}➤ Creating static/js/app.js...${NC}"
cat > static/js/app.js << 'EOF'
// Initialize date
document.getElementById('current-date').textContent = new Date().toLocaleString();

// Configuration object to store all settings
let configuration = {};

// Handle expose ports checkbox
document.getElementById('expose-ports').addEventListener('change', function() {
    document.getElementById('ports-group').style.display = this.checked ? 'block' : 'none';
});

// Add environment variable row
function addEnvVar() {
    const container = document.getElementById('env-vars');
    const row = document.createElement('div');
    row.className = 'env-var-row';
    row.innerHTML = `
        <input type="text" placeholder="KEY" class="env-key">
        <input type="text" placeholder="VALUE" class="env-value">
        <button type="button" class="btn-remove" onclick="removeEnvVar(this)">×</button>
    `;
    container.appendChild(row);
}

// Remove environment variable row
function removeEnvVar(button) {
    button.parentElement.remove();
}

// Add port mapping row
function addPort() {
    const container = document.getElementById('ports');
    const row = document.createElement('div');
    row.className = 'port-row';
    row.innerHTML = `
        <input type="text" placeholder="8080:80" class="port-mapping">
        <button type="button" class="btn-remove" onclick="removePort(this)">×</button>
    `;
    container.appendChild(row);
}

// Remove port mapping row
function removePort(button) {
    button.parentElement.remove();
}

// Collect all configuration data
function collectConfiguration() {
    const config = {
        user: 'kody-w',
        repositories: document.getElementById('repositories').value.split('\n').filter(r => r.trim()),
        workspace: document.getElementById('workspace').value,
        simulation: {
            language: document.getElementById('language').value,
            python_version: document.getElementById('language').value === 'python' ? document.getElementById('version').value : null,
            node_version: document.getElementById('language').value === 'nodejs' ? document.getElementById('version').value : null,
            java_version: document.getElementById('language').value === 'java' ? document.getElementById('version').value : null,
            entry_point: document.getElementById('entry-point').value,
            system_deps: document.getElementById('system-deps').value.split(',').map(d => d.trim()).filter(d => d),
            pip_packages: document.getElementById('pip-packages').value.split(',').map(p => p.trim()).filter(p => p),
            mount_source: document.getElementById('mount-source').checked,
            config_files: document.getElementById('config-files').checked,
            env_vars: {}
        },
        docker: {
            restart_policy: document.getElementById('restart-policy').value,
            network_mode: document.getElementById('network-mode').value,
            build_cache: document.getElementById('build-cache').checked,
            auto_start: document.getElementById('auto-start').checked,
            expose_ports: document.getElementById('expose-ports').checked,
            ports: []
        },
        resources: {
            memory_limit: document.getElementById('memory-limit').value,
            cpu_limit: document.getElementById('cpu-limit').value,
            gpu_enabled: document.getElementById('gpu-enabled').checked
        },
        monitoring: {
            enabled: document.getElementById('monitoring-enabled').checked,
            logging: document.getElementById('logging').checked,
            prometheus: document.getElementById('prometheus').checked,
            grafana: document.getElementById('grafana').checked
        }
    };
    
    // Collect environment variables
    document.querySelectorAll('.env-var-row').forEach(row => {
        const key = row.querySelector('.env-key').value.trim();
        const value = row.querySelector('.env-value').value.trim();
        if (key) {
            config.simulation.env_vars[key] = value;
        }
    });
    
    // Collect ports
    if (config.docker.expose_ports) {
        document.querySelectorAll('.port-mapping').forEach(input => {
            const port = input.value.trim();
            if (port) {
                config.docker.ports.push(port);
            }
        });
    }
    
    return config;
}

// Generate script
async function generateScript() {
    configuration = collectConfiguration();
    
    if (configuration.repositories.length === 0) {
        alert('Please enter at least one repository URL');
        return;
    }
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(configuration)
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('script-output').textContent = data.script;
            document.getElementById('output-section').style.display = 'block';
            document.getElementById('output-section').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        alert('Error generating script: ' + error.message);
    }
}

// Copy script to clipboard
function copyScript() {
    const scriptText = document.getElementById('script-output').textContent;
    navigator.clipboard.writeText(scriptText).then(() => {
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = '✅ Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    });
}

// Download script
async function downloadScript() {
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(configuration)
        });
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `simulation_setup_${new Date().getTime()}.sh`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        alert('Error downloading script: ' + error.message);
    }
}

// Reset form
function resetForm() {
    if (confirm('Are you sure you want to reset all configurations?')) {
        document.getElementById('config-form').reset();
        document.getElementById('output-section').style.display = 'none';
        
        // Reset dynamic fields
        document.getElementById('env-vars').innerHTML = `
            <div class="env-var-row">
                <input type="text" placeholder="KEY" class="env-key">
                <input type="text" placeholder="VALUE" class="env-value">
                <button type="button" class="btn-remove" onclick="removeEnvVar(this)">×</button>
            </div>
        `;
        
        document.getElementById('ports').innerHTML = `
            <div class="port-row">
                <input type="text" placeholder="8080:80" class="port-mapping">
                <button type="button" class="btn-remove" onclick="removePort(this)">×</button>
            </div>
        `;
    }
}

// New configuration
function newConfiguration() {
    resetForm();
    window.scrollTo(0, 0);
}

// Handle language change
document.getElementById('language').addEventListener('change', function() {
    const versionInput = document.getElementById('version');
    const entryPointInput = document.getElementById('entry-point');
    
    switch(this.value) {
        case 'python':
            versionInput.value = '3.11';
            entryPointInput.value = 'main.py';
            break;
        case 'nodejs':
            versionInput.value = '18';
            entryPointInput.value = 'index.js';
            break;
        case 'java':
            versionInput.value = '17';
            entryPointInput.value = 'Main';
            break;
        case 'custom':
            versionInput.value = 'latest';
            entryPointInput.value = 'run.sh';
            break;
    }
});
EOF

# Create requirements.txt
echo -e "${GREEN}➤ Creating requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
Flask==3.0.0
gunicorn==21.2.0
EOF

# Create Dockerfile
echo -e "${GREEN}➤ Creating Dockerfile...${NC}"
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "app:app"]
EOF

# Create docker-compose.yml
echo -e "${GREEN}➤ Creating docker-compose.yml...${NC}"
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    container_name: advanced-simulation-generator
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=development
      - PYTHONUNBUFFERED=1
    volumes:
      - ./:/app
      - ./generated_scripts:/app/generated_scripts
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - simgen-network

networks:
  simgen-network:
    driver: bridge

volumes:
  generated_scripts:
EOF

# Create README.md
echo -e "${GREEN}➤ Creating README.md...${NC}"
cat > README.md << 'EOF'
# 🚀 Advanced Simulation Configuration Generator

A powerful web application for generating customized Docker deployment scripts for simulation repositories.

## Features

- 📦 **Multi-Repository Support**: Process multiple GitHub repositories simultaneously
- 🔧 **Language Support**: Python, Node.js, Java, and custom configurations
- 🐳 **Docker Optimization**: Advanced Docker and docker-compose configurations
- 💪 **Resource Management**: CPU, memory, and GPU allocation
- 📊 **Monitoring Integration**: Prometheus and Grafana support
- 🎛️ **Flexible Configuration**: Environment variables, ports, volumes, and more
- 📝 **Script Generation**: Export ready-to-run bash scripts
- 💾 **Download Support**: Save configurations for later use

## Quick Start

```bash
# Run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8080