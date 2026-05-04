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
