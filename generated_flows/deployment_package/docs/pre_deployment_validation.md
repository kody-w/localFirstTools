# Pre-Deployment Validation Guide
## AutomatedMeetingNotesEmailer Flow

**Document Version**: 1.0
**Generated**: 2025-10-14
**Flow**: AutomatedMeetingNotesEmailer

---

## Overview

This document provides comprehensive pre-deployment validation procedures to ensure successful deployment of the AutomatedMeetingNotesEmailer flow to Microsoft Power Platform environments.

---

## Prerequisites Checklist

### System Requirements

- [ ] **Power Platform CLI (pac) installed**
  ```bash
  # Check installation
  pac --version

  # Required version: 1.30.0 or higher
  # Install from: https://aka.ms/PowerPlatformCLI
  ```

- [ ] **Environment Access**
  - User has System Administrator or System Customizer role
  - User can create and modify solutions
  - User can import flows
  - User can create connections

- [ ] **Microsoft 365 Subscription**
  - Valid Office 365 / Microsoft 365 subscription
  - Exchange Online service enabled
  - User mailbox provisioned and active

- [ ] **Network Connectivity**
  - Access to Power Platform environments
  - Access to Microsoft 365 services
  - No firewall blocking Power Platform domains
  - No proxy issues

### Tool Requirements

- [ ] **jq (JSON processor)** - for JSON validation
  ```bash
  # macOS
  brew install jq

  # Ubuntu/Debian
  sudo apt-get install jq

  # Verify
  jq --version
  ```

- [ ] **zip/unzip** - for solution packaging
  ```bash
  # Verify
  zip --version
  unzip --version
  ```

- [ ] **curl** - for API testing
  ```bash
  # Verify
  curl --version
  ```

---

## Environment Validation

### Step 1: Authenticate to Power Platform

```bash
# Interactive authentication
pac auth create --url https://your-org.crm.dynamics.com

# Service principal authentication (recommended for CI/CD)
pac auth create --kind SERVICEPRINCIPALSECRET \
  --url https://your-org.crm.dynamics.com \
  --applicationId <app-id> \
  --clientSecret <secret> \
  --tenant <tenant-id>

# Verify authentication
pac auth list
pac org who
```

**Expected Output:**
```
Connected as: user@contoso.com
Organization: Contoso Development
Environment: https://contoso-dev.crm.dynamics.com
Version: 9.2.x.x
```

**Validation Criteria:**
- ✓ Authentication successful
- ✓ User has appropriate role
- ✓ Environment is accessible
- ✓ Environment version is compatible

### Step 2: Verify Environment Capabilities

```bash
# List available connectors
pac connector list | head -n 20

# Check for Office 365 Outlook connector
pac connector list | grep -i "office365"

# Verify solution capabilities
pac solution list
```

**Expected Results:**
- Office 365 Outlook connector is available
- User can list solutions in environment
- No authentication errors

### Step 3: Check Environment Capacity

```bash
# Check environment details
pac org who

# List existing solutions (to check for conflicts)
pac solution list | grep -i "meeting"
```

**Validation Criteria:**
- ✓ Environment has available capacity
- ✓ No conflicting solution with same name exists
- ✓ API call quota is sufficient

---

## Flow Validation

### Step 1: Validate Flow JSON Structure

```bash
# Navigate to flow directory
cd /Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows

# Validate JSON syntax
jq empty AutomatedMeetingNotesEmailer.json

# Extract and verify required fields
jq '.properties.templateName' AutomatedMeetingNotesEmailer.json
jq '.properties.connectionReferences' AutomatedMeetingNotesEmailer.json
jq '.properties.definition.triggers' AutomatedMeetingNotesEmailer.json
```

**Expected Output:**
```json
"Automated Meeting Notes Emailer"
{
  "shared_office365": {
    "runtimeSource": "embedded",
    "connection": {...},
    "api": {...}
  }
}
```

**Validation Criteria:**
- ✓ JSON is syntactically valid
- ✓ Template name is present
- ✓ Connection references are defined
- ✓ Triggers are defined
- ✓ Actions are defined

### Step 2: Verify Connection Requirements

```bash
# Extract connection references
jq '.properties.connectionReferences | keys[]' AutomatedMeetingNotesEmailer.json

# Expected: shared_office365

# Check connection availability in environment
pac connection list | grep -i "office365"
```

**Validation Criteria:**
- ✓ All required connectors are identified
- ✓ Connectors are available in target environment
- ✓ User has license to use connectors (all are standard)

### Step 3: Validate Trigger Configuration

```bash
# Extract trigger information
jq '.properties.definition.triggers' AutomatedMeetingNotesEmailer.json

# Verify trigger type
jq '.properties.definition.triggers.manual.type' AutomatedMeetingNotesEmailer.json
# Expected: "Request"

# Verify input schema
jq '.properties.definition.triggers.manual.inputs.schema' AutomatedMeetingNotesEmailer.json
```

