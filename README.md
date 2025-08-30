# 🌐 localFirstTools

> **Zero-dependency, offline-first web applications that run entirely in your browser**

A collection of 70+ self-contained HTML applications featuring games, productivity tools, AI interfaces, and utilities. Each app is a single HTML file with all code inline - no build process, no npm, no servers required. Just open and use.

## ✨ Features

- **🔌 Completely Offline** - Every app works without an internet connection
- **📦 No Dependencies** - Each app is a single HTML file with embedded CSS/JavaScript
- **🚀 Instant Launch** - No installation, compilation, or setup required
- **💾 Local Storage** - Data persists in your browser, never leaves your device
- **📱 Responsive Design** - Works on desktop, tablet, and mobile devices
- **🎨 Modern UI** - Clean, intuitive interfaces with smooth animations

## 🎮 Application Gallery

### 🎯 Games (20+ apps)
Interactive games from retro classics to modern 3D experiences:
- **3D Worlds**: `sky-realms-game.html`, `crystal-caves-world.html`, `tile-room-3d.html`
- **Classic Games**: `snake3.html`, `solitaire-tutorial-game.html`, `gameoflife.html`
- **Emulators**: `gameboy-emulator.html`, `complete-retroplay-console-ios.html`
- **Action Games**: `monster-truck-game.html`, `racing.html`, `drone-simulator.html`
- **Strategy**: `balatro.html`, `poker-trainer-continued.html`, `city-of-heroes.html`

### 🤖 AI Tools (12+ apps)
Cutting-edge AI interfaces and agent systems:
- **Agent Systems**: `agent-browser.html`, `consolidated-ai-github-agents.html`
- **AI Assistants**: `copilot-companion.html`, `wrist-ai.html`
- **Automation**: `dynamics365-email-automation.html`, `agent-deployment-prototype.html`
- **Workshops**: `claude-subagents-tutorial.html`, `mcp-registry.html`

### 📈 Productivity (15+ apps)
Tools for organization, writing, and task management:
- **Writing Tools**: `ghostwriter.html`, `omni-writer.html`, `autonomous-book-factory.html`
- **Note Taking**: `jim-rohn-journal-app.html`, `prompt-library.html`
- **Communication**: `snap-message-app.html`, `sneakernet-complete.html`
- **Task Management**: `digital-twin-keeper.html`, `severance-refiner.html`

### 💼 Business (5+ apps)
Professional tools for presentations and CRM:
- **Presentations**: `presentation-app-complete.html`, `presentation-app-final.html`
- **Sales Tools**: `ai-simulation-sales-demo.html`, `influence-mastery-app.html`
- **CRM**: `d365-solution-flattener.html`

### 🎬 Media & Entertainment (6+ apps)
Recording and multimedia applications:
- **Recording**: `dual-camera-recorder.html`, `youtube-webcam-recorder.html`
- **Music**: `drum-machine-808.html`
- **Special Effects**: `hologram-camera-recorder.html`, `bothangles-ios-fixed.html`

### 🛠️ Development Tools (6+ apps)
Tools for developers and technical users:
- **Code Tools**: `artifact-converter.html`, `mermaid-viewer.html`
- **GitHub**: `github-gallery-setup.html`, `github-sync-manager.html`
- **File Management**: `cdn-file-manager.html`, `local-browser.html`

### 📚 Education & Reference (7+ apps)
Learning tools and educational games:
- **Training**: `card-counting-trainer.html`, `teacher-learner-app.html`
- **Interactive**: `nexus.html`, `pipboy-interface.html`
- **Visualization**: `rainbow-svg-path.html`, `iframe-tunneler-7.html`

### 🧰 Utilities (7+ apps)
General purpose tools:
- **Converters**: `timezone-converter-tool.html`, `text-file-splitter.html`
- **System Tools**: `vibe-terminal.html`, `wordpress-crawler.html`
- **Demos**: `flooring-demo-complete.html`, `nexus-hub-gesture-explorer.html`

### 🧘 Health & Wellness (2+ apps)
- **Breathing**: `breathwork-guide.html`, `breathwork.html`

## 🚀 Quick Start

### Option 1: GitHub Pages (Recommended)
1. Fork this repository
2. Enable GitHub Pages in Settings → Pages
3. Visit `https://[your-username].github.io/localFirstTools2/`

