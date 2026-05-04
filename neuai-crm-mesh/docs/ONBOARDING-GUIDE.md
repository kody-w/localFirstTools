# NeuAI CRM Data Mesh - Live CRM Onboarding Guide

This guide walks you through obtaining credentials to connect the NeuAI CRM Data Mesh to live Salesforce and Dynamics 365 instances.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Salesforce Setup](#salesforce-setup)
   - [Create a Connected App](#step-1-create-a-connected-app)
   - [Configure OAuth Settings](#step-2-configure-oauth-settings)
   - [Retrieve Credentials](#step-3-retrieve-credentials)
   - [Get Security Token](#step-4-get-security-token-optional)
   - [API Permissions](#step-5-verify-api-permissions)
3. [Dynamics 365 Setup](#dynamics-365-setup)
   - [Azure AD App Registration](#step-1-azure-ad-app-registration)
   - [Configure API Permissions](#step-2-configure-api-permissions)
   - [Create Client Secret](#step-3-create-client-secret)
   - [Create Application User in Dynamics](#step-4-create-application-user-in-dynamics-365)
   - [Get Environment URL](#step-5-get-your-dynamics-365-environment-url)
4. [Environment Configuration](#environment-configuration)
5. [Testing Your Connection](#testing-your-connection)
6. [Troubleshooting](#troubleshooting)
7. [Security Best Practices](#security-best-practices)

---

## Prerequisites

Before starting, ensure you have:

| Platform | Requirements |
|----------|--------------|
| **Salesforce** | Admin access to a Salesforce org (Production, Sandbox, or Developer Edition) |
| **Dynamics 365** | Admin access to a Dynamics 365 environment + Azure AD Global Admin or Application Administrator role |
| **Local** | Python 3.9+ installed |

**Get Free Developer Accounts:**
- Salesforce Developer Edition: https://developer.salesforce.com/signup
- Dynamics 365 Trial: https://dynamics.microsoft.com/en-us/dynamics-365-free-trial/
- Azure Free Account: https://azure.microsoft.com/en-us/free/

---

## Salesforce Setup

### Step 1: Create a Connected App

1. **Log into Salesforce** at https://login.salesforce.com (or your custom domain)

2. **Navigate to Setup**
   - Click the gear icon (⚙️) → **Setup**

3. **Find App Manager**
   - In the Quick Find box, type `App Manager`
   - Click **App Manager** under Apps

4. **Create New Connected App**
   - Click **New Connected App** (top right)
   - Fill in the basic information:

   | Field | Value |
   |-------|-------|
   | Connected App Name | `NeuAI CRM Data Mesh` |
   | API Name | `NeuAI_CRM_Data_Mesh` (auto-populated) |
   | Contact Email | Your email address |

### Step 2: Configure OAuth Settings

1. **Enable OAuth Settings**
   - Check ✅ **Enable OAuth Settings**

2. **Set Callback URL**
   ```
   https://localhost:8080/oauth/callback
   ```
   (For server-to-server, you can also use: `https://login.salesforce.com/services/oauth2/success`)

3. **Select OAuth Scopes** - Add these scopes:

   | Scope | Description |
   |-------|-------------|
   | `api` | Access and manage your data (required) |
   | `refresh_token, offline_access` | Perform requests at any time (required for long-running) |
   | `full` | Full access (alternative to granular scopes) |

   **Minimum Required Scopes:**
   - `Access and manage your data (api)`
   - `Perform requests on your behalf at any time (refresh_token, offline_access)`

4. **Additional Settings**
   - ✅ **Require Secret for Web Server Flow**
   - ✅ **Require Secret for Refresh Token Flow**
   - ✅ **Enable Client Credentials Flow** (for server-to-server)

5. **Save** the Connected App

6. **Wait 2-10 minutes** for Salesforce to propagate the app

### Step 3: Retrieve Credentials

1. **Navigate back to App Manager**
   - Setup → App Manager

2. **Find your app** and click the dropdown arrow → **View**

3. **Copy the credentials:**

   | Credential | Location | Example |
   |------------|----------|---------|
   | **Consumer Key** (Client ID) | API (Enable OAuth Settings) section | `3MVG9...` (long alphanumeric) |
   | **Consumer Secret** | Click **Manage Consumer Details** → Verify identity | `1234567890ABCDEF...` |

   > ⚠️ **Important:** The Consumer Secret is shown only once. Save it securely!

### Step 4: Get Security Token (Optional)

For **Username-Password Flow** (not recommended for production):

1. Click your profile picture → **Settings**
2. In Quick Find, type `Reset My Security Token`
3. Click **Reset My Security Token**
4. Check your email for the new token
5. Append the token to your password when authenticating

### Step 5: Verify API Permissions

1. **Check Profile API Access**
   - Setup → Profiles → Select your profile
   - Ensure **API Enabled** is checked

2. **Check Permission Sets** (if using)
   - Setup → Permission Sets
   - Verify the user has API access

3. **IP Relaxation** (for development)
   - Navigate to the Connected App
   - Edit Policies
   - Set IP Relaxation to **Relax IP restrictions**

---

## Dynamics 365 Setup

### Step 1: Azure AD App Registration

1. **Go to Azure Portal**
   - Navigate to https://portal.azure.com

2. **Open Azure Active Directory**
   - Search for `Azure Active Directory` in the top search bar
   - Click on it

3. **Create App Registration**
   - In the left sidebar, click **App registrations**
   - Click **+ New registration**

4. **Fill in App Details:**

   | Field | Value |
   |-------|-------|
   | Name | `NeuAI CRM Data Mesh` |
   | Supported account types | `Accounts in this organizational directory only` (Single tenant) |
   | Redirect URI | Select `Web` → `https://localhost:8080/oauth/callback` |

5. **Click Register**

6. **Copy Essential IDs** (from Overview page):

   | ID | Description | Example |
   |----|-------------|---------|
   | **Application (client) ID** | Your app's unique identifier | `12345678-1234-1234-1234-123456789abc` |
   | **Directory (tenant) ID** | Your Azure AD tenant | `abcdefgh-1234-5678-9abc-def012345678` |

### Step 2: Configure API Permissions

1. **Navigate to API Permissions**
   - In your app registration, click **API permissions** in the left sidebar

2. **Add Dynamics CRM Permission**
   - Click **+ Add a permission**
   - Select **APIs my organization uses**
   - Search for `Dynamics CRM` (or `Dataverse`)
   - Click **Dynamics CRM**

3. **Select Permission Type:**

   | Permission Type | Use Case |
   |-----------------|----------|
   | **Delegated permissions** | When a user signs in (interactive) |
   | **Application permissions** | Server-to-server (background/daemon) |

4. **For Server-to-Server (Recommended):**
   - Select **Application permissions**
   - Check ✅ `user_impersonation`

5. **For Interactive (User Sign-in):**
   - Select **Delegated permissions**
   - Check ✅ `user_impersonation`

6. **Click Add permissions**

7. **Grant Admin Consent**
   - Click **Grant admin consent for [Your Organization]**
   - Confirm by clicking **Yes**
   - Status should show ✅ green checkmarks

### Step 3: Create Client Secret

1. **Navigate to Certificates & secrets**
   - In your app registration, click **Certificates & secrets**

2. **Create New Secret**
   - Click **+ New client secret**
   - Description: `NeuAI CRM Mesh Production`
   - Expires: Choose based on your security policy
     - `6 months` (recommended for production)
     - `12 months`
     - `24 months`
     - `Custom` (set specific date)

3. **Copy the Secret Value IMMEDIATELY**

   > ⚠️ **Critical:** The secret value is shown **only once**! Copy it now.

   | Field | What to Copy |
   |-------|--------------|
   | **Value** | The actual secret (copy this!) - looks like `abc123~...` |
   | **Secret ID** | The ID of the secret (not the secret itself) |

### Step 4: Create Application User in Dynamics 365

For **server-to-server** authentication, you must create an Application User:

1. **Go to Power Platform Admin Center**
   - Navigate to https://admin.powerplatform.microsoft.com

2. **Select Your Environment**
   - Click **Environments** in the left sidebar
   - Click on your Dynamics 365 environment

3. **Open Settings**
   - Click **Settings** at the top
   - Expand **Users + permissions**
   - Click **Application users**

4. **Create New Application User**
   - Click **+ New app user**
   - Click **+ Add an app**
   - Search for `NeuAI CRM Data Mesh` (your registered app)
   - Select it and click **Add**

5. **Assign Business Unit**
   - Select your primary **Business unit**

6. **Assign Security Role**
   - Click **Edit** (pencil icon) next to Security roles
   - Add appropriate roles:

   | Role | Access Level |
   |------|--------------|
   | `System Administrator` | Full access (development only) |
   | `Salesperson` | Standard CRM access |
   | `Sales Manager` | Enhanced CRM access |
   | Custom Role | Based on your requirements |

7. **Save** the application user

### Step 5: Get Your Dynamics 365 Environment URL

1. **From Power Platform Admin Center:**
   - Go to https://admin.powerplatform.microsoft.com
   - Click **Environments**
   - Select your environment
   - Copy the **Environment URL**

   Example URLs:
   ```
   https://yourorg.crm.dynamics.com          (North America)
   https://yourorg.crm4.dynamics.com         (EMEA)
   https://yourorg.crm5.dynamics.com         (Asia Pacific)
   https://yourorg.crm9.dynamics.com         (Government)
   ```

2. **From Dynamics 365 App:**
   - Open any Dynamics 365 app
   - Look at the URL in your browser
   - Copy the base URL (everything before `/main.aspx`)

---

## Environment Configuration

Create a `.env` file in the `neuai-crm-mesh` directory:

```bash
# ===========================================
# NeuAI CRM Data Mesh - Environment Configuration
# ===========================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control!

# ----- Salesforce Configuration -----
SALESFORCE_CLIENT_ID=your_consumer_key_here
SALESFORCE_CLIENT_SECRET=your_consumer_secret_here
SALESFORCE_USERNAME=your.email@company.com
SALESFORCE_PASSWORD=your_password_here
SALESFORCE_SECURITY_TOKEN=your_security_token_here
SALESFORCE_DOMAIN=login.salesforce.com
# Use test.salesforce.com for sandboxes
# Use your custom domain if configured (e.g., mycompany.my.salesforce.com)

# Salesforce API Version (check latest at developer.salesforce.com)
SALESFORCE_API_VERSION=v59.0

# ----- Dynamics 365 Configuration -----
DYNAMICS_CLIENT_ID=your_application_client_id_here
DYNAMICS_CLIENT_SECRET=your_client_secret_value_here
DYNAMICS_TENANT_ID=your_directory_tenant_id_here
DYNAMICS_ENVIRONMENT_URL=https://yourorg.crm.dynamics.com

# Dynamics 365 API Version
DYNAMICS_API_VERSION=v9.2

# ----- Local CRM Configuration -----
LOCAL_DATA_DIR=./data
LOCAL_BACKUP_ENABLED=true

# ----- Server Configuration -----
HOST=0.0.0.0
PORT=8080
DEBUG=false
LOG_LEVEL=INFO

# ----- Security -----
# Enable/disable features
ENABLE_AI_QUERIES=true
DUPLICATE_THRESHOLD=0.8

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Credential Summary Table

| Platform | Credential | How to Get |
|----------|------------|------------|
| **Salesforce** | Client ID | Connected App → Consumer Key |
| **Salesforce** | Client Secret | Connected App → Manage Consumer Details |
| **Salesforce** | Security Token | User Settings → Reset My Security Token |
| **Dynamics 365** | Client ID | Azure AD App → Application (client) ID |
| **Dynamics 365** | Client Secret | Azure AD App → Certificates & secrets |
| **Dynamics 365** | Tenant ID | Azure AD App → Directory (tenant) ID |
| **Dynamics 365** | Environment URL | Power Platform Admin → Environment details |

---

## Testing Your Connection

### Test Salesforce Connection

```python
# test_salesforce.py
import os
from simple_salesforce import Salesforce

sf = Salesforce(
    username=os.getenv('SALESFORCE_USERNAME'),
    password=os.getenv('SALESFORCE_PASSWORD'),
    security_token=os.getenv('SALESFORCE_SECURITY_TOKEN'),
    client_id=os.getenv('SALESFORCE_CLIENT_ID'),
    client_secret=os.getenv('SALESFORCE_CLIENT_SECRET')
)

# Test query
accounts = sf.query("SELECT Id, Name FROM Account LIMIT 5")
print(f"Found {accounts['totalSize']} accounts")
for record in accounts['records']:
    print(f"  - {record['Name']}")
```

### Test Dynamics 365 Connection

```python
# test_dynamics.py
import os
import requests
from msal import ConfidentialClientApplication

# Get access token
app = ConfidentialClientApplication(
    client_id=os.getenv('DYNAMICS_CLIENT_ID'),
    client_credential=os.getenv('DYNAMICS_CLIENT_SECRET'),
    authority=f"https://login.microsoftonline.com/{os.getenv('DYNAMICS_TENANT_ID')}"
)

token = app.acquire_token_for_client(
    scopes=[f"{os.getenv('DYNAMICS_ENVIRONMENT_URL')}/.default"]
)

# Test API call
headers = {
    'Authorization': f"Bearer {token['access_token']}",
    'OData-MaxVersion': '4.0',
    'OData-Version': '4.0',
    'Content-Type': 'application/json'
}

response = requests.get(
    f"{os.getenv('DYNAMICS_ENVIRONMENT_URL')}/api/data/v9.2/accounts?$top=5",
    headers=headers
)

data = response.json()
print(f"Found {len(data['value'])} accounts")
for account in data['value']:
    print(f"  - {account['name']}")
```

### Run Connection Tests

```bash
# Install test dependencies
pip install simple-salesforce msal requests python-dotenv

# Load environment and run tests
cd neuai-crm-mesh
python -c "from dotenv import load_dotenv; load_dotenv()" && python test_salesforce.py
python -c "from dotenv import load_dotenv; load_dotenv()" && python test_dynamics.py
```

---

## Troubleshooting

### Salesforce Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_LOGIN` | Wrong credentials | Verify username, password, and security token |
| `INVALID_CLIENT` | Wrong Consumer Key/Secret | Regenerate in Connected App |
| `API_DISABLED_FOR_ORG` | API not enabled | Contact Salesforce admin to enable API |
| `REQUEST_LIMIT_EXCEEDED` | Too many API calls | Implement rate limiting, upgrade edition |
| `INVALID_SESSION_ID` | Token expired | Refresh the access token |

### Dynamics 365 Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `AADSTS7000215` | Invalid client secret | Regenerate secret in Azure AD |
| `AADSTS700016` | App not found in tenant | Check tenant ID, re-register app |
| `AADSTS65001` | Consent not granted | Admin must grant consent |
| `403 Forbidden` | Missing security role | Add security role to Application User |
| `401 Unauthorized` | Invalid/expired token | Check credentials, refresh token |

### Common Issues

**"Connected App not found" (Salesforce)**
- Wait 10 minutes after creating the app
- Ensure you're in the correct org (Production vs Sandbox)

**"Application not assigned to a role" (Dynamics)**
- Create Application User in Power Platform Admin Center
- Assign appropriate security role

**"CORS error" (Browser)**
- Add your frontend origin to `CORS_ORIGINS` in `.env`
- For development, use `*` (not recommended for production)

---

## Security Best Practices

### Credential Storage

| Do | Don't |
|----|-------|
| ✅ Use environment variables | ❌ Hardcode credentials in code |
| ✅ Use `.env` files (gitignored) | ❌ Commit credentials to git |
| ✅ Use secret managers in production | ❌ Log credentials |
| ✅ Rotate secrets regularly | ❌ Share credentials via email/chat |

### Recommended Secret Managers

| Platform | Service |
|----------|---------|
| Azure | Azure Key Vault |
| AWS | AWS Secrets Manager |
| GCP | Google Secret Manager |
| Local | HashiCorp Vault |

### Minimum Permissions Principle

**Salesforce:**
- Create a dedicated integration user
- Use Permission Sets instead of Profiles
- Grant only required object permissions

**Dynamics 365:**
- Create custom security role with minimal permissions
- Use Application User (not real user credentials)
- Scope to specific Business Units if needed

### Token Refresh Strategy

```python
# Implement token refresh logic
class TokenManager:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

    def get_token(self):
        if self.is_expired():
            self.refresh()
        return self.access_token

    def is_expired(self):
        return datetime.now() >= self.expires_at - timedelta(minutes=5)
```

---

## Next Steps

After completing this onboarding:

1. **Install Python dependencies:**
   ```bash
   cd neuai-crm-mesh
   pip install -r requirements.txt
   pip install simple-salesforce msal python-dotenv
   ```

2. **Run connection tests** to verify credentials

3. **Start the Data Mesh server:**
   ```bash
   python -m neuai_crm serve --port 8080
   ```

4. **Use the CLI to test operations:**
   ```bash
   python -m neuai_crm stats
   python -m neuai_crm query "Show me all accounts"
   ```

---

## Quick Reference Card

### Salesforce Checklist
- [ ] Create Connected App
- [ ] Enable OAuth Settings
- [ ] Add API scopes
- [ ] Copy Consumer Key
- [ ] Copy Consumer Secret
- [ ] Get Security Token (if needed)
- [ ] Verify API access on profile

### Dynamics 365 Checklist
- [ ] Register Azure AD App
- [ ] Copy Application (client) ID
- [ ] Copy Directory (tenant) ID
- [ ] Add Dynamics CRM API permission
- [ ] Grant admin consent
- [ ] Create client secret (copy immediately!)
- [ ] Create Application User in Power Platform
- [ ] Assign security role
- [ ] Get environment URL

### Environment Variables Checklist
- [ ] Create `.env` file
- [ ] Add `.env` to `.gitignore`
- [ ] Fill in Salesforce credentials
- [ ] Fill in Dynamics 365 credentials
- [ ] Test connections

---

## Support Resources

| Resource | URL |
|----------|-----|
| Salesforce Developer Docs | https://developer.salesforce.com/docs |
| Salesforce Connected Apps | https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm |
| Dynamics 365 Web API | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview |
| Azure AD App Registration | https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app |
| MSAL Python | https://github.com/AzureAD/microsoft-authentication-library-for-python |
| Simple Salesforce | https://github.com/simple-salesforce/simple-salesforce |

---

*Last updated: December 2024*
*NeuAI CRM Data Mesh v1.0*
