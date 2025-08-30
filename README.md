# Deploy to Azure Button

## 🚀 Quick Deploy to Azure

Deploy the complete Copilot Agent 365 infrastructure with one click:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2Flocalfirsttools%2Fmain%2Fazuredeploy.json)

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
git clone https://github.com/kody-w/localfirsttools.git
cd localfirsttools

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
   encodeURIComponent("https://raw.githubusercontent.com/kody-w/localfirsttools/main/azuredeploy.json")
   ```
   Result: `https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2Flocalfirsttools%2Fmain%2Fazuredeploy.json`
3. Replace `ENCODED_TEMPLATE_URL` with the encoded result

### Alternative Button Styles

**Large Button:**
```markdown
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2Flocalfirsttools%2Fmain%2Fazuredeploy.json)
```

**Small Button:**
```markdown
[![Deploy to Azure](https://azuredeploy.net/deploybutton.png)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2Flocalfirsttools%2Fmain%2Fazuredeploy.json)
```

**Government Cloud:**
```markdown
[![Deploy to Azure Gov](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazuregov.png)](https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fkody-w%2Flocalfirsttools%2Fmain%2Fazuredeploy.json)
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

- [Report Issues](https://github.com/kody-w/localfirsttools/issues)
- [Documentation](https://github.com/kody-w/localfirsttools/wiki)
- [Azure Status](https://status.azure.com)