### Option 2: Local File System
1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/localFirstTools2.git
   cd localFirstTools2
   ```
2. Open `index.html` in your browser
3. Or open any app directly: `apps/games/snake3.html`

### Option 3: Local Web Server
```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve

# Then visit http://localhost:8000
```

## 🏗️ Architecture

```
localFirstTools2/
├── index.html                 # Main gallery launcher
├── apps/                      # All applications by category
│   ├── games/                 # Gaming applications
│   ├── productivity/          # Productivity tools
│   ├── ai-tools/             # AI-powered applications
│   ├── business/             # Business tools
│   ├── development/          # Developer tools
│   ├── media/                # Media applications
│   ├── education/            # Educational tools
│   ├── health/               # Health apps
│   └── utilities/            # General utilities
├── data/                     # Application data
│   ├── games/                # Game configuration JSONs
│   └── config/               # App registry and settings
├── scripts/                  # Utility scripts
└── edgeAddons/              # Browser extensions
```

## 🛠️ Development

### Creating a New Application

1. **Create a single HTML file** in the appropriate `apps/` subdirectory
2. **Follow the standard template**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Your App Name</title>
       <style>
           /* All CSS must be inline */
       </style>
   </head>
   <body>
       <!-- Your HTML here -->
       <script>
           // All JavaScript must be inline
           // Use localStorage for persistence
       </script>
   </body>
   </html>
   ```

3. **Key principles**:
   - ✅ All code must be inline (HTML, CSS, JavaScript)
   - ✅ No external dependencies or CDN links
   - ✅ Use localStorage for data persistence
   - ✅ Must work completely offline
   - ✅ Responsive design for all screen sizes

### Organizing Files

Use the built-in organizer to categorize apps:
```bash
python scripts/organize_files.py --execute
```

### Building Extensions

For the Xbox controller extension:
```bash
cd edgeAddons
./create-xbox-mkb-extension.sh
```

## 🎯 Philosophy

**Local-First Principles:**
- **Privacy First**: Your data never leaves your device
- **No Tracking**: Zero analytics, cookies, or telemetry
- **Offline Forever**: Apps work without internet, always
- **No Build Process**: Edit HTML directly, refresh to see changes
- **Portable**: Copy files anywhere, they just work
- **Future Proof**: Standard HTML/CSS/JS will work for decades

## 🤝 Contributing

1. **Fork the repository**
2. **Create your app** following the template above
3. **Place it** in the appropriate `apps/` category
4. **Test thoroughly** offline and on mobile
5. **Submit a PR** with a description of your app

### Contribution Guidelines
- Keep apps self-contained in single HTML files
- No external dependencies or build requirements
- Test offline functionality
- Ensure mobile responsiveness
- Add meaningful app titles and descriptions

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with the belief that software should be:
- **Simple** - No complex toolchains
- **Permanent** - Works today, works in 10 years
- **Private** - Your data stays yours
- **Accessible** - Runs on any device with a browser

---

<div align="center">

**[Launch Gallery](index.html)** | **[View Apps](apps/)** | **[Report Issue](https://github.com/[username]/localFirstTools2/issues)**

*Made with ❤️ for the local-first movement*

</div>


# Deploy to Azure Button

Add this section to your README.md:

---

## 🚀 Quick Deploy to Azure

Deploy the complete Copilot Agent 365 infrastructure with one click:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fyour-username%2FCopilot-Agent-365%2Fmain%2Fazuredeploy.json)

### What Gets Deployed

This button will create the following Azure resources in your subscription:

- **Azure Function App** (Python 3.11) - Hosts your AI agents
- **Azure OpenAI Service** - GPT-4o model deployment
- **Azure Service Bus** - Enterprise messaging for agent collaboration
- **Azure Event Grid** - Real-time event notifications
- **Azure Storage Account** - File storage for agent memory
- **Application Insights** - Monitoring and diagnostics

### Deployment Steps

1. **Click the Deploy to Azure button** above
2. **Fill in the parameters**:
   - `Resource Group`: Create new or select existing
   - `Location`: Choose your Azure region (must support OpenAI)
   - `Function App Name`: Unique name for your bot (auto-generated)
   - `OpenAI Model`: Select GPT-4o (recommended) or GPT-4
   - `Service Bus SKU`: Standard (required for topics/subscriptions)
