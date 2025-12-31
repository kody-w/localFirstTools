#!/usr/bin/env python3
"""
NeuAI Desktop Installer
=======================
Downloads and installs NeuAI as a first-party desktop application.

Usage:
    python neuai-installer.py [--uninstall] [--update]

Or run directly from the web:
    curl -sL https://raw.githubusercontent.com/kody-w/m365-agents-for-python/main/localFirstTools/neuai-installer.py | python3

Features:
    - Downloads latest NeuAI from GitHub
    - Installs to user directory (~/.neuai/)
    - Creates command-line access ('neuai' command)
    - Creates desktop shortcut (macOS/Windows/Linux)
    - Auto-detects Python installation
    - No admin/sudo required
"""

import os
import sys
import json
import shutil
import stat
import platform
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/kody-w/m365-agents-for-python/main/localFirstTools"
APP_NAME = "NeuAI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Intelligent AI Assistant with Persistent Memory"

# Files to download
REQUIRED_FILES = [
    "neuai-cli.py",
]

OPTIONAL_FILES = [
    "neuai-test-suite.py",
]

# =============================================================================
# Utilities
# =============================================================================

def print_banner():
    """Print installer banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███╗   ██╗███████╗██╗   ██╗ █████╗ ██╗                   ║
║    ████╗  ██║██╔════╝██║   ██║██╔══██╗██║                   ║
║    ██╔██╗ ██║█████╗  ██║   ██║███████║██║                   ║
║    ██║╚██╗██║██╔══╝  ██║   ██║██╔══██║██║                   ║
║    ██║ ╚████║███████╗╚██████╔╝██║  ██║██║                   ║
║    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝                   ║
║                                                              ║
║                  DESKTOP INSTALLER                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_platform():
    """Get current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


def get_install_dir():
    """Get installation directory based on platform."""
    home = Path.home()
    plat = get_platform()

    if plat == "macos":
        return home / ".neuai"
    elif plat == "windows":
        return home / "AppData" / "Local" / "NeuAI"
    else:  # Linux
        return home / ".neuai"


def get_bin_dir():
    """Get binary/scripts directory for PATH."""
    home = Path.home()
    plat = get_platform()

    if plat == "macos":
        return home / ".local" / "bin"
    elif plat == "windows":
        return home / "AppData" / "Local" / "NeuAI" / "bin"
    else:  # Linux
        return home / ".local" / "bin"


def download_file(url: str, dest: Path) -> bool:
    """Download a file from URL to destination."""
    try:
        print(f"  📥 Downloading {dest.name}...", end=" ", flush=True)
        urllib.request.urlretrieve(url, dest)
        print("✅")
        return True
    except urllib.error.URLError as e:
        print(f"❌ ({e.reason})")
        return False
    except Exception as e:
        print(f"❌ ({e})")
        return False


def make_executable(path: Path):
    """Make a file executable."""
    try:
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass


def find_python():
    """Find Python 3 executable."""
    candidates = ["python3", "python", "py"]

    for cmd in candidates:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and "3." in result.stdout:
                return cmd
        except Exception:
            continue

    return None


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"{version.major}.{version.minor}"
    return True, f"{version.major}.{version.minor}.{version.micro}"


# =============================================================================
# Installation Functions
# =============================================================================

