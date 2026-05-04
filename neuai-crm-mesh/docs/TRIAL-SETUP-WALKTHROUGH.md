# Trial Instance Setup Walkthrough

A complete, step-by-step guide to setting up free trial instances of Salesforce and Dynamics 365, then connecting them to NeuAI CRM Data Mesh.

**Time Required:** ~45 minutes total
- Salesforce: ~15 minutes
- Dynamics 365: ~25 minutes
- Testing: ~5 minutes

---

## Table of Contents

1. [Part 1: Salesforce Developer Edition](#part-1-salesforce-developer-edition)
2. [Part 2: Dynamics 365 Trial](#part-2-dynamics-365-trial)
3. [Part 3: Configure Environment](#part-3-configure-environment)
4. [Part 4: Test Connections](#part-4-test-connections)
5. [Part 5: Load Sample Data](#part-5-load-sample-data)
6. [Appendix: Credential Reference](#appendix-credential-reference)

---

## Part 1: Salesforce Developer Edition

Salesforce offers a **free, permanent Developer Edition** (not a time-limited trial). This is perfect for development and testing.

### Step 1.1: Sign Up for Developer Edition

1. **Open the signup page:**
   ```
   https://developer.salesforce.com/signup
   ```

2. **Fill in the registration form:**

   | Field | What to Enter |
   |-------|---------------|
   | First Name | Your first name |
   | Last Name | Your last name |
   | Email | Your email (use a real one - verification required) |
   | Role | Select `Developer` |
   | Company | Your company or `Personal` |
   | Country | Your country |
   | Postal Code | Your postal code |
   | Username | **IMPORTANT:** This must be in email format but doesn't need to be a real email. Example: `yourname@neuai-dev.com` |

   > **Note:** Your username is NOT your email. It's a unique identifier in email format. You can make up a domain.

3. **Click "Sign me up"**

4. **Check your email** for a verification message from Salesforce
   - Subject: "Verify your new Salesforce account"
   - Click the verification link

5. **Set your password:**
   - Must be 8+ characters
   - Must include letters and numbers
   - **Save this password securely!**

6. **Complete the initial setup wizard** (you can skip most of it)

### Step 1.2: Get Your Salesforce Instance URL

After logging in:

1. **Look at your browser's address bar**

   You'll see something like:
   ```
   https://yourname-dev-ed.develop.my.salesforce.com/...
   ```

2. **Your instance URL is:**
   ```
   https://yourname-dev-ed.develop.my.salesforce.com
   ```

   Or for Lightning:
   ```
   https://yourname-dev-ed.lightning.force.com
   ```

3. **Write this down** - you'll need it later

### Step 1.3: Create a Connected App

1. **Open Setup:**
   - Click the **gear icon** (⚙️) in the top-right
   - Click **Setup**

2. **Navigate to App Manager:**
   - In the **Quick Find** box (left sidebar), type: `App Manager`
   - Click **App Manager**

3. **Create New Connected App:**
   - Click **New Connected App** (top-right button)

4. **Fill in Basic Information:**

   | Field | Value |
   |-------|-------|
   | Connected App Name | `NeuAI CRM Data Mesh` |
   | API Name | (auto-fills to `NeuAI_CRM_Data_Mesh`) |
   | Contact Email | Your email address |

5. **Enable OAuth Settings:**
   - Scroll down to **API (Enable OAuth Settings)**
   - Check ✅ **Enable OAuth Settings**

6. **Set Callback URL:**
   ```
   https://localhost:8080/oauth/callback
   ```

   (You can also add: `https://login.salesforce.com/services/oauth2/success`)

7. **Select OAuth Scopes:**

   Click **Add** for each of these scopes:
   - `Access and manage your data (api)` ← **Required**
   - `Perform requests on your behalf at any time (refresh_token, offline_access)` ← **Required**
   - `Access your basic information (id, profile, email, address, phone)` ← Optional but helpful

   Your Selected OAuth Scopes should show these 3 items.

8. **Configure Additional Settings:**
   - ✅ Check **Require Secret for Web Server Flow**
   - ✅ Check **Require Secret for Refresh Token Flow**
   - ✅ Check **Enable Client Credentials Flow** (important for server-to-server)

9. **Click Save**

10. **Wait for propagation:**

    You'll see a message:
    > "Changes can take up to 10 minutes to take effect"

    In practice, it usually takes 2-5 minutes.

11. **Click Continue**

### Step 1.4: Get Consumer Key and Secret

1. **Go back to App Manager:**
   - Setup → App Manager

2. **Find your app** in the list (`NeuAI CRM Data Mesh`)

3. **Click the dropdown arrow** (▼) on the right side of the row

4. **Click View**

5. **Find the API section:**
   - Look for **Consumer Key** - this is your `SALESFORCE_CLIENT_ID`
   - **Copy it and save it somewhere secure**

6. **Get the Consumer Secret:**
   - Click **Manage Consumer Details**
   - Salesforce will send a verification code to your email
   - Enter the code
   - **Copy the Consumer Secret** - this is your `SALESFORCE_CLIENT_SECRET`

   > ⚠️ **IMPORTANT:** The Consumer Secret is shown only on this screen. Copy it NOW!

### Step 1.5: Get Security Token

The security token is appended to your password for API authentication.

1. **Click your profile picture** (top-right)

2. **Click Settings**

3. **In Quick Find**, type: `Reset My Security Token`

4. **Click Reset My Security Token**

5. **Click Reset Security Token**

6. **Check your email** for a message with subject:
   > "Your new Salesforce security token"

7. **Copy the security token** - this is your `SALESFORCE_SECURITY_TOKEN`

### Step 1.6: Record Your Salesforce Credentials

You should now have:

| Credential | Example | Your Value |
|------------|---------|------------|
| Username | `yourname@neuai-dev.com` | _____________ |
| Password | `MyP@ssw0rd123` | _____________ |
| Security Token | `aB1cD2eF3gH4iJ5k` | _____________ |
| Consumer Key (Client ID) | `3MVG9...` (long string) | _____________ |
| Consumer Secret | `1234567890ABCDEF...` | _____________ |
| Domain | `login` (for production/dev) | `login` |

---

## Part 2: Dynamics 365 Trial

Dynamics 365 requires both a **Microsoft 365 account** and **Azure subscription** for full API access. We'll set up both using free trials.

### Step 2.1: Create Microsoft 365 Developer Account

You have two options:

#### Option A: Microsoft 365 Developer Program (Recommended)

1. **Go to the Developer Program:**
   ```
   https://developer.microsoft.com/en-us/microsoft-365/dev-program
   ```

2. **Click "Join now"**

3. **Sign in or create a Microsoft account**
   - If you don't have one, create a free account at https://account.microsoft.com

4. **Fill in the developer profile:**
   - Country/Region: Your country
   - Company: Your company or `Personal Development`
   - Language: English
   - Check the boxes for terms and communications preferences

5. **Click Next**

6. **Select your focus area:**
   - Choose anything (e.g., "Custom solutions for my organization")

7. **Select areas of interest:**
   - Check "Microsoft Graph" and any others

8. **Click Save**

9. **Set up your E5 sandbox:**
   - Click **Set up E5 subscription**
   - Choose **Instant sandbox** (recommended)
   - Select your country
   - Create an admin username (e.g., `admin`)
   - Your domain will be: `yourdomain.onmicrosoft.com`
   - Create a password

10. **Add phone number for verification**

11. **Wait for sandbox creation** (1-2 minutes)

12. **Record your credentials:**
    - Admin email: `admin@yourdomain.onmicrosoft.com`
    - Password: (what you set)

#### Option B: Dynamics 365 Free Trial (Alternative)

1. **Go to:**
   ```
   https://dynamics.microsoft.com/en-us/dynamics-365-free-trial/
   ```

2. **Select "Sales" or "Customer Service"**

3. **Click "Try for free"**

4. **Enter your work email** (or create a new Microsoft account)

5. **Follow the setup wizard**

### Step 2.2: Set Up Dynamics 365 Environment

1. **Go to Power Platform Admin Center:**
   ```
   https://admin.powerplatform.microsoft.com
   ```

2. **Sign in** with your Microsoft 365 admin account

3. **Check for existing environment:**
   - Click **Environments** in the left sidebar
   - You may already have a default environment

4. **If you need to create a new environment:**
   - Click **+ New**
   - Name: `NeuAI Development`
   - Type: `Trial` or `Sandbox`
   - Region: Select closest to you
   - Enable Dynamics 365 apps: **Yes**
   - Click **Next**
   - Select **Sales Pro** or **Sales Enterprise**
   - Click **Save**

5. **Wait for environment creation** (5-15 minutes)
   - Status will change from "Preparing" to "Ready"

6. **Get your environment URL:**
   - Click on your environment name
   - Look for **Environment URL**
   - It will look like: `https://orgXXXXXXXX.crm.dynamics.com`
   - **Copy this URL** - this is your `DYNAMICS_ENVIRONMENT_URL`

### Step 2.3: Create Azure AD App Registration

1. **Go to Azure Portal:**
   ```
   https://portal.azure.com
   ```

2. **Sign in** with the same Microsoft 365 account

3. **Search for "Azure Active Directory":**
   - Click the search bar at the top
   - Type: `Azure Active Directory`
   - Click **Azure Active Directory**

4. **Navigate to App Registrations:**
   - In the left sidebar, click **App registrations**

5. **Create New Registration:**
   - Click **+ New registration**

6. **Fill in the form:**

   | Field | Value |
   |-------|-------|
   | Name | `NeuAI CRM Data Mesh` |
   | Supported account types | `Accounts in this organizational directory only` (Single tenant) |
   | Redirect URI (optional) | Select `Web` → `https://localhost:8080/oauth/callback` |

7. **Click Register**

8. **Copy the IDs from the Overview page:**

   | Field | Your Value |
   |-------|------------|
   | Application (client) ID | _____________ |
   | Directory (tenant) ID | _____________ |

   These are your `DYNAMICS_CLIENT_ID` and `DYNAMICS_TENANT_ID`

### Step 2.4: Add API Permissions

1. **In your app registration, click "API permissions"** (left sidebar)

2. **Click "+ Add a permission"**

3. **Select "APIs my organization uses"**

4. **Search for "Dynamics CRM":**
   - Type `Dynamics` in the search box
   - Click **Dynamics CRM**

5. **Select permission type:**
   - Click **Delegated permissions**
   - Check ✅ `user_impersonation`
   - Click **Add permissions**

6. **Add Application permissions (for server-to-server):**
   - Click **+ Add a permission** again
   - APIs my organization uses → Dynamics CRM
   - Click **Application permissions**
   - Check ✅ `user_impersonation`
   - Click **Add permissions**

7. **Grant Admin Consent:**
   - Click the button: **Grant admin consent for [Your Organization]**
   - Click **Yes** to confirm
   - All permissions should now show ✅ green checkmarks

### Step 2.5: Create Client Secret

1. **Click "Certificates & secrets"** (left sidebar)

2. **Click "+ New client secret"**

3. **Fill in:**
   - Description: `NeuAI CRM Mesh Dev`
   - Expires: `6 months` (or longer for development)

4. **Click Add**

5. **IMMEDIATELY copy the Value:**

   | Field | What it is |
   |-------|------------|
   | Value | `abc123~xxxxxxxxxxxxx` ← **COPY THIS NOW!** |
   | Secret ID | (not the secret itself, just an identifier) |

   > ⚠️ **CRITICAL:** The secret value is shown **ONLY ONCE**. If you navigate away, you cannot retrieve it and must create a new one.

   This is your `DYNAMICS_CLIENT_SECRET`

### Step 2.6: Create Application User in Dynamics 365

This step grants your Azure AD app access to Dynamics 365 data.

1. **Go to Power Platform Admin Center:**
   ```
   https://admin.powerplatform.microsoft.com
   ```

2. **Click "Environments"**

3. **Click on your environment name**

4. **Click "Settings"** (top toolbar)

5. **Expand "Users + permissions"**

6. **Click "Application users"**

7. **Click "+ New app user"**

8. **Add your app:**
   - Click **+ Add an app**
   - Search for `NeuAI CRM Data Mesh`
   - Select it
   - Click **Add**

9. **Select Business Unit:**
   - Choose your organization's root business unit

10. **Assign Security Roles:**
    - Click the **pencil icon** (✏️) next to "Security roles"
    - For development, add: **System Administrator**
    - For production, add appropriate roles like: **Salesperson**, **Sales Manager**
    - Click **Save**

11. **Click "Create"**

### Step 2.7: Record Your Dynamics 365 Credentials

You should now have:

| Credential | Example | Your Value |
|------------|---------|------------|
| Client ID | `12345678-1234-1234-1234-123456789abc` | _____________ |
| Client Secret | `abc123~xxxxxxxxxxxxxx` | _____________ |
| Tenant ID | `abcdefgh-1234-5678-9abc-def012345678` | _____________ |
| Environment URL | `https://orgXXXXXXXX.crm.dynamics.com` | _____________ |

---

## Part 3: Configure Environment

Now let's configure NeuAI CRM Data Mesh with your credentials.

### Step 3.1: Create .env File

1. **Navigate to the project directory:**
   ```bash
   cd /Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/neuai-crm-mesh
   ```

2. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the .env file:**
   ```bash
   nano .env
   # or use your preferred editor:
   # code .env
   # vim .env
   ```

### Step 3.2: Fill in Salesforce Credentials

Update these lines with your values:

```bash
# ----- Salesforce Configuration -----
SALESFORCE_CLIENT_ID=3MVG9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SALESFORCE_CLIENT_SECRET=1234567890ABCDEF1234567890ABCDEF12345678
SALESFORCE_USERNAME=yourname@neuai-dev.com
SALESFORCE_PASSWORD=YourActualPassword123
SALESFORCE_SECURITY_TOKEN=aB1cD2eF3gH4iJ5kL6mN7oP8

# Salesforce Domain
SALESFORCE_DOMAIN=login
```

> **Note:** For the password, use your actual Salesforce password WITHOUT the security token appended. The code will handle combining them.

### Step 3.3: Fill in Dynamics 365 Credentials

Update these lines with your values:

```bash
# ----- Dynamics 365 Configuration -----
DYNAMICS_CLIENT_ID=12345678-1234-1234-1234-123456789abc
DYNAMICS_CLIENT_SECRET=abc123~xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DYNAMICS_TENANT_ID=abcdefgh-1234-5678-9abc-def012345678
DYNAMICS_ENVIRONMENT_URL=https://orgXXXXXXXX.crm.dynamics.com
```

### Step 3.4: Verify .env File

Your complete `.env` file should look similar to this:

```bash
# ===========================================
# NeuAI CRM Data Mesh - Environment Configuration
# ===========================================

# ----- Salesforce Configuration -----
SALESFORCE_CLIENT_ID=3MVG9abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
SALESFORCE_CLIENT_SECRET=ABCDEF123456789ABCDEF123456789AB
SALESFORCE_USERNAME=admin@neuai-dev.com
SALESFORCE_PASSWORD=MySecureP@ssw0rd!
SALESFORCE_SECURITY_TOKEN=xYz123AbC456DeF789
SALESFORCE_DOMAIN=login
SALESFORCE_API_VERSION=v59.0

# ----- Dynamics 365 Configuration -----
DYNAMICS_CLIENT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890
DYNAMICS_CLIENT_SECRET=Abc123~xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DYNAMICS_TENANT_ID=98765432-abcd-ef12-3456-7890abcdef12
DYNAMICS_ENVIRONMENT_URL=https://org12345678.crm.dynamics.com
DYNAMICS_API_VERSION=v9.2

# ----- Server Configuration -----
HOST=0.0.0.0
PORT=8080
DEBUG=true

# ----- Logging -----
LOG_LEVEL=DEBUG

# ----- Other Settings -----
CORS_ORIGINS=*
DATA_DIR=./data
ENABLE_AI_QUERIES=true
DUPLICATE_THRESHOLD=0.8
```

### Step 3.5: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install base requirements
pip install -r requirements.txt

# Install CRM connector dependencies
pip install simple-salesforce msal requests python-dotenv
```

---

## Part 4: Test Connections

### Step 4.1: Create Test Script

Create a file called `test_connections.py`:

```bash
cat > test_connections.py << 'EOF'
#!/usr/bin/env python3
"""Test connections to Salesforce and Dynamics 365."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_salesforce():
    """Test Salesforce connection."""
    print("\n" + "="*50)
    print("Testing Salesforce Connection")
    print("="*50)

    try:
        from simple_salesforce import Salesforce

        # Get credentials
        username = os.getenv('SALESFORCE_USERNAME')
        password = os.getenv('SALESFORCE_PASSWORD')
        token = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
        client_id = os.getenv('SALESFORCE_CLIENT_ID')
        domain = os.getenv('SALESFORCE_DOMAIN', 'login')

        print(f"Username: {username}")
        print(f"Domain: {domain}.salesforce.com")
        print(f"Client ID: {client_id[:20]}..." if client_id else "Client ID: NOT SET")

        # Connect
        print("\nConnecting...")
        sf = Salesforce(
            username=username,
            password=password + token,
            consumer_key=client_id,
            consumer_secret=os.getenv('SALESFORCE_CLIENT_SECRET'),
            domain=domain
        )

        print(f"✅ Connected to Salesforce!")
        print(f"   Instance: {sf.sf_instance}")
        print(f"   API Version: {sf.sf_version}")

        # Test query
        print("\nQuerying accounts...")
        result = sf.query("SELECT Id, Name FROM Account LIMIT 5")
        print(f"✅ Query successful! Found {result['totalSize']} accounts")

        for record in result['records']:
            print(f"   - {record['Name']}")

        return True

    except Exception as e:
        print(f"❌ Salesforce Error: {e}")
        return False


def test_dynamics():
    """Test Dynamics 365 connection."""
    print("\n" + "="*50)
    print("Testing Dynamics 365 Connection")
    print("="*50)

    try:
        import requests
        from msal import ConfidentialClientApplication

        # Get credentials
        client_id = os.getenv('DYNAMICS_CLIENT_ID')
        client_secret = os.getenv('DYNAMICS_CLIENT_SECRET')
        tenant_id = os.getenv('DYNAMICS_TENANT_ID')
        env_url = os.getenv('DYNAMICS_ENVIRONMENT_URL', '').rstrip('/')

        print(f"Client ID: {client_id}")
        print(f"Tenant ID: {tenant_id}")
        print(f"Environment: {env_url}")

        if not all([client_id, client_secret, tenant_id, env_url]):
            print("❌ Missing credentials! Check your .env file.")
            return False

        # Get access token
        print("\nAcquiring access token...")
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        scope = [f"{env_url}/.default"]

        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority
        )

        result = app.acquire_token_for_client(scopes=scope)

        if 'access_token' not in result:
            print(f"❌ Token Error: {result.get('error_description', 'Unknown error')}")
            return False

        print("✅ Access token acquired!")

        # Test API call
        print("\nCalling WhoAmI endpoint...")
        headers = {
            'Authorization': f"Bearer {result['access_token']}",
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json'
        }

        response = requests.get(
            f"{env_url}/api/data/v9.2/WhoAmI",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connected to Dynamics 365!")
            print(f"   User ID: {data.get('UserId')}")
            print(f"   Organization: {data.get('OrganizationId')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   {response.text}")
            return False

        # Test query
        print("\nQuerying accounts...")
        response = requests.get(
            f"{env_url}/api/data/v9.2/accounts?$top=5&$select=name",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            accounts = data.get('value', [])
            print(f"✅ Query successful! Found {len(accounts)} accounts")
            for account in accounts:
                print(f"   - {account.get('name', 'Unnamed')}")
        else:
            print(f"⚠️  Query returned {response.status_code} (may be empty org)")

        return True

    except Exception as e:
        print(f"❌ Dynamics 365 Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all connection tests."""
    print("\n" + "#"*50)
    print("# NeuAI CRM Data Mesh - Connection Tests")
    print("#"*50)

    sf_ok = test_salesforce()
    d365_ok = test_dynamics()

    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    print(f"Salesforce:   {'✅ Connected' if sf_ok else '❌ Failed'}")
    print(f"Dynamics 365: {'✅ Connected' if d365_ok else '❌ Failed'}")
    print("="*50)

    if sf_ok and d365_ok:
        print("\n🎉 All connections successful! You're ready to use NeuAI CRM Data Mesh.")
        return 0
    else:
        print("\n⚠️  Some connections failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
EOF
```

### Step 4.2: Run the Test

```bash
python3 test_connections.py
```

### Expected Output (Success)

```
##################################################
# NeuAI CRM Data Mesh - Connection Tests
##################################################

==================================================
Testing Salesforce Connection
==================================================
Username: admin@neuai-dev.com
Domain: login.salesforce.com
Client ID: 3MVG9abc123def456...

Connecting...
✅ Connected to Salesforce!
   Instance: na123.salesforce.com
   API Version: 59.0

Querying accounts...
✅ Query successful! Found 5 accounts
   - Acme Corporation
   - Global Media
   - United Partners
   - Edge Communications
   - Burlington Textiles

==================================================
Testing Dynamics 365 Connection
==================================================
Client ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Tenant ID: 98765432-abcd-ef12-3456-7890abcdef12
Environment: https://org12345678.crm.dynamics.com

Acquiring access token...
✅ Access token acquired!

Calling WhoAmI endpoint...
✅ Connected to Dynamics 365!
   User ID: 12345678-abcd-ef12-3456-7890abcdef12
   Organization: 87654321-dcba-21fe-6543-210987fedcba

Querying accounts...
✅ Query successful! Found 3 accounts
   - Contoso Ltd
   - Adventure Works
   - Fabrikam Inc

==================================================
Summary
==================================================
Salesforce:   ✅ Connected
Dynamics 365: ✅ Connected
==================================================

🎉 All connections successful! You're ready to use NeuAI CRM Data Mesh.
```

### Troubleshooting Test Failures

#### Salesforce Errors

| Error | Solution |
|-------|----------|
| `INVALID_LOGIN: Invalid username, password, security token` | Check username, password, and security token. Reset token if needed. |
| `INVALID_CLIENT_ID` | Wait 10 minutes for Connected App to propagate, or verify Consumer Key. |
| `API_DISABLED_FOR_ORG` | Your org doesn't have API access. Use Developer Edition. |

#### Dynamics 365 Errors

| Error | Solution |
|-------|----------|
| `AADSTS7000215: Invalid client secret` | Secret may have expired. Create a new one in Azure AD. |
| `AADSTS700016: Application not found` | Check Client ID and Tenant ID are correct. |
| `AADSTS65001: User or admin has not consented` | Go to API Permissions and click "Grant admin consent". |
| `403 Forbidden` | Application User missing or no security role assigned. |
| `401 Unauthorized` | Token invalid. Check credentials and try again. |

---

## Part 5: Load Sample Data

Trial instances often come with sample data, but let's add some consistent test data.

### Step 5.1: Add Sample Data to Salesforce

1. **Open Salesforce** and log in

2. **Go to Setup → Data → Data Import Wizard**
   - Or search "Import" in Quick Find

3. **Or manually create test records:**

   **Create an Account:**
   - Click the **App Launcher** (grid icon)
   - Click **Sales** → **Accounts**
   - Click **New**
   - Name: `NeuAI Test Company`
   - Click **Save**

   **Create a Contact:**
   - Go to **Contacts** → **New**
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john.doe@neuai-test.com`
   - Account: `NeuAI Test Company`
   - Click **Save**

   **Create an Opportunity:**
   - Go to **Opportunities** → **New**
   - Name: `NeuAI Demo Deal`
   - Account: `NeuAI Test Company`
   - Close Date: (30 days from now)
   - Stage: `Prospecting`
   - Amount: `50000`
   - Click **Save**

### Step 5.2: Add Sample Data to Dynamics 365

1. **Open Dynamics 365:**
   - Go to your environment URL
   - Or from Power Platform Admin Center, click **Open**

2. **Open Sales Hub:**
   - Click the app selector (grid in top-left)
   - Select **Sales Hub**

3. **Create an Account:**
   - Click **Accounts** in the left navigation
   - Click **+ New**
   - Name: `NeuAI Test Company`
   - Click **Save & Close**

4. **Create a Contact:**
   - Click **Contacts** → **+ New**
   - First Name: `Jane`
   - Last Name: `Smith`
   - Email: `jane.smith@neuai-test.com`
   - Company: `NeuAI Test Company`
   - Click **Save & Close**

5. **Create an Opportunity:**
   - Click **Opportunities** → **+ New**
   - Topic: `NeuAI Demo Deal`
   - Account: `NeuAI Test Company`
   - Est. Close Date: (30 days from now)
   - Est. Revenue: `75000`
   - Click **Save & Close**

### Step 5.3: Test with CLI

Now test the NeuAI CRM Data Mesh CLI:

```bash
cd /Users/kodywildfeuer/Documents/GitHub/m365-agents-for-python/localFirstTools/neuai-crm-mesh

# Check stats (using local files first)
python3 -m neuai_crm stats \
  --salesforce examples/salesforce-data.json \
  --dynamics examples/dynamics-data.json \
  --local examples/local-data.json

# Detect duplicates
python3 -m neuai_crm detect-duplicates \
  --salesforce examples/salesforce-data.json \
  --dynamics examples/dynamics-data.json

# Translate data format
python3 -m neuai_crm translate \
  --from salesforce \
  --to dynamics365 \
  --file examples/salesforce-data.json
```

---

## Appendix: Credential Reference

### Complete Credentials Checklist

#### Salesforce
| Credential | Where to Get | Your Value |
|------------|--------------|------------|
| Username | Your Salesforce login (email format) | |
| Password | Your Salesforce password | |
| Security Token | Settings → Reset My Security Token | |
| Consumer Key | App Manager → View App → API section | |
| Consumer Secret | App Manager → Manage Consumer Details | |
| Domain | `login` (prod) or `test` (sandbox) | |

#### Dynamics 365
| Credential | Where to Get | Your Value |
|------------|--------------|------------|
| Client ID | Azure AD → App registrations → Overview | |
| Client Secret | Azure AD → Certificates & secrets | |
| Tenant ID | Azure AD → App registrations → Overview | |
| Environment URL | Power Platform Admin → Environments | |

### Environment Variable Reference

```bash
# Salesforce
SALESFORCE_CLIENT_ID=        # Consumer Key from Connected App
SALESFORCE_CLIENT_SECRET=    # Consumer Secret
SALESFORCE_USERNAME=         # Your Salesforce username
SALESFORCE_PASSWORD=         # Your Salesforce password
SALESFORCE_SECURITY_TOKEN=   # Security token from email
SALESFORCE_DOMAIN=login      # 'login' or 'test' or custom domain

# Dynamics 365
DYNAMICS_CLIENT_ID=          # Application (client) ID
DYNAMICS_CLIENT_SECRET=      # Client secret value
DYNAMICS_TENANT_ID=          # Directory (tenant) ID
DYNAMICS_ENVIRONMENT_URL=    # https://orgXXXXXXXX.crm.dynamics.com
```

### Quick Links

| Service | URL |
|---------|-----|
| Salesforce Developer Signup | https://developer.salesforce.com/signup |
| Salesforce Login | https://login.salesforce.com |
| Microsoft 365 Developer Program | https://developer.microsoft.com/microsoft-365/dev-program |
| Azure Portal | https://portal.azure.com |
| Power Platform Admin Center | https://admin.powerplatform.microsoft.com |
| Dynamics 365 Trial | https://dynamics.microsoft.com/dynamics-365-free-trial/ |

---

## Next Steps

Now that you have working connections to both CRMs:

1. **Explore the API** - Try different CLI commands
2. **Build integrations** - Use the connector classes in your code
3. **Set up webhooks** - For real-time sync (advanced)
4. **Add more users** - Test with multiple user scenarios

For questions or issues, see `docs/ONBOARDING-GUIDE.md` for troubleshooting tips.

---

*Guide created: December 2024*
*Tested with: Salesforce API v59.0, Dynamics 365 API v9.2*