3. **Review and Create** - Takes 5-10 minutes to deploy
4. **Get your endpoint** from Outputs tab:
   - Copy the `functionUrlWithKey` value
   - This is your bot's API endpoint with authentication

### Post-Deployment Configuration

After deployment completes:

1. **Test Your Bot**:
```bash
curl -X POST "YOUR_FUNCTION_URL_WITH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "conversation_history": []}'
```

2. **Enable Collaborative Features**:
   - Service Bus topics are automatically created
   - Event Grid subscriptions are configured
   - Agents can immediately start collaborating

3. **Optional: Install Locally**:
```bash
# Clone the repository
git clone https://github.com/your-username/Copilot-Agent-365.git
cd Copilot-Agent-365

# Run the setup script (Windows)
./setup.ps1

# Or for Mac/Linux
bash setup.sh
```

### Custom Deployment

To deploy with custom parameters, save this as `azuredeploy.parameters.json`:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "functionAppName": {
      "value": "my-copilot-365"
    },
    "openAIModelName": {
      "value": "gpt-4o"
    },
    "serviceBusSku": {
      "value": "Standard"
    },
    "location": {
      "value": "eastus"
    }
  }
}
```

Then deploy using Azure CLI:

```bash
az group create --name CopilotAgent365RG --location eastus

az deployment group create \
  --resource-group CopilotAgent365RG \
  --template-file azuredeploy.json \
  --parameters azuredeploy.parameters.json
```

### ARM Template Location

For the Deploy to Azure button to work, ensure your `azuredeploy.json` file is in the root of your repository and accessible via:

```
https://raw.githubusercontent.com/kody-w/localfirsttools/main/azuredeploy.json
```

### Creating the Deploy Button

The Deploy to Azure button uses this URL format:

```markdown
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/ENCODED_TEMPLATE_URL)
```

To encode your template URL:
1. Take your raw GitHub URL: `https://raw.githubusercontent.com/kody-w/localfirsttools/main/azuredeploy.json`
2. URL encode it using any online encoder or:
   ```javascript
   encodeURIComponent("https://raw.githubusercontent.com/kody-w//localfirsttools/main/azuredeploy.json")
   ```
3. Replace `ENCODED_TEMPLATE_URL` with the encoded result

### Alternative Button Styles

**Large Button:**
```markdown
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/YOUR_ENCODED_URL)
```

**Small Button:**
```markdown
[![Deploy to Azure](https://azuredeploy.net/deploybutton.png)](https://portal.azure.com/#create/Microsoft.Template/uri/YOUR_ENCODED_URL)
```

**Government Cloud:**
```markdown
[![Deploy to Azure Gov](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazuregov.png)](https://portal.azure.us/#create/Microsoft.Template/uri/YOUR_ENCODED_URL)
```

### Deployment Outputs

After successful deployment, you'll receive:

- **functionAppName**: Name of your Function App
- **functionAppUrl**: Base URL of your Function App
- **functionEndpoint**: API endpoint for the bot
- **functionUrlWithKey**: Complete URL with authentication key
- **serviceBusNamespace**: Service Bus namespace for messaging
- **eventGridTopicEndpoint**: Event Grid endpoint for notifications

### Cost Estimation

Typical monthly costs (varies by usage):
- **Function App**: ~$0 (Consumption plan, first 1M requests free)
- **OpenAI**: ~$0.03 per 1K tokens (GPT-4o)
- **Service Bus**: ~$10 (Standard tier base cost)
- **Event Grid**: ~$0 (first 100K operations free)
- **Storage**: ~$1 (minimal usage)
- **Total**: ~$11-20/month for light usage

### Troubleshooting

If deployment fails:

1. **Check Region Support**: Ensure your selected region supports Azure OpenAI
2. **Verify Quotas**: Check you have sufficient quota for OpenAI deployments
3. **Review Permissions**: Ensure you have Owner or Contributor role
4. **Check Naming**: Function App names must be globally unique

### Support

- [Report Issues](https://github.com/your-username/Copilot-Agent-365/issues)
- [Documentation](https://github.com/your-username/Copilot-Agent-365/wiki)
- [Azure Status](https://status.azure.com)

---