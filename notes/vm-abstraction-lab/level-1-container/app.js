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