**Validation Criteria:**
- ✓ Trigger type is valid (Request/HTTP)
- ✓ Input schema is well-formed
- ✓ Required fields are defined

### Step 4: Validate Action Sequence

```bash
# List all actions
jq '.properties.definition.actions | keys[]' AutomatedMeetingNotesEmailer.json

# Expected actions:
# - Parse_JSON_-_Meeting_Data
# - Initialize_Variable_-_Email_Recipients
# - Initialize_Variable_-_Action_Items_HTML
# - Condition_-_Check_Action_Items
# - Compose_-_Email_Body
# - Send_an_email_(V2)
# - Response_-_Success

# Count actions
jq '.properties.definition.actions | length' AutomatedMeetingNotesEmailer.json
# Expected: 7 actions
```

**Validation Criteria:**
- ✓ All expected actions are present
- ✓ Action dependencies are properly sequenced
- ✓ No orphaned or unreachable actions

---

## Connection Validation

### Step 1: Check Existing Connections

```bash
# List all connections in environment
pac connection list

# Filter for Office 365 connections
pac connection list | grep -i "office365"

# Get connection details (replace <CONNECTION-ID> with actual ID)
# pac connection show --connection-id <CONNECTION-ID>
```

**If No Connection Exists:**
```bash
# Create new Office 365 connection
pac connection create --connector shared_office365 --environment <ENV-ID>

# This will open browser for OAuth authentication
# Sign in with Microsoft 365 account
# Grant required permissions (Mail.Send)
```

**Validation Criteria:**
- ✓ Office 365 Outlook connection exists OR can be created
- ✓ Connection is active (not expired or disabled)
- ✓ Connection owner has proper permissions
- ✓ Connection can send emails

### Step 2: Test Connection Functionality

Manual test via Power Automate portal:
1. Open https://make.powerautomate.com
2. Navigate to Data > Connections
3. Find Office 365 Outlook connection
4. Click "..." menu > Test
5. Verify connection test succeeds

**Validation Criteria:**
- ✓ Connection test passes
- ✓ No authentication errors
- ✓ User has Mail.Send permission

---

## Solution Validation

### Step 1: Check for Existing Solution

```bash
# Check if solution already exists
pac solution list | grep -i "MeetingAutomation"

# If exists, export backup
# pac solution export --name "MeetingAutomation" \
#   --path ./backup_$(date +%Y%m%d_%H%M%S).zip --managed false
```

**If Solution Exists:**
- Document current version
- Create backup before proceeding
- Plan for upgrade vs. new installation
- Check for dependent components

**If Solution Does Not Exist:**
- Proceed with new solution creation
- No backup needed
- Clean installation path

### Step 2: Validate Solution Structure

```bash
# Navigate to deployment package
cd /Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/deployment_package

# Verify directory structure
ls -la scripts/
ls -la config/
ls -la reports/

# Check script permissions
ls -l scripts/deployment_script.sh
ls -l scripts/rollback_script.sh

# Make executable if needed
chmod +x scripts/deployment_script.sh
chmod +x scripts/rollback_script.sh
```

**Expected Structure:**
```
deployment_package/
├── scripts/
│   ├── deployment_script.sh (executable)
│   └── rollback_script.sh (executable)
├── config/
│   └── connection-mapping.json
├── reports/
│   ├── flow_analysis_report.md
│   └── deployment_readiness_checklist.md
├── pipelines/
│   ├── azure-pipelines.yml
│   └── github-actions-deploy.yml
└── docs/
    ├── pre_deployment_validation.md
    └── post_deployment_verification.md
```

**Validation Criteria:**
- ✓ All required files present
- ✓ Scripts are executable
- ✓ Configuration files are valid JSON
- ✓ Documentation is complete

---

## Security Validation

### Step 1: Review Security Requirements

```bash
# Check current user permissions
pac org who

# Verify user role assignments
# (This is done via Power Platform Admin Center)
```

**Required Permissions:**
- System Administrator OR System Customizer role
- Ability to create/modify solutions
- Ability to import flows
- Ability to create connections
- Ability to assign connection references

### Step 2: Validate Service Principal (if using for CI/CD)

```bash
# Test service principal authentication
pac auth create --kind SERVICEPRINCIPALSECRET \
  --url https://your-org.crm.dynamics.com \
  --applicationId <app-id> \
  --clientSecret <secret> \
  --tenant <tenant-id>

# Verify service principal has required permissions
pac org who
```

**Required Service Principal Permissions:**
- System Administrator or System Customizer role in environment
- Azure AD application permissions configured
- Client secret not expired
- Service principal not disabled

