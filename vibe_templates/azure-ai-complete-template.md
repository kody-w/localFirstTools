# Complete Azure AI Assistant Template with M365 Copilot Integration

## 🚀 Complete Enterprise Solution Overview

This template provides a full enterprise AI assistant solution with:
- **One-click Azure deployment** using ARM templates
- **Microsoft 365 Copilot integration** via Copilot Studio
- **Power Platform connectivity** for Teams and M365
- **Automated setup scripts** for Windows/Mac/Linux
- **Python 3.11 compatibility** for Azure Functions v4
- **Persistent memory system** with user isolation
- **Extensible agent architecture**
- **GitHub-based agent marketplace**

## 📁 Complete Project Structure

```
{{project_name}}/
├── deployment/                      # Azure deployment files
│   ├── azuredeploy.json            # ARM template for Azure
│   ├── azuredeploy.parameters.json # ARM parameters
│   └── MSFTAIBASMultiAgentCopilot_1_0_0_2.zip # Power Platform solution
├── function_app.py                 # Main Azure Function
├── requirements.txt                # Python dependencies  
├── host.json                       # Azure Functions config
├── local.settings.json             # Local settings (generated)
├── agents/                         # Core agent modules
│   ├── __init__.py
│   ├── basic_agent.py
│   ├── context_memory_agent.py
│   └── manage_memory_agent.py
├── agent_stacks/                   # Pre-configured agent stacks
│   ├── voice_to_crm_stack/
│   ├── email_automation_stack/
│   └── document_processing_stack/
├── utils/                          # Utility modules
│   ├── __init__.py
│   └── azure_file_storage.py
├── power_platform/                 # Power Platform integration
│   ├── flows/
│   │   └── talk_to_mac_flow.json
│   ├── copilot_studio/
│   │   └── agent_bot_config.json
│   └── README.md
├── client/                         # Web UI
│   ├── index.html                 # Complete platform UI
│   ├── styles.css
│   ├── script.js
│   └── generate_trading_card.js
├── docs/                           # Documentation
│   ├── images/
│   ├── DEPLOYMENT.md
│   ├── COPILOT_INTEGRATION.md
│   ├── AGENTS.md
│   └── API.md
├── tests/                          # Test files
├── manifest.json                   # Agent manifest
├── README.md                       # Main documentation
├── LICENSE
└── .gitignore
```

## 📝 Core Deployment Files

