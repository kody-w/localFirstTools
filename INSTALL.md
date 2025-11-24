# Install

## Downloads

### Release Builds

Download pre-built extension packages from the [releases page](https://github.com/kody-w/localFirstTools/releases):

- **Chrome Extension ZIP**: Ready-to-install unpacked extension
- **Meta Analysis JSON**: Ecosystem analytics data

### Development Builds

Download pre-built artifacts of main from [GitHub Actions](https://github.com/kody-w/localFirstTools/actions):

- **local-first-tools-extension.zip** - Latest build from main branch
- **build-report.md** - Build statistics and details

To download:

1. Go to the [Build workflow](https://github.com/kody-w/localFirstTools/actions/workflows/build-extension.yml)
2. Click on the latest successful run
3. Scroll down to "Artifacts" section
4. Download `local-first-tools-extension.zip`

---

## Installation

### Chrome

1. Download the extension ZIP file
2. Extract to a permanent location:
   ```
   ~/Documents/local-first-tools-extension/
   ```
3. Open Chrome and navigate to `chrome://extensions/`
4. Enable **Developer mode** (toggle in top-right corner)
5. Click **Load unpacked**
6. Select the extracted folder containing `manifest.json`

The extension will appear in your toolbar. Click the puzzle piece icon to access all 180+ applications.

### Microsoft Edge

1. Download the extension ZIP file
2. Extract to a permanent location
3. Open Edge and navigate to `edge://extensions/`
4. Enable **Developer mode** (toggle in left sidebar)
5. Click **Load unpacked**
6. Select the extracted folder containing `manifest.json`

### Brave Browser

1. Download the extension ZIP file
2. Extract to a permanent location
3. Open Brave and navigate to `brave://extensions/`
4. Enable **Developer mode** (toggle in top-right corner)
5. Click **Load unpacked**
6. Select the extracted folder containing `manifest.json`

### Opera

1. Download the extension ZIP file
2. Extract to a permanent location
3. Open Opera and navigate to `opera://extensions/`
4. Enable **Developer mode**
5. Click **Load unpacked**
6. Select the extracted folder containing `manifest.json`

> **Note:** Firefox uses a different extension format and is not supported.

---

## Testing Pre-Release Builds

Pre-release builds are available from pull request workflows. These builds are not included in official releases but can be tested manually:

1. Go to the [Actions tab](https://github.com/kody-w/localFirstTools/actions)
2. Find the workflow run for the PR you want to test
3. Download the extension artifact
4. Follow the standard installation steps above

### Updating Extensions

To update to a newer version:

1. Download the latest extension ZIP
2. Extract to the same location (overwrite existing files)
3. Go to `chrome://extensions/`
4. Click the refresh icon on the Local First Tools card

Or for a clean update:

1. Remove the existing extension
2. Download and extract the new version
3. Load the unpacked extension again

---

## Troubleshooting

### Extension disappeared after browser restart

**Solution:** The extension folder was moved or deleted. Chrome needs continuous access to the unpacked files.

- Extract to a permanent location (Documents folder recommended)
- Do NOT delete the folder after installation
- If you need to move it, remove the extension first, then reinstall

### "This extension may have been corrupted" error

**Solution:**

1. Remove the extension
2. Re-extract the ZIP file to a new location
3. Ensure you're not using a network drive or cloud-synced folder
4. Load the extension again

### Can't find "Load unpacked" button

**Solution:** Developer mode must be enabled. Toggle the switch in the top-right corner of the extensions page.

### Apps showing 404 errors

**Solution:** Incorrect folder structure selected.

1. Select the folder containing `manifest.json` (not a parent folder)
2. Verify the `apps/` and `data/` folders exist inside
3. Click the refresh icon on the extension card

---

## System Requirements

- **Browsers:** Chrome 88+, Edge 88+, Brave, Opera (Chromium-based)
- **Disk Space:** ~10 MB
- **Network:** None required (100% offline)