def install():
    """Main installation function."""
    print_banner()
    print(f"Platform: {get_platform().title()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check Python version
    ok, version = check_python_version()
    if not ok:
        print(f"\n❌ Python 3.8+ required. You have Python {version}")
        return False

    print(f"\n{'='*60}")
    print("INSTALLATION")
    print('='*60)

    install_dir = get_install_dir()
    bin_dir = get_bin_dir()

    print(f"\nInstall location: {install_dir}")
    print(f"Command location: {bin_dir}")

    # Confirm
    response = input("\nProceed with installation? [Y/n]: ").strip().lower()
    if response and response != 'y' and response != 'yes':
        print("\n❌ Installation cancelled.")
        return False

    # Create directories
    print("\n📁 Creating directories...")
    install_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(parents=True, exist_ok=True)
    (install_dir / "data").mkdir(exist_ok=True)

    # Download files
    print("\n📦 Downloading NeuAI...")

    for filename in REQUIRED_FILES:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        dest = install_dir / filename
        if not download_file(url, dest):
            print(f"\n❌ Failed to download required file: {filename}")
            return False
        make_executable(dest)

    for filename in OPTIONAL_FILES:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        dest = install_dir / filename
        download_file(url, dest)  # Optional, don't fail if missing
        make_executable(dest)

    # Create launcher script
    print("\n🚀 Creating launcher...")
    create_launcher(install_dir, bin_dir)

    # Create desktop shortcut
    print("\n🖥️  Creating desktop shortcut...")
    create_desktop_shortcut(install_dir)

    # Create version file
    version_info = {
        "version": APP_VERSION,
        "installed": datetime.now().isoformat(),
        "platform": get_platform(),
        "python": sys.version.split()[0],
        "install_dir": str(install_dir),
        "bin_dir": str(bin_dir)
    }
    with open(install_dir / "version.json", 'w') as f:
        json.dump(version_info, f, indent=2)

    # Print success message
    print("\n" + "="*60)
    print("✅ INSTALLATION COMPLETE!")
    print("="*60)

    print_post_install_instructions(bin_dir)

    return True


def create_launcher(install_dir: Path, bin_dir: Path):
    """Create platform-specific launcher script."""
    plat = get_platform()
    python_cmd = find_python() or "python3"
    main_script = install_dir / "neuai-cli.py"

    if plat == "windows":
        # Windows batch file
        launcher = bin_dir / "neuai.bat"
        content = f'''@echo off
"{python_cmd}" "{main_script}" %*
'''
        launcher.write_text(content)

        # Also create PowerShell script
        ps_launcher = bin_dir / "neuai.ps1"
        ps_content = f'''& "{python_cmd}" "{main_script}" $args
'''
        ps_launcher.write_text(ps_content)

    else:
        # Unix shell script (macOS/Linux)
        launcher = bin_dir / "neuai"
        content = f'''#!/usr/bin/env bash
exec "{python_cmd}" "{main_script}" "$@"
'''
        launcher.write_text(content)
        make_executable(launcher)

    print(f"  ✅ Created: {launcher}")


def create_desktop_shortcut(install_dir: Path):
    """Create platform-specific desktop shortcut."""
    plat = get_platform()
    python_cmd = find_python() or "python3"
    main_script = install_dir / "neuai-cli.py"

    if plat == "macos":
        create_macos_app(install_dir, python_cmd, main_script)
    elif plat == "windows":
        create_windows_shortcut(install_dir, python_cmd, main_script)
    else:
        create_linux_desktop_entry(install_dir, python_cmd, main_script)


def create_macos_app(install_dir: Path, python_cmd: str, main_script: Path):
    """Create macOS .app bundle."""
    apps_dir = Path.home() / "Applications"
    apps_dir.mkdir(exist_ok=True)

    app_path = apps_dir / "NeuAI.app"
    contents = app_path / "Contents"
    macos_dir = contents / "MacOS"
    resources = contents / "Resources"

    # Remove existing
    if app_path.exists():
        shutil.rmtree(app_path)

    # Create structure
    macos_dir.mkdir(parents=True)
    resources.mkdir(parents=True)

    # Create executable
    executable = macos_dir / "NeuAI"
    exec_content = f'''#!/bin/bash
# NeuAI Desktop Launcher

# Open Terminal with NeuAI
osascript -e 'tell application "Terminal"
    activate
    do script "{python_cmd} \\"{main_script}\\""
end tell'
'''
    executable.write_text(exec_content)
    make_executable(executable)

    # Create Info.plist
    plist = contents / "Info.plist"
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>NeuAI</string>
    <key>CFBundleIdentifier</key>
    <string>com.neuai.desktop</string>
    <key>CFBundleName</key>
    <string>NeuAI</string>
    <key>CFBundleDisplayName</key>
    <string>NeuAI</string>
    <key>CFBundleVersion</key>
    <string>{APP_VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>{APP_VERSION}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
'''
    plist.write_text(plist_content)

    # Create simple icon (text-based for now)
    create_macos_icon(resources)

    print(f"  ✅ Created: {app_path}")


def create_macos_icon(resources: Path):
    """Create a simple icon for macOS app."""
    # Create a simple script that generates the icon
    # In a real app, you'd include an actual .icns file
    icon_script = resources / "create_icon.py"
    icon_script.write_text('''# Icon placeholder
# In production, include a proper NeuAI.icns file
''')


def create_windows_shortcut(install_dir: Path, python_cmd: str, main_script: Path):
    """Create Windows desktop shortcut."""
    try:
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "NeuAI.lnk"

        # Create a VBScript to create the shortcut
        vbs_content = f'''
Set WshShell = WScript.CreateObject("WScript.Shell")
Set shortcut = WshShell.CreateShortcut("{shortcut_path}")
shortcut.TargetPath = "cmd.exe"
shortcut.Arguments = "/k {python_cmd} ""{main_script}"""
shortcut.WorkingDirectory = "{install_dir}"
shortcut.Description = "{APP_DESCRIPTION}"
shortcut.Save
'''

        vbs_path = install_dir / "create_shortcut.vbs"
        vbs_path.write_text(vbs_content)

        # Run VBScript
        subprocess.run(["cscript", "//nologo", str(vbs_path)],
                      cwd=install_dir, capture_output=True)

        # Cleanup
        vbs_path.unlink()

        print(f"  ✅ Created: {shortcut_path}")

    except Exception as e:
        print(f"  ⚠️  Could not create shortcut: {e}")
        print(f"      You can manually create a shortcut to: {main_script}")


def create_linux_desktop_entry(install_dir: Path, python_cmd: str, main_script: Path):
    """Create Linux .desktop file."""
    applications_dir = Path.home() / ".local" / "share" / "applications"
    applications_dir.mkdir(parents=True, exist_ok=True)

    desktop_file = applications_dir / "neuai.desktop"

    content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=NeuAI
Comment={APP_DESCRIPTION}
Exec={python_cmd} {main_script}
Icon=utilities-terminal
Terminal=true
Categories=Utility;Development;
Keywords=AI;Assistant;Chat;
'''

    desktop_file.write_text(content)
    make_executable(desktop_file)

    print(f"  ✅ Created: {desktop_file}")


def print_post_install_instructions(bin_dir: Path):
    """Print post-installation instructions."""
    plat = get_platform()

    print(f"\n📌 TO USE NEUAI:")
    print("-" * 40)

    if plat == "macos":
        print(f'''
Option 1: Open the app from ~/Applications/NeuAI.app

Option 2: Use the command line:

  # Add to your PATH (add to ~/.zshrc or ~/.bashrc):
  export PATH="$PATH:{bin_dir}"

  # Then run:
  neuai

Option 3: Run directly:
  python3 ~/.neuai/neuai-cli.py
''')
    elif plat == "windows":
        print(f'''
Option 1: Double-click the NeuAI shortcut on your Desktop

Option 2: Use Command Prompt or PowerShell:

  # Add to PATH via System Settings, or run:
  {bin_dir}\\neuai.bat

Option 3: Run directly:
  python %LOCALAPPDATA%\\NeuAI\\neuai-cli.py
''')
    else:  # Linux
        print(f'''
Option 1: Find NeuAI in your applications menu

Option 2: Use the command line:

  # Add to your PATH (add to ~/.bashrc):
  export PATH="$PATH:{bin_dir}"

  # Then run:
  neuai

Option 3: Run directly:
  python3 ~/.neuai/neuai-cli.py
''')

    print("\n🔑 FIRST RUN:")
    print("-" * 40)
    print("NeuAI will prompt you for Azure OpenAI credentials on first run.")
    print("Have these ready:")
    print("  • Azure OpenAI Endpoint URL")
    print("  • API Key")
    print("  • Deployment Name (e.g., gpt-4)")


# =============================================================================
# Uninstallation
# =============================================================================

def uninstall():
    """Uninstall NeuAI."""
    print_banner()
    print("UNINSTALLING NEUAI")
    print("="*60)

    install_dir = get_install_dir()
    bin_dir = get_bin_dir()
    plat = get_platform()

    items_to_remove = []

    # Check what exists
    if install_dir.exists():
        items_to_remove.append(("Installation directory", install_dir))

    launcher = bin_dir / ("neuai.bat" if plat == "windows" else "neuai")
    if launcher.exists():
        items_to_remove.append(("Launcher script", launcher))

    if plat == "macos":
        app_path = Path.home() / "Applications" / "NeuAI.app"
        if app_path.exists():
            items_to_remove.append(("macOS App", app_path))
    elif plat == "windows":
        shortcut = Path.home() / "Desktop" / "NeuAI.lnk"
        if shortcut.exists():
            items_to_remove.append(("Desktop shortcut", shortcut))
    else:
        desktop_file = Path.home() / ".local" / "share" / "applications" / "neuai.desktop"
        if desktop_file.exists():
            items_to_remove.append(("Desktop entry", desktop_file))

    if not items_to_remove:
        print("\n❌ NeuAI is not installed.")
        return False

    print("\nThe following will be removed:")
    for name, path in items_to_remove:
        print(f"  • {name}: {path}")

    # Check for user data
    data_dir = install_dir / "data"
    config_file = install_dir / "data" / "config.json" if install_dir.exists() else None
    memories_file = install_dir / "data" / "memories.json" if install_dir.exists() else None

    has_data = False
    if install_dir.exists():
        # Check for any .json files in install_dir (data)
        json_files = list(install_dir.glob("*.json"))
        has_data = len(json_files) > 0

    if has_data:
        print("\n⚠️  WARNING: This will also delete your saved credentials and memories!")

    response = input("\nAre you sure you want to uninstall? [y/N]: ").strip().lower()
    if response != 'y' and response != 'yes':
        print("\n❌ Uninstallation cancelled.")
        return False

    print("\n🗑️  Removing files...")

    for name, path in items_to_remove:
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  ✅ Removed: {path}")
        except Exception as e:
            print(f"  ⚠️  Could not remove {path}: {e}")

    print("\n✅ NeuAI has been uninstalled.")
    return True


# =============================================================================
# Update
# =============================================================================

def update():
    """Update NeuAI to latest version."""
    print_banner()
    print("UPDATING NEUAI")
    print("="*60)

    install_dir = get_install_dir()

    if not install_dir.exists():
        print("\n❌ NeuAI is not installed. Run without flags to install.")
        return False

    print(f"\nUpdating from: {GITHUB_RAW_BASE}")
    print(f"Install location: {install_dir}")

    # Backup user data
    print("\n📦 Backing up user data...")
    backup_files = ["config.json", "memories.json", "context.json"]
    backups = {}

    for filename in backup_files:
        filepath = install_dir / filename
        if filepath.exists():
            backups[filename] = filepath.read_text()
            print(f"  ✅ Backed up: {filename}")

    # Download new files
    print("\n📥 Downloading updates...")

    for filename in REQUIRED_FILES:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        dest = install_dir / filename
        if not download_file(url, dest):
            print(f"\n❌ Failed to download: {filename}")
            return False
        make_executable(dest)

    for filename in OPTIONAL_FILES:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        dest = install_dir / filename
        download_file(url, dest)
        make_executable(dest)

    # Restore user data (they should already be there, but just in case)
    print("\n📦 Verifying user data...")
    for filename, content in backups.items():
        filepath = install_dir / filename
        if not filepath.exists():
            filepath.write_text(content)
            print(f"  ✅ Restored: {filename}")

    # Update version file
    version_info = {
        "version": APP_VERSION,
        "updated": datetime.now().isoformat(),
        "platform": get_platform(),
        "python": sys.version.split()[0],
        "install_dir": str(install_dir)
    }
    with open(install_dir / "version.json", 'w') as f:
        json.dump(version_info, f, indent=2)

    print("\n✅ NeuAI has been updated!")
    return True


# =============================================================================
# Main
# =============================================================================

def main():
    """Main entry point."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    if "--uninstall" in sys.argv:
        return 0 if uninstall() else 1

    if "--update" in sys.argv:
        return 0 if update() else 1

    if "--version" in sys.argv:
        print(f"NeuAI Installer v{APP_VERSION}")
        return 0

    # Default: install
    return 0 if install() else 1


if __name__ == "__main__":
    sys.exit(main())