### 1. Complete ARM Template (azuredeploy.json)

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "functionAppName": {
      "type": "string",
      "defaultValue": "[concat('{{project_prefix}}-', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Name of the Function App (must be globally unique)"
      }
    },
    "storageAccountName": {
      "type": "string",
      "defaultValue": "[concat('st', uniqueString(resourceGroup().id))]",
      "maxLength": 24,
      "metadata": {
        "description": "Storage Account Name (3-24 characters, lowercase and numbers only)"
      }
    },
    "openAIServiceName": {
      "type": "string",
      "defaultValue": "[concat('openai-', uniqueString(resourceGroup().id))]",
      "metadata": {
        "description": "Name for the Azure OpenAI Service"
      }
    },
    "openAIModelName": {
      "type": "string",
      "defaultValue": "gpt-4o",
      "allowedValues": [
        "gpt-35-turbo",
        "gpt-4",
        "gpt-4-32k",
        "gpt-4o",
        "gpt-4o-mini"
      ],
      "metadata": {
        "description": "Azure OpenAI model to deploy"
      }
    },
    "openAISku": {
      "type": "string",
      "defaultValue": "S0",
      "allowedValues": ["S0"]
    },
    "openAIDeploymentCapacity": {
      "type": "int",
      "defaultValue": 10,
      "minValue": 1,
      "maxValue": 1000,
      "metadata": {
        "description": "Capacity in units of 1K TPM"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "eastus",
      "allowedValues": [
        "eastus",
        "eastus2",
        "northcentralus",
        "southcentralus",
        "westus",
        "westus3",
        "australiaeast",
        "canadaeast",
        "francecentral",
        "japaneast",
        "norwayeast",
        "swedencentral",
        "switzerlandnorth",
        "uksouth"
      ]
    }
  },
  "variables": {
    "hostingPlanName": "[concat(parameters('functionAppName'), '-plan')]",
    "applicationInsightsName": "[concat(parameters('functionAppName'), '-insights')]",
    "fileShareName": "{{file_share_name}}",
    "functionAppId": "[resourceId('Microsoft.Web/sites', parameters('functionAppName'))]",
    "storageAccountId": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageAccountName'))]",
    "openAIResourceId": "[resourceId('Microsoft.CognitiveServices/accounts', parameters('openAIServiceName'))]"
  },
  "resources": [
    {
      "type": "Microsoft.CognitiveServices/accounts",
      "apiVersion": "2023-05-01",
      "name": "[parameters('openAIServiceName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "[parameters('openAISku')]"
      },
      "kind": "OpenAI",
      "properties": {
        "customSubDomainName": "[parameters('openAIServiceName')]",
        "networkAcls": {
          "defaultAction": "Allow"
        },
        "publicNetworkAccess": "Enabled"
      }
    },
    {
      "type": "Microsoft.CognitiveServices/accounts/deployments",
      "apiVersion": "2023-05-01",
      "name": "[concat(parameters('openAIServiceName'), '/gpt-deployment')]",
      "dependsOn": [
        "[variables('openAIResourceId')]"
      ],
      "sku": {
        "name": "Standard",
        "capacity": "[parameters('openAIDeploymentCapacity')]"
      },
      "properties": {
        "model": {
          "format": "OpenAI",
          "name": "[parameters('openAIModelName')]",
          "version": "2024-08-06"
        },
        "versionUpgradeOption": "OnceNewDefaultVersionAvailable",
        "raiPolicyName": "Microsoft.Default"
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2022-09-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2",
      "properties": {
        "supportsHttpsTrafficOnly": true,
        "minimumTlsVersion": "TLS1_2"
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts/fileServices",
      "apiVersion": "2022-09-01",
      "name": "[concat(parameters('storageAccountName'), '/default')]",
      "dependsOn": [
        "[variables('storageAccountId')]"
      ]
    },
    {
      "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
      "apiVersion": "2022-09-01",
      "name": "[concat(parameters('storageAccountName'), '/default/', variables('fileShareName'))]",
      "dependsOn": [
        "[resourceId('Microsoft.Storage/storageAccounts/fileServices', parameters('storageAccountName'), 'default')]"
      ],
      "properties": {
        "shareQuota": 5120
      }
    },
    {
      "type": "Microsoft.Insights/components",
      "apiVersion": "2020-02-02",
      "name": "[variables('applicationInsightsName')]",
      "location": "[parameters('location')]",
      "kind": "web",
      "properties": {
        "Application_Type": "web"
      }
    },
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2022-03-01",
      "name": "[variables('hostingPlanName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Y1",
        "tier": "Dynamic"
      },
      "kind": "functionapp",
      "properties": {
        "reserved": true
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2022-03-01",
      "name": "[parameters('functionAppName')]",
      "location": "[parameters('location')]",
      "kind": "functionapp,linux",
      "identity": {
        "type": "SystemAssigned"
      },
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('hostingPlanName'))]",
        "[variables('storageAccountId')]",
        "[resourceId('Microsoft.Insights/components', variables('applicationInsightsName'))]",
        "[variables('openAIResourceId')]",
        "[resourceId('Microsoft.CognitiveServices/accounts/deployments', parameters('openAIServiceName'), 'gpt-deployment')]"
      ],
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('hostingPlanName'))]",
        "siteConfig": {
          "appSettings": [
            {
              "name": "AzureWebJobsStorage",
              "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageAccountName'), ';EndpointSuffix=', environment().suffixes.storage, ';AccountKey=',listKeys(variables('storageAccountId'), '2022-09-01').keys[0].value)]"
            },
            {
              "name": "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING",
              "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageAccountName'), ';EndpointSuffix=', environment().suffixes.storage, ';AccountKey=',listKeys(variables('storageAccountId'), '2022-09-01').keys[0].value)]"
            },
            {
              "name": "WEBSITE_CONTENTSHARE",
              "value": "[toLower(parameters('functionAppName'))]"
            },
            {
              "name": "FUNCTIONS_EXTENSION_VERSION",
              "value": "~4"
            },
            {
              "name": "FUNCTIONS_WORKER_RUNTIME",
              "value": "python"
            },
            {
              "name": "APPINSIGHTS_INSTRUMENTATIONKEY",
              "value": "[reference(resourceId('Microsoft.Insights/components', variables('applicationInsightsName'))).InstrumentationKey]"
            },
            {
              "name": "APPLICATIONINSIGHTS_CONNECTION_STRING",
              "value": "[reference(resourceId('Microsoft.Insights/components', variables('applicationInsightsName'))).ConnectionString]"
            },
            {
              "name": "AZURE_OPENAI_API_KEY",
              "value": "[listKeys(variables('openAIResourceId'), '2023-05-01').key1]"
            },
            {
              "name": "AZURE_OPENAI_ENDPOINT",
              "value": "[reference(variables('openAIResourceId')).endpoint]"
            },
            {
              "name": "AZURE_OPENAI_API_VERSION",
              "value": "2024-02-01"
            },
            {
              "name": "AZURE_OPENAI_DEPLOYMENT_NAME",
              "value": "gpt-deployment"
            },
            {
              "name": "AZURE_FILES_SHARE_NAME",
              "value": "[variables('fileShareName')]"
            },
            {
              "name": "ASSISTANT_NAME",
              "value": "{{assistant_name}}"
            },
            {
              "name": "CHARACTERISTIC_DESCRIPTION",
              "value": "{{assistant_description}}"
            },
            {
              "name": "SCM_DO_BUILD_DURING_DEPLOYMENT",
              "value": "true"
            },
            {
              "name": "ENABLE_ORYX_BUILD",
              "value": "true"
            },
            {
              "name": "PYTHON_ENABLE_WORKER_EXTENSIONS",
              "value": "1"
            }
          ],
          "linuxFxVersion": "python|3.11",
          "cors": {
            "allowedOrigins": ["*"],
            "supportCredentials": false
          },
          "ftpsState": "FtpsOnly"
        },
        "httpsOnly": true
      }
    }
  ],
  "outputs": {
    "windowsSetupScript": {
      "type": "string",
      "value": "[concat('# Generated setup script with your Azure values embedded\n# Run this after deployment completes')]"
    },
    "macLinuxSetupScript": {
      "type": "string",
      "value": "[concat('#!/bin/bash\n# Generated setup script with your Azure values embedded')]"
    },
    "functionAppName": {
      "type": "string",
      "value": "[parameters('functionAppName')]"
    },
    "functionEndpoint": {
      "type": "string",
      "value": "[concat('https://', reference(variables('functionAppId')).defaultHostName, '/api/{{function_route}}')]"
    },
    "functionUrlWithKey": {
      "type": "string",
      "value": "[concat('https://', reference(variables('functionAppId')).defaultHostName, '/api/{{function_route}}?code=', listkeys(concat(resourceId('Microsoft.Web/sites', parameters('functionAppName')), '/host/default'), '2022-03-01').functionKeys.default)]"
    },
    "powerPlatformConnectionUrl": {
      "type": "string",
      "value": "[concat('Use this URL in Power Automate HTTP action: ', reference(variables('functionAppId')).defaultHostName, '/api/{{function_route}}')]"
    }
  }
}
```

### 2. Main README.md with M365 Copilot Integration

```markdown
# {{project_name}} - Enterprise AI Assistant with M365 Copilot

