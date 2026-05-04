#!/usr/bin/env python3
import os
import json
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

# Configuration
SCREENSHOT_DIR = Path("screenshots")
CONFIG_FILE = Path("vibe_gallery_config.json")
OUTPUT_HTML = Path("vibe_gallery.html")
MAX_FILES = 10  # Limit for the demo

async def take_screenshot(browser, html_file, output_path):
    """Take a high-res screenshot of an HTML file"""
    page = await browser.new_page(viewport={"width": 1280, "height": 720})
    try:
        # Use absolute path for file:// protocol
        file_url = f"file://{html_file.absolute()}"
        await page.goto(file_url, wait_until="networkidle", timeout=30000)
        # Wait a bit for animations to settle
        await asyncio.sleep(2)
        await page.screenshot(path=output_path)
        print(f"  📸 Screenshot saved: {output_path.name}")
        return True
    except Exception as e:
        print(f"  ❌ Error taking screenshot of {html_file.name}: {e}")
        return False
    finally:
        await page.close()

def extract_basic_metadata(html_file):
    """Extract title and a short description from HTML"""
    try:
        content = html_file.read_text(encoding='utf-8', errors='ignore')[:5000]
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else html_file.stem.replace('-', ' ').title()
        
        # Simple AI-like title enhancement (Heuristic)
        if "3d" in content.lower() or "three.js" in content.lower():
            vibe = "Immersive 3D Experience"
        elif "canvas" in content.lower():
            vibe = "Generative Art Piece"
        elif "game" in content.lower():
            vibe = "Interactive Game"
        else:
            vibe = "Creative Experiment"
            
        return {
            "title": title,
            "vibe": vibe,
            "filename": html_file.name,
            "path": str(html_file.relative_to(Path.cwd()))
        }
    except Exception:
        return None

async def main():
    print("🚀 Starting Supercharged Vibe Gallery Updater")
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    
    html_files = list(Path.cwd().glob("*.html"))
    # Filter out index.html and vibe_gallery.html
    html_files = [f for f in html_files if f.name not in ["index.html", "vibe_gallery.html"]]
    
    print(f"🔍 Found {len(html_files)} HTML files. Processing top {MAX_FILES}...")
    
    apps = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for i, html_file in enumerate(html_files[:MAX_FILES]):
            print(f"[{i+1}/{MAX_FILES}] Processing {html_file.name}...")
            
            screenshot_name = f"{html_file.stem}.png"
            screenshot_path = SCREENSHOT_DIR / screenshot_name
            
            success = await take_screenshot(browser, html_file, screenshot_path)
            
            metadata = extract_basic_metadata(html_file)
            if metadata:
                metadata["screenshot"] = str(screenshot_path)
                apps.append(metadata)
                
        await browser.close()

    # Generate the Gallery HTML
    generate_gallery_html(apps)
    print(f"\n✅ Gallery generated: {OUTPUT_HTML}")

def generate_gallery_html(apps):
    """Generate a beautiful, responsive CSS Grid gallery"""
    cards_html = ""
    for app in apps:
        cards_html += f"""
        <div class="card">
            <div class="card-image" style="background-image: url('{app['screenshot']}')">
                <div class="card-overlay">
                    <a href="{app['path']}" target="_blank" class="btn">Launch App</a>
                </div>
            </div>
            <div class="card-content">
                <span class="vibe-tag">{app['vibe']}</span>
                <h3>{app['title']}</h3>
                <p>{app['filename']}</p>
            </div>
        </div>
        """

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supercharged Vibe Gallery</title>
    <style>
        :root {{
            --bg: #020617;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f8fafc;
            --accent: #38bdf8;
            --tag-bg: linear-gradient(135deg, #0ea5e9, #2563eb);
        }}
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.15) 0, transparent 50%), 
                radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.15) 0, transparent 50%);
            color: var(--text);
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }}
        header {{
            text-align: center;
            margin-bottom: 4rem;
            animation: fadeInDown 1s ease-out;
        }}
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        h1 {{
            font-size: 4rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2.5rem;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 1.5rem;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255,255,255,0.1);
            display: flex;
            flex-direction: column;
        }}
        .card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border-color: rgba(56, 189, 248, 0.5);
        }}
        .card-image {{
            height: 220px;
            background-size: cover;
            background-position: center;
            position: relative;
            transition: transform 0.5s ease;
        }}
        .card:hover .card-image {{
            transform: scale(1.05);
        }}
        .card-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: all 0.3s ease;
        }}
        .card:hover .card-overlay {{
            opacity: 1;
        }}
        .btn {{
            background: var(--accent);
            color: white;
            padding: 0.8rem 2rem;
            border-radius: 9999px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.4);
            transition: all 0.2s;
        }}
        .btn:hover {{
            transform: scale(1.05);
            filter: brightness(1.1);
        }}
        .card-content {{
            padding: 2rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }}
        .vibe-tag {{
            background: var(--tag-bg);
            font-size: 0.7rem;
            padding: 0.3rem 1rem;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 800;
            width: fit-content;
            margin-bottom: 1rem;
        }}
        h3 {{
            margin: 0 0 0.75rem 0;
            font-size: 1.5rem;
            line-height: 1.2;
        }}
        p {{
            color: #94a3b8;
            font-size: 0.9rem;
            margin: 0;
            font-family: 'JetBrains Mono', monospace;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Vibe Gallery</h1>
        <p>Automated Visual Discovery of Creative Experiments</p>
    </header>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>
    """
    OUTPUT_HTML.write_text(html_template, encoding='utf-8')

if __name__ == "__main__":
    asyncio.run(main())
