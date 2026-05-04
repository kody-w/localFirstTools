# CRM & Workflow Sample Files

These sample JSON files are designed to test the cross-platform sync and translation capabilities of the local-first CRM simulators and workflow translator.

## CRM Sample Data

All three files contain the **same data** in different platform formats - perfect for testing import/export between systems:

| File | Platform | Import Into |
|------|----------|-------------|
| `crm-sample-local.json` | Local-First CRM | `local-first-crm.html` |
| `crm-sample-salesforce.json` | Salesforce | `salesforce-simulator.html` |
| `crm-sample-dynamics365.json` | Dynamics 365 | `dynamics365-powerplatform.html` |

### Sample Data Contents

- **3 Companies/Accounts**: Acme Corporation, Globex Industries, Stark Innovations
- **4 Contacts**: Sarah Chen, Marcus Johnson, Elena Rodriguez, David Kim
- **4 Deals/Opportunities**: Various stages from qualified to won
- **5 Activities/Tasks**: Calls, emails, and meetings

### Testing Cross-Platform Sync

1. **Import into any CRM**: Open one of the CRM simulators and import the corresponding JSON file
2. **Export to different format**: Use the export buttons to export in a different platform's format
3. **Import into target CRM**: Import the exported file into the target CRM simulator
4. **Verify data integrity**: Check that all records, relationships, and field values are preserved

## Workflow Sample Files

| File | Platform | Import Into |
|------|----------|-------------|
| `workflow-sample-power-automate.json` | Power Automate (Logic Apps) | `lowcode-workflow-translator.html` |
| `workflow-sample-n8n.json` | n8n | `lowcode-workflow-translator.html` |

### Sample Workflow: New Contact Onboarding

Both workflow files implement the **same business logic**:

1. **Trigger**: When a new contact is created
2. **Condition**: Check if contact is a VIP (job title contains "CEO")
3. **If VIP**:
   - Send notification email to sales team
   - Create follow-up task for 3 days out
4. **If not VIP**:
   - Send standard welcome email
5. **Always**: Log the event to audit system

### Testing Workflow Translation

1. Open `lowcode-workflow-translator.html`
2. Drag and drop any workflow file onto the import zone
3. View the workflow in the visual builder
4. See real-time translations in all three formats:
   - Power Automate (JSON)
   - Salesforce Flow (XML)
   - n8n (JSON)
5. Export in any format for use in production systems

## Schema Mapping Reference

### Entities

| Local CRM | Salesforce | Dynamics 365 |
|-----------|------------|--------------|
| companies | Account | account |
| contacts | Contact | contact |
| deals | Opportunity | opportunity |
| activities | Task | activitypointer |

### Key Fields

| Concept | Local CRM | Salesforce | Dynamics 365 |
|---------|-----------|------------|--------------|
| First Name | firstName | FirstName | firstname |
| Last Name | lastName | LastName | lastname |
| Email | email | Email | emailaddress1 |
| Phone | phone | Phone | telephone1 |
| Company Link | companyId | AccountId | parentcustomerid |
| Deal Value | value | Amount | estimatedvalue |
| Deal Stage | stage | StageName | stepname |

### Stage Mapping

| Local CRM | Salesforce | Dynamics 365 |
|-----------|------------|--------------|
| lead | Prospecting | 1 - Qualify |
| qualified | Qualification | 2 - Develop |
| proposal | Proposal/Price Quote | 3 - Propose |
| negotiation | Negotiation/Review | 4 - Close |
| won | Closed Won | Won |
| lost | Closed Lost | Lost |
