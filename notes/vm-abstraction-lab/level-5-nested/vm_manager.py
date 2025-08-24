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