### Step 3: Data Privacy and Compliance

**Review Data Handling:**
- Personal data: Email addresses, names
- Meeting content: Notes, action items
- Data retention: No data stored (transient processing)
- GDPR compliance: Personal data processed but not stored

**Security Controls:**
- [ ] HTTP trigger authentication configured
- [ ] API access restricted to authorized apps
- [ ] Connection uses OAuth (no hardcoded credentials)
- [ ] Run history retention policy defined
- [ ] Audit logging enabled

---

## Network and Connectivity Validation

### Step 1: Test Power Platform Connectivity

```bash
# Test environment URL accessibility
curl -I https://your-org.crm.dynamics.com

# Expected: HTTP 200 or 301/302 redirect
```

### Step 2: Test Microsoft 365 Connectivity

```bash
# Test Outlook service
curl -I https://outlook.office365.com

# Test authentication endpoint
curl -I https://login.microsoftonline.com
```

**Validation Criteria:**
- ✓ Power Platform environment is accessible
- ✓ Microsoft 365 services are accessible
- ✓ No network timeouts or errors
- ✓ No proxy or firewall blocking

---

## Test Data Preparation

### Step 1: Prepare Sample Test Payload

Create file: `test_payload.json`
```json
{
  "meeting_title": "Pre-Deployment Test Meeting",
  "participants": [
    "test.user1@contoso.com",
    "test.user2@contoso.com"
  ],
  "notes": "This is a test meeting to verify the AutomatedMeetingNotesEmailer flow deployment. If you receive this email, the flow is working correctly.",
  "action_items": [
    {
      "task": "Verify email formatting",
      "assignee": "test.user1@contoso.com",
      "due_date": "2025-10-15"
    },
    {
      "task": "Check action items display",
      "assignee": "test.user2@contoso.com",
      "due_date": "2025-10-16"
    }
  ]
}
```

### Step 2: Validate Test Payload

```bash
# Validate test payload JSON
jq empty test_payload.json

# Verify required fields
jq 'has("meeting_title") and has("participants") and has("notes")' test_payload.json
# Expected: true

# Verify array structures
jq '.participants | type' test_payload.json
# Expected: "array"

jq '.action_items | type' test_payload.json
# Expected: "array"
```

### Step 3: Prepare Test Email Recipients

**Important:**
- Use test email accounts, not production users
- Verify test users can receive emails
- Document test user email addresses
- Ensure test users are aware of test emails

---

## Deployment Script Validation

### Step 1: Validate Deployment Script Syntax

```bash
# Check bash syntax
bash -n scripts/deployment_script.sh

# Expected: No output (syntax is valid)

# Check for required commands
grep -E "pac|jq|zip" scripts/deployment_script.sh | wc -l
# Should find multiple references

# Verify environment variable usage
grep -E "TARGET_ENV_URL|SOLUTION_NAME" scripts/deployment_script.sh | wc -l
# Should find multiple references
```

### Step 2: Dry-Run the Deployment Script

```bash
# Set required environment variables
export TARGET_ENV_URL="https://your-org-dev.crm.dynamics.com"
export SOLUTION_NAME="MeetingAutomation"
export DEPLOYMENT_TYPE="unmanaged"

# Run deployment script (already in DRY-RUN mode)
cd scripts/
./deployment_script.sh
```

**Expected Results:**
- ✓ All validation steps pass
- ✓ No errors in log file
- ✓ Solution package created
- ✓ Deployment steps documented

### Step 3: Validate Rollback Script

```bash
# Check rollback script syntax
bash -n scripts/rollback_script.sh

# Expected: No output (syntax is valid)

# Review rollback logic
grep -E "rollback|backup|restore" scripts/rollback_script.sh | wc -l
# Should find multiple references
```

---

## Final Pre-Deployment Checklist

### Environment Readiness

- [ ] pac CLI installed and updated (v1.30.0+)
- [ ] User authenticated to target environment
- [ ] User has System Administrator or System Customizer role
- [ ] Environment capacity verified
- [ ] Network connectivity confirmed

### Flow Readiness

- [ ] Flow JSON validated (syntax and structure)
- [ ] Connection requirements identified
- [ ] All required connectors available
- [ ] Trigger configuration verified
- [ ] Action sequence validated

### Connection Readiness

- [ ] Office 365 Outlook connector available
- [ ] Connection exists OR can be created
- [ ] Connection test passed
- [ ] User has Mail.Send permission
- [ ] Connection owner documented

### Solution Readiness

- [ ] Solution name confirmed (no conflicts)
- [ ] Backup created (if updating existing solution)
- [ ] Solution structure validated
- [ ] Deployment scripts ready and executable
- [ ] Rollback script ready

### Security Readiness