## 🚀 Complete Deployment Process

### Step 1: Deploy to Azure (1 minute)
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/{{encoded_template_url}})

### Step 2: Test Your Endpoint
After deployment completes:
1. Click the **"Outputs"** tab in Azure Portal
2. Copy `functionUrlWithKey` value
3. Test with:
```bash
curl -X POST [YOUR_FUNCTION_URL] \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello", "conversation_history": []}'
```

### Step 3: Connect to Microsoft 365 Copilot

#### Download Power Platform Solution
[📦 Download Power Platform Solution](https://github.com/{{github_repo}}/raw/main/power_platform/MSFTAIBASMultiAgentCopilot_1_0_0_2.zip)

#### Import to Power Platform
1. Go to [make.powerapps.com](https://make.powerapps.com)
2. Navigate to **Solutions** → **Import solution**
3. Upload the downloaded ZIP file
4. Click **Next** → **Import**

#### Configure Power Automate Flow
1. Open the imported solution
2. Find **"Talk to MAC (Migration Assessment Copilot)"** flow
3. Edit the flow and update the HTTP action:
   - **URL**: `[Your Function URL from Step 2]`
   - **Key**: `[Your Function Key]`
4. Save and turn on the flow

#### Setup Copilot Studio Bot
1. Go to [Copilot Studio](https://copilotstudio.microsoft.com)
2. Find your imported bot **"Agent"**
3. Open **Topics** → **MAIN** topic
4. Verify the Power Automate action is connected
5. Test in the Test pane

#### Deploy to Microsoft 365
1. In Copilot Studio, go to **Channels**
2. Select **"Microsoft Teams"**
3. Click **"Turn on Teams"**
4. For M365 Copilot integration:
   - Enable **"Microsoft 365 Copilot"** channel
   - Configure declarative agent settings
   - Submit for admin approval if required

### Step 4: Choose Your Agent Stack
Browse our template library to select and deploy agent stacks for your specific use cases.

## ✨ Features

- 🧠 **{{ai_model}} Powered** - Latest Azure OpenAI models
- 💾 **Persistent Memory** - User-specific and shared memory
- 🔐 **Enterprise Security** - Function-level authentication
- ⚡ **Auto-scaling** - Serverless architecture
- 🎨 **Web Interface** - Complete management UI
- 🤝 **M365 Integration** - Teams and Copilot ready
- 📦 **Agent Marketplace** - GitHub-based agent store
- 🔧 **Zero Configuration** - Automatic setup

## 🏗️ Architecture

### Solution Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   User Interface Layer                    │
├───────────────┬──────────────┬──────────────────────────┤
│ M365 Copilot  │ Teams        │ Web Interface            │
└───────┬───────┴──────┬───────┴──────────┬───────────────┘
        │              │                  │
┌───────▼──────────────▼──────────────────▼───────────────┐
│              Copilot Studio (Conversation Layer)         │
│  • Natural Language Processing                           │
│  • Conversation Management                               │
│  • User Authentication                                   │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│           Power Automate (Integration Layer)             │
│  • User Context from Office 365                          │
│  • Data Transformation                                   │
│  • Error Handling                                        │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│          Azure Function (Processing Layer)               │
│  • Agent Selection & Routing                             │
│  • Memory Management                                     │
│  • Azure OpenAI Integration                              │
└───┬──────┬──────┬──────┬──────┬─────────────────────────┘
    │      │      │      │      │
┌───▼──┬───▼──┬───▼──┬───▼──┬───▼─────────────────────────┐
│ CRM  │ Doc  │Email │ Cal  │ Custom Agents               │
└──────┴──────┴──────┴──────┴─────────────────────────────┘
    │                            │
┌───▼────────────────────────────▼─────────────────────────┐
│                     Data Layer                           │
│  • Azure Storage (Memory)                                │
│  • Azure OpenAI (GPT-4o)                                 │
│  • Business Systems (CRM, SharePoint, etc.)              │
└───────────────────────────────────────────────────────────┘
```

## 📋 API Specification

### Main Function Endpoint
```
POST /api/{{function_route}}
```

### Request Format
```json
{
  "user_input": "Your message here",
  "conversation_history": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ],
  "user_guid": "optional-user-identifier",
  "agent_action": "optional-specific-agent",
  "context": {
    "user_email": "from-power-automate",
    "user_name": "from-power-automate",
    "tenant_id": "from-power-automate"
  }
}
```

### Response Format
```json
{
  "assistant_response": "Formatted markdown response",
  "voice_response": "Short voice-friendly response",
  "agent_logs": "Debug information",
  "user_guid": "user-identifier-in-use",
  "adaptive_card": "optional-teams-adaptive-card",
  "actions": [
    {
      "type": "create_task",
      "parameters": {}
    }
  ]
}
```

## 🛠️ Power Platform Integration Files

### Power Automate Flow Template
```json
{
  "name": "Talk to AI Agent",
  "trigger": "PowerVirtualAgents",
  "actions": [
    {
      "type": "HTTP",
      "method": "POST",
      "uri": "@{parameters('FunctionUrl')}",
      "headers": {
        "Content-Type": "application/json",
        "x-functions-key": "@{parameters('FunctionKey')}"
      },
      "body": {
        "user_input": "@{triggerBody()['text']}",
        "conversation_history": "@{variables('ConversationHistory')}",
        "user_guid": "@{triggerBody()['UserID']}",
        "context": {
          "user_email": "@{triggerBody()['UserEmail']}",
          "user_name": "@{triggerBody()['UserDisplayName']}",
          "tenant_id": "@{triggerBody()['TenantID']}"
        }
      }
    },
    {
      "type": "Response",
      "body": {
        "text": "@{body('HTTP')['assistant_response']}",
        "speak": "@{body('HTTP')['voice_response']}",
        "card": "@{body('HTTP')['adaptive_card']}"
      }
    }
  ]
}
```

### Copilot Studio Configuration
```json
{
  "bot_name": "{{assistant_name}}",
  "description": "{{assistant_description}}",
  "topics": [
    {
      "name": "MAIN",
      "trigger_phrases": [
        "Talk to {{assistant_name}}",
        "Connect me to the AI agent",
        "I need help from the assistant"
      ],
      "actions": [
        {
          "type": "PowerAutomate",
          "flow": "Talk to AI Agent",
          "inputs": ["user_message", "conversation_context"],
          "outputs": ["response", "voice", "card"]
        }
      ]
    }
  ],
  "channels": {
    "teams": {
      "enabled": true,
      "app_id": "auto-generated",
      "welcome_message": "Hello! I'm {{assistant_name}}, your AI assistant. How can I help you today?"
    },
    "m365_copilot": {
      "enabled": true,
      "declarative_agent": {
        "name": "{{assistant_name}}",
        "description": "{{assistant_description}}",
        "instructions": "You are an AI assistant that helps users with various tasks through natural language.",
        "capabilities": [
          "answer_questions",
          "process_documents",
          "manage_tasks",
          "integrate_with_systems"
        ]
      }
    }
  }
}
```

## 🎯 Agent Stack Templates

### Available Pre-configured Stacks

#### 1. Basic Starter Pack
```python
agents = [
  "basic_agent.py",
  "context_memory_agent.py",
  "manage_memory_agent.py"
]
```

#### 2. M365 Integration Suite
```python
agents = [
  "dynamics_365_agent.py",
  "sharepoint_agent.py",
  "teams_agent.py",
  "outlook_agent.py",
  "planner_agent.py"
]
```

#### 3. Document Processing Stack
```python
agents = [
  "pdf_processor_agent.py",
  "document_extractor_agent.py",
  "ocr_agent.py",
  "summary_agent.py"
]
```

#### 4. Voice & Communication Stack
```python
agents = [
  "voice_to_text_agent.py",
  "text_to_speech_agent.py",
  "email_drafting_agent.py",
  "teams_notification_agent.py"
]
```

## 📦 Agent Manifest (manifest.json)

```json
{
  "version": "1.0.0",
  "generated": "{{timestamp}}",
  "repository": "{{github_repo}}",
  "agents": [
    {
      "id": "basic_agent",
      "name": "Basic Agent",
      "filename": "basic_agent.py",
      "category": "core",
      "description": "Foundation agent with core capabilities",
      "features": ["Base functionality", "Core operations"],
      "size": "5KB",
      "url": "https://raw.githubusercontent.com/{{github_repo}}/main/agents/basic_agent.py"
    }
  ],
  "stacks": [
    {
      "id": "m365_integration",
      "name": "Microsoft 365 Integration Suite",
      "description": "Complete M365 integration",
      "agents": ["dynamics_365_agent", "sharepoint_agent", "teams_agent"],
      "metadata": {
        "complexity": "advanced",
        "estimatedSetupTime": "2-3 weeks",
        "requiredLicenses": ["M365 E3", "Power Platform"]
      }
    }
  ]
}
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11 (required for Azure Functions v4)
- Azure Functions Core Tools v4
- Node.js 16+ (for Azure Functions Core Tools)
- Azure CLI (optional for deployment)
- Power Platform license (for M365 integration)

### Quick Start
```bash
# Clone repository
git clone https://github.com/{{github_repo}}.git
cd {{project_name}}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy local settings template
cp local.settings.json.template local.settings.json
# Edit local.settings.json with your Azure values

# Start local development
func start
```

### Testing M365 Integration Locally
1. Use ngrok to expose local function: `ngrok http 7071`
2. Update Power Automate flow with ngrok URL
3. Test through Teams or Copilot Studio Test pane

## 🚀 Deployment Options

### Option 1: GitHub Actions CI/CD
```yaml
name: Deploy to Azure Functions

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: azure/functions-action@v1
      with:
        app-name: ${{ secrets.AZURE_FUNCTIONAPP_NAME }}
        package: '.'
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

### Option 2: Azure CLI
```bash
# Login to Azure
az login

# Deploy to Function App
func azure functionapp publish {{function_app_name}}

# Deploy Power Platform solution
pac solution import --path ./power_platform/solution.zip
```

### Option 3: VS Code Extension
1. Install Azure Functions extension
2. Sign in to Azure
3. Right-click on project → Deploy to Function App

## 💰 Cost Estimation

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| Azure Functions | Consumption plan | ~$0-5 |
| Azure Storage | 5GB file storage | ~$5 |
| Azure OpenAI | 100K tokens/day | ~$30 |
| Application Insights | Basic telemetry | ~$0 |
| Power Platform | Per user license | ~$20/user |
| **Total** | | **~$55 + usage** |

## 🔒 Security Configuration

### Azure Function Security
- Function-level authentication keys
- Managed Identity for Azure resources
- IP restrictions (optional)
- CORS configuration

### M365 Integration Security
- OAuth 2.0 authentication
- Service Principal registration
- Conditional Access policies
- Data Loss Prevention (DLP) compliance

### Power Platform Security
```json
{
  "authentication": {
    "type": "OAuth2",
    "authority": "https://login.microsoftonline.com/{{tenant_id}}",
    "audience": "api://{{app_id}}"
  },
  "permissions": {
    "delegated": [
      "User.Read",
      "Mail.Send",
      "Calendars.ReadWrite",
      "Files.ReadWrite.All"
    ],
    "application": [
      "User.Read.All",
      "Mail.Send",
      "Calendars.ReadWrite",
      "Sites.ReadWrite.All"
    ]
  }
}
```

## 📊 Monitoring & Analytics

### Application Insights Queries
```kusto
// Agent usage by type
customEvents
| where timestamp > ago(7d)
| where name == "AgentExecution"
| summarize count() by tostring(customDimensions.agentName)
| render piechart

// Response times
requests
| where timestamp > ago(1d)
| summarize avg(duration), percentile(duration, 95) by bin(timestamp, 1h)
| render timechart

// Error tracking
exceptions
| where timestamp > ago(1d)
| summarize count() by problemId, outerMessage
| order by count_ desc
```

### Power Platform Analytics
- Bot Analytics in Copilot Studio
- Flow run history in Power Automate
- Usage analytics in Power Platform Admin Center

## 🧪 Testing

### Unit Tests
```python
# tests/test_agents.py
import pytest
from agents.basic_agent import BasicAgent

def test_basic_agent():
    agent = BasicAgent()
    result = agent.perform(user_input="test")
    assert result is not None
```

### Integration Tests
```python
# tests/test_integration.py
import requests

def test_function_endpoint():
    response = requests.post(
        "http://localhost:7071/api/{{function_route}}",
        json={"user_input": "Hello", "conversation_history": []}
    )
    assert response.status_code == 200
    assert "assistant_response" in response.json()
```

### Power Platform Testing
1. Use Copilot Studio Test pane
2. Test in Teams with test users
3. Monitor Power Automate flow runs

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Python version mismatch | Use Python 3.11 specifically |
| Path with spaces error | Use quoted paths or short names |
| Azure deployment fails | Check region availability and quotas |
| Power Automate 401 error | Verify function key in flow |
| Copilot not responding | Check Power Automate flow is on |
| Teams app not visible | Wait for admin approval |
| Memory not persisting | Check Azure Storage connection |

### Debug Commands
```bash
# Check Azure Function logs
func azure functionapp logstream {{function_app_name}}

# Test locally with verbose output
func start --verbose

# Check Power Automate runs
pac flow run list --environment {{environment_id}}

# Validate ARM template
az deployment group validate \
  --resource-group {{resource_group}} \
  --template-file azuredeploy.json
```

## 📚 Documentation

### For Developers
- [AGENTS.md](docs/AGENTS.md) - Agent development guide
- [API.md](docs/API.md) - API reference
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide

### For M365 Administrators
- [COPILOT_INTEGRATION.md](docs/COPILOT_INTEGRATION.md) - M365 setup
- [POWER_PLATFORM.md](docs/POWER_PLATFORM.md) - Power Platform config
- [SECURITY.md](docs/SECURITY.md) - Security best practices

### For End Users
- [USER_GUIDE.md](docs/USER_GUIDE.md) - How to use the assistant
- [TEAMS_GUIDE.md](docs/TEAMS_GUIDE.md) - Teams app usage
- [FAQ.md](docs/FAQ.md) - Frequently asked questions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add unit tests for new agents
- Update documentation
- Test M365 integration before PR

## 📝 License

{{license_type}}

## 🆘 Support

- **GitHub Issues**: [{{github_repo}}/issues](https://github.com/{{github_repo}}/issues)
- **Discussions**: [{{github_repo}}/discussions](https://github.com/{{github_repo}}/discussions)
- **Documentation**: [{{documentation_url}}]({{documentation_url}})
- **Microsoft Support**: For M365/Power Platform issues

---

<p align="center">
  Made with ❤️ by {{author}}
  <br><br>
  <strong>Enterprise AI Made Simple</strong>
</p>
```

## 🎯 Template Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{project_name}}` | Project name | `AI-Assistant-M365` |
| `{{project_prefix}}` | Resource prefix | `aiaccel` |
| `{{assistant_name}}` | Assistant name | `Copilot Agent 365` |
| `{{assistant_description}}` | Assistant personality | `Enterprise AI assistant integrated with Microsoft 365` |
| `{{function_route}}` | API route | `businessinsightbot_function` |
| `{{file_share_name}}` | Azure file share | `azfbusinessbot3c92ab` |
| `{{ai_model}}` | AI model name | `GPT-4o` |
| `{{author}}` | Project author | `Your Organization` |
| `{{license_type}}` | License | `MIT` |
| `{{github_repo}}` | GitHub repository | `kody-w/AI-Agent-Templates` |
| `{{encoded_template_url}}` | URL-encoded ARM template | `https%3A%2F%2Fraw...` |
| `{{documentation_url}}` | Docs URL | `https://docs.example.com` |
| `{{tenant_id}}` | Azure AD tenant | `your-tenant-id` |

## 🚀 Quick Start Commands

```bash
# One-liner setup (after Azure deployment)
curl -sSL https://raw.githubusercontent.com/{{github_repo}}/main/setup.sh | bash

# Or for Windows PowerShell
iwr -useb https://raw.githubusercontent.com/{{github_repo}}/main/setup.ps1 | iex

# Test the deployment
curl -X POST https://{{function_app_name}}.azurewebsites.net/api/{{function_route}} \
  -H "Content-Type: application/json" \
  -H "x-functions-key: {{function_key}}" \
  -d '{"user_input": "Hello", "conversation_history": []}'
```

## 📈 Success Metrics

Track these KPIs after deployment:
- **Response Time**: < 2 seconds (P95)
- **Error Rate**: < 1%
- **User Adoption**: 50% of team using within 30 days
- **Cost per Conversation**: < $0.10
- **Memory Recall Accuracy**: > 95%
- **M365 Integration Success**: > 99%
- **Agent Execution Success**: > 98%

---

**This complete template provides everything needed for enterprise deployment with full M365 Copilot integration!**