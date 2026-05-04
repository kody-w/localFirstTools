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