- [ ] Security requirements reviewed
- [ ] User permissions validated
- [ ] Service principal configured (if using CI/CD)
- [ ] Data privacy considerations documented
- [ ] Audit logging enabled

### Test Readiness

- [ ] Test payload prepared and validated
- [ ] Test email recipients identified
- [ ] Test accounts notified
- [ ] Test plan documented
- [ ] Success criteria defined

### Documentation Readiness

- [ ] Flow analysis report reviewed
- [ ] Deployment readiness checklist completed
- [ ] Pre-deployment validation guide reviewed
- [ ] Post-deployment verification plan ready
- [ ] Rollback procedures documented

---

## Validation Report Template

```markdown
# Pre-Deployment Validation Report

**Date**: [DATE]
**Validator**: [NAME]
**Environment**: [ENV NAME]
**Flow**: AutomatedMeetingNotesEmailer

## Validation Results

### Prerequisites
- [ ] Pass / [ ] Fail - pac CLI installed
- [ ] Pass / [ ] Fail - Environment access
- [ ] Pass / [ ] Fail - Microsoft 365 subscription
- [ ] Pass / [ ] Fail - Network connectivity

### Flow Validation
- [ ] Pass / [ ] Fail - JSON structure valid
- [ ] Pass / [ ] Fail - Connection requirements met
- [ ] Pass / [ ] Fail - Trigger configuration verified
- [ ] Pass / [ ] Fail - Action sequence validated

### Connection Validation
- [ ] Pass / [ ] Fail - Office 365 connection exists/created
- [ ] Pass / [ ] Fail - Connection test passed
- [ ] Pass / [ ] Fail - Permissions verified

### Solution Validation
- [ ] Pass / [ ] Fail - No naming conflicts
- [ ] Pass / [ ] Fail - Backup created (if needed)
- [ ] Pass / [ ] Fail - Deployment scripts ready

### Security Validation
- [ ] Pass / [ ] Fail - User permissions verified
- [ ] Pass / [ ] Fail - Security requirements met
- [ ] Pass / [ ] Fail - Compliance considerations reviewed

## Issues Identified

[List any issues found during validation]

## Remediation Actions

[List actions taken to resolve issues]

## Deployment Recommendation

[ ] APPROVED - Ready for deployment
[ ] CONDITIONAL - Ready with noted caveats
[ ] NOT APPROVED - Issues must be resolved

**Approver Signature**: _______________
**Date**: _______________
```

---

## Troubleshooting Common Validation Issues

### Issue: pac CLI Not Found

**Symptom**: `pac: command not found`

**Solution**:
```bash
# Install pac CLI
dotnet tool install --global Microsoft.PowerApps.CLI.Tool

# Add to PATH (if needed)
export PATH="$PATH:$HOME/.dotnet/tools"

# Verify installation
pac --version
```

### Issue: Authentication Fails

**Symptom**: `Authentication failed` or `Invalid credentials`

**Solutions**:
1. Verify environment URL is correct
2. Check user has appropriate role
3. Try re-authenticating:
   ```bash
   pac auth clear
   pac auth create --url <env-url>
   ```
4. Check network connectivity
5. Verify Azure AD tenant is correct

### Issue: Connector Not Available

**Symptom**: `Connector not found` or connector not listed

**Solutions**:
1. Check connector is enabled in Power Platform Admin Center
2. Verify licensing (Office 365 Outlook is standard)
3. Wait for environment provisioning to complete (new environments)
4. Check firewall/proxy settings

### Issue: JSON Validation Fails

**Symptom**: `parse error: Invalid JSON` from jq

**Solutions**:
1. Check for syntax errors (missing commas, brackets)
2. Verify file encoding (UTF-8)
3. Use online JSON validator for detailed errors
4. Re-export flow JSON from source

### Issue: Permission Denied

**Symptom**: `Access denied` or `Insufficient permissions`

**Solutions**:
1. Verify user role (need System Administrator or System Customizer)
2. Check Azure AD group memberships
3. Request role assignment from administrator
4. Verify service principal permissions (if using)

---

## Next Steps

After completing all validation steps:

1. **Review Validation Results**: Ensure all checks passed
2. **Document Issues**: Record any issues and resolutions
3. **Obtain Approvals**: Get required sign-offs
4. **Schedule Deployment**: Choose appropriate maintenance window
5. **Notify Stakeholders**: Inform relevant parties of deployment
6. **Proceed to Deployment**: Execute deployment script
7. **Monitor Execution**: Watch for errors during deployment
8. **Perform Post-Deployment Verification**: Follow verification guide

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-14 | Power Platform Deployment Agent | Initial version |

**Related Documents**:
- Flow Analysis Report
- Deployment Readiness Checklist
- Post-Deployment Verification Guide
- Deployment Script Documentation
- Rollback Procedures
