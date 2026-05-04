# LocalFirstTools Desktop App

This directory contains the configuration to build a standalone, offline desktop application for the LocalFirstTools collection using [Tauri](https://tauri.app/).

## Why Tauri?

Tauri is a framework for building tiny, blazing fast binaries for all major desktop platforms. Developers can integrate any front-end framework that compiles to HTML, JS and CSS for building their user interface.

- **Rust-based**: Secure and performant.
- **Tiny Bundle**: Uses the OS's native web renderer (WebView2 on Windows, WebKit on macOS/Linux) instead of bundling Chrome (like Electron), resulting in much smaller file sizes.
- **Local First**: Perfect for this project's philosophy.

## Prerequisites

1.  **Install Rust**:
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2.  **Install System Dependencies** (Linux only):
    See [Tauri Setup Guide](https://tauri.app/v1/guides/getting-started/prerequisites) for Linux-specific dependencies.
    - macOS and Windows usually require no extra steps if Xcode/VS Build Tools are installed.

## How to Build

1.  **Run the Build Script**:
    We have provided a script that prepares the files and runs the build.
    ```bash
    chmod +x build_app.sh
    ./build_app.sh
    ```

    This script will:
    1.  Create a `dist` folder.
    2.  Copy all HTML tools from the root directory into `dist`.
    3.  Run `cargo tauri build` to compile the application.

2.  **Locate the App**:
    After building, your app will be located in:
    `src-tauri/target/release/bundle/`
    
    - **macOS**: `.dmg` or `.app`
    - **Windows**: `.msi` or `.exe`
    - **Linux**: `.deb` or `.AppImage`

## Development

To run the app in development mode (hot reload not applicable for static files, but useful for testing):

```bash
cd src-tauri
cargo tauri dev
```

## Icons

To customize the app icon, replace the files in `src-tauri/icons/` or use the `tauri icon` command to generate them from a source image.
