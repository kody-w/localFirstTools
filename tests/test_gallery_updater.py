import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add scripts directory to path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/gallery')))

import vibe_gallery_updater

@pytest.fixture
def mock_fs(tmp_path):
    """Create a mock file system with some HTML files"""
    # Create root directory structure
    apps_dir = tmp_path / "apps"
    apps_dir.mkdir()
    
    # Create a sample HTML file in root
    root_html = tmp_path / "root_app.html"
    root_html.write_text("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Root App</title>
        <meta name="description" content="A root level application">
    </head>
    <body>
        <canvas id="game"></canvas>
        <script>console.log('game loop');</script>
    </body>
    </html>
    """, encoding="utf-8")
    
    # Create a sample HTML file in apps/
    app_html = apps_dir / "game_app.html"
    app_html.write_text("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Game App</title>
        <meta name="description" content="A game application">
    </head>
    <body>
        <script>
            // 3d game logic
            const scene = new THREE.Scene();
        </script>
    </body>
    </html>
    """, encoding="utf-8")
    
    return tmp_path

def test_extract_metadata_from_html(mock_fs):
    """Test metadata extraction from HTML content"""
    file_path = mock_fs / "root_app.html"
    metadata = vibe_gallery_updater.extract_metadata_from_html(file_path)
    
    assert metadata is not None
    assert metadata["title"] == "Root App"
    assert metadata["description"] == "A root level application"
    assert "canvas" in metadata["tags"]
    assert "game" in metadata["tags"]
    assert metadata["interactionType"] == "game"

def test_categorize_app():
    """Test app categorization logic"""
    # Test game category
    metadata_game = {
        "title": "Space Shooter",
        "description": "A space shooting game",
        "tags": ["game", "canvas"],
        "interactionType": "game"
    }
    category = vibe_gallery_updater.categorize_app("apps/games/shooter.html", metadata_game)
    assert category == "games_puzzles"
    
    # Test 3D category
    metadata_3d = {
        "title": "3D World",
        "description": "A 3D world explorer",
        "tags": ["3d", "webgl"],
        "interactionType": "visual"
    }
    category = vibe_gallery_updater.categorize_app("apps/3d/world.html", metadata_3d)
    assert category == "3d_immersive"

def test_scan_directories_for_apps(mock_fs):
    """Test scanning directories for apps"""
    apps = vibe_gallery_updater.scan_directories_for_apps(mock_fs)
    
    # Check if apps were found and categorized correctly
    # root_app.html has 'game' tag -> games_puzzles
    # game_app.html has '3d' tag -> 3d_immersive
    
    found_root = False
    found_game = False
    
    for category, app_list in apps.items():
        for app in app_list:
            if app["filename"] == "root_app.html":
                found_root = True
                assert category == "games_puzzles"
            elif app["filename"] == "game_app.html":
                found_game = True
                assert category == "3d_immersive"
                
    assert found_root
    assert found_game

def test_update_vibe_gallery_config(mock_fs):
    """Test updating the JSON config file"""
    # Run the updater
    config_path = vibe_gallery_updater.update_vibe_gallery_config(mock_fs)
    
    assert config_path.exists()
    
    # Verify config content
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    assert "vibeGallery" in config
    assert "categories" in config["vibeGallery"]
    
    categories = config["vibeGallery"]["categories"]
    
    # Check for our apps
    games_apps = categories.get("games_puzzles", {}).get("apps", [])
    immersive_apps = categories.get("3d_immersive", {}).get("apps", [])
    
    assert any(app["filename"] == "root_app.html" for app in games_apps)
    assert any(app["filename"] == "game_app.html" for app in immersive_apps)

def test_version_grouping(mock_fs):
    """Test that versioned files are grouped together"""
    # Create a main file and a copy
    (mock_fs / "test_tool.html").write_text("<html><title>Test Tool</title></html>", encoding="utf-8")
    (mock_fs / "test_tool copy.html").write_text("<html><title>Test Tool Copy</title></html>", encoding="utf-8")
    
    vibe_gallery_updater.update_vibe_gallery_config(mock_fs)
    
    with open(mock_fs / "vibe_gallery_config.json", 'r') as f:
        config = json.load(f)
        
    # Find the category containing Test Tool (likely experimental_ai as fallback)
    found = False
    for cat in config["vibeGallery"]["categories"].values():
        for app in cat.get("apps", []):
            if app["filename"] == "test_tool.html":
                found = True
                # Check if versions field exists and contains the copy
                assert "versions" in app
                assert len(app["versions"]) == 1
                assert app["versions"][0]["filename"] == "test_tool copy.html"
                
    assert found
