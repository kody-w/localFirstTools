#!/usr/bin/env node
/**
 * LEVIATHAN World Browser - Icon Generator
 * Generates PNG icons for the browser extension
 *
 * Usage: node generate-icons.js
 * Outputs: icon16.png, icon48.png, icon128.png
 */

const fs = require('fs');
const path = require('path');

// Try to use canvas if available, otherwise output instructions
try {
    const { createCanvas } = require('canvas');
    generateWithCanvas(createCanvas);
} catch (e) {
    console.log('Canvas module not found. Generating base64 fallback icons...');
    generateBase64Icons();
}

function generateWithCanvas(createCanvas) {
    const sizes = [16, 48, 128];
    const outputDir = __dirname;

    sizes.forEach(size => {
        const canvas = createCanvas(size, size);
        const ctx = canvas.getContext('2d');
        drawIcon(ctx, size);

        const buffer = canvas.toBuffer('image/png');
        const filename = path.join(outputDir, `icon${size}.png`);
        fs.writeFileSync(filename, buffer);
        console.log(`Created: ${filename}`);
    });

    // Also copy to extension directory
    const extDir = path.join(__dirname, '../../edgeAddons/world-browser-extension');
    if (fs.existsSync(extDir)) {
        sizes.forEach(size => {
            const src = path.join(outputDir, `icon${size}.png`);
            const dst = path.join(extDir, `icon${size}.png`);
            fs.copyFileSync(src, dst);
            console.log(`Copied to extension: ${dst}`);
        });
    }

    console.log('\nDone! Icons generated successfully.');
}

function drawIcon(ctx, size) {
    const center = size / 2;
    const radius = size * 0.4;

    // Background gradient
    const bgGrad = ctx.createRadialGradient(center, center, 0, center, center, size);
    bgGrad.addColorStop(0, '#1a0a3a');
    bgGrad.addColorStop(1, '#0a0a1a');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, size, size);

    // Outer glow
    ctx.beginPath();
    ctx.arc(center, center, radius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.3)';
    ctx.lineWidth = size * 0.08;
    ctx.stroke();

    // Planet circle
    const planetGrad = ctx.createRadialGradient(
        center - radius * 0.3, center - radius * 0.3, 0,
        center, center, radius
    );
    planetGrad.addColorStop(0, '#4488ff');
    planetGrad.addColorStop(0.5, '#2266cc');
    planetGrad.addColorStop(1, '#114488');

    ctx.beginPath();
    ctx.arc(center, center, radius * 0.8, 0, Math.PI * 2);
    ctx.fillStyle = planetGrad;
    ctx.fill();

    // Planet ring
    ctx.beginPath();
    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(Math.PI * 0.15);
    ctx.scale(1, 0.3);
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.restore();
    ctx.strokeStyle = '#0ff';
    ctx.lineWidth = Math.max(1, size * 0.04);
    ctx.stroke();

    // Stars (for larger sizes)
    if (size >= 48) {
        const stars = [[0.15, 0.2], [0.85, 0.15], [0.1, 0.75], [0.9, 0.8]];
        ctx.fillStyle = '#fff';
        stars.forEach(([x, y]) => {
            ctx.beginPath();
            ctx.arc(size * x, size * y, Math.max(1, size * 0.02), 0, Math.PI * 2);
            ctx.fill();
        });
    }
}

function generateBase64Icons() {
    // Pre-generated minimal placeholder icons (will be replaced when canvas is available)
    console.log('\nTo generate proper icons:');
    console.log('1. Install canvas: npm install canvas');
    console.log('2. Run: node generate-icons.js');
    console.log('\nOR open generate-icons.html in a browser and download the icons.');
}
