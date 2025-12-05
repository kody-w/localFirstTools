# Automated Meeting Notes Emailer - Power Automate Flow

## Overview
This Power Automate flow automatically formats and distributes meeting notes via email to all participants. It accepts structured meeting data via HTTP POST request and sends a professionally formatted HTML email with meeting notes and action items.

## Flow Summary

**Flow Name:** Automated Meeting Notes Emailer
**Flow Type:** Instant (Manual Trigger via HTTP Request)
**Primary Connector:** Office 365 Outlook
**Response Type:** JSON response with success/failure status

---

## Flow Structure

### 1. Trigger: HTTP Request (Manual)
- **Type:** Request trigger with HTTP endpoint
- **Method:** POST
- **Authentication:** Supports all authentication types
- **Expected Input:** JSON payload with meeting information

### 2. Actions Sequence

#### Action 1: Parse JSON - Meeting Data
- **Purpose:** Parse incoming JSON payload
- **Output:** Structured meeting data object

#### Action 2: Initialize Variable - Email Recipients
- **Purpose:** Convert participants array to semicolon-separated string
- **Variable Type:** String
- **Value:** Joined participant email addresses

#### Action 3: Initialize Variable - Action Items HTML
- **Purpose:** Store formatted HTML for action items
- **Variable Type:** String
- **Initial Value:** Empty string

#### Action 4: Condition - Check Action Items
- **Purpose:** Determine if action items exist
- **Condition:** Array length > 0

**If True:**
- Loop through each action item
- Build HTML list items with task, assignee, and due date

**If False:**
- Set default message: "No action items recorded"

#### Action 5: Compose - Email Body
- **Purpose:** Create professionally formatted HTML email body
- **Includes:**
  - Styled header with meeting title
  - Meeting notes section
  - Action items list
  - Participants list
  - Auto-generated timestamp

#### Action 6: Send Email (V2)
- **Purpose:** Send formatted email to all participants
- **Recipients:** All meeting participants
- **Subject:** "Meeting Notes: [Meeting Title]"
- **Body:** HTML formatted content

#### Action 7: Response - Success
- **Purpose:** Return HTTP response confirming email sent
- **Status Code:** 200
- **Response Body:** JSON with status, message, and metadata

---

## Input Schema

### Required Fields

```json
{
  "meeting_title": "string",
  "participants": ["email1@example.com", "email2@example.com"],
  "notes": "string"
}
```

### Optional Fields

```json
{
  "action_items": [
    {
      "task": "string",
      "assignee": "string",
      "due_date": "string"
    }
  ]
}
```

### Complete Example Request

```json
{
  "meeting_title": "Q4 Planning Strategy Session",
  "participants": [
    "john.smith@company.com",
    "sarah.jones@company.com",
    "mike.wilson@company.com"
  ],
  "notes": "Discussed Q4 objectives and key initiatives:\n\n1. Launch new product line in October\n2. Expand marketing budget by 15%\n3. Hire 3 additional team members\n4. Focus on customer retention metrics\n\nKey Decisions:\n- Approved budget increase\n- Set launch date for Oct 15\n- Agreed on hiring priorities",
  "action_items": [
    {
      "task": "Finalize product specifications",
      "assignee": "John Smith",
      "due_date": "2025-10-20"
    },
    {
      "task": "Create marketing campaign proposal",
      "assignee": "Sarah Jones",
      "due_date": "2025-10-25"
    },
    {
      "task": "Post job openings for new positions",
      "assignee": "Mike Wilson",
      "due_date": "2025-10-18"
    }
  ]
}
```

---

## Output Response

### Success Response (200)

```json
{
  "status": "success",
  "message": "Meeting notes email sent successfully",
  "meeting_title": "Q4 Planning Strategy Session",
  "recipients_count": 3,
  "timestamp": "2025-10-14T15:30:00Z"
}
```

### Error Scenarios
- **400:** Invalid JSON format or missing required fields
- **401:** Authentication failure
- **500:** Email sending failure or internal error

---

## Required Connections

### Office 365 Outlook Connection
- **Connection Name:** shared_office365
- **Required Permissions:**
  - Send email as user
  - Access user mailbox
- **Authentication Type:** OAuth 2.0
- **Scopes Required:**
  - `Mail.Send`
  - `Mail.ReadWrite`

### Setup Instructions:
1. Open Power Automate portal
2. Navigate to Connections
3. Add new connection: "Office 365 Outlook"
4. Sign in with organizational account
5. Grant requested permissions
6. Note the connection reference name for flow configuration

---

## Configuration Notes

### Pre-Deployment Checklist
- [ ] Office 365 Outlook connector configured
- [ ] Test user has permission to send emails
- [ ] Organization allows automated email sending
- [ ] Email address format validation enabled
- [ ] HTML email rendering supported in recipient mailboxes

### Post-Deployment Configuration

#### 1. Connection Reference Update
Update the connection reference in the flow JSON:
```json
"connectionReferenceLogicalName": "YOUR_CONNECTION_NAME"
```

#### 2. Trigger URL
After deployment, note the HTTP POST URL:
- Found in: Flow details > Manual trigger
- Format: `https://prod-XX.logic.azure.com:443/workflows/.../triggers/manual/paths/invoke?api-version=2016-10-01&sp=...`

#### 3. Security Considerations
- Enable trigger authentication (recommended: Azure AD)
- Restrict IP addresses if needed
- Implement rate limiting to prevent abuse
- Monitor flow run history for suspicious activity

#### 4. Email Customization
To customize the email template:
- Edit the "Compose - Email Body" action
- Modify HTML/CSS in the compose content
- Test email rendering across different email clients
- Ensure mobile responsiveness

---

## Testing the Flow

### Test via Power Automate Portal
1. Open flow in edit mode
2. Click "Test" in top-right corner
3. Select "Manually"
4. Paste sample JSON payload
5. Click "Run flow"
6. Check email inbox for formatted message

### Test via HTTP Request (Postman/cURL)

```bash
curl -X POST "YOUR_FLOW_TRIGGER_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "Test Meeting",
    "participants": ["your.email@company.com"],
    "notes": "This is a test of the meeting notes emailer.",
    "action_items": [
      {
        "task": "Review flow functionality",
        "assignee": "Test User",
        "due_date": "2025-10-15"
      }
    ]
  }'
```

### Validation Checklist
- [ ] Email received by all participants
- [ ] Meeting title displays correctly
- [ ] Notes formatting preserved (line breaks, spacing)
- [ ] Action items list formatted properly
- [ ] Participant list accurate
- [ ] Timestamp shows current UTC time
- [ ] HTML styling renders correctly
- [ ] Email marked with appropriate importance

---

## Integration Examples

### Integration with Microsoft Teams
```javascript
// Teams bot webhook trigger
const meetingData = {
  meeting_title: meetingContext.title,
  participants: meetingContext.attendees.map(a => a.email),
  notes: meetingContext.notes,
  action_items: meetingContext.actionItems
};

fetch(FLOW_TRIGGER_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(meetingData)
});
```

### Integration with SharePoint
```javascript
// SharePoint list item trigger
const listItem = context.itemProperties;
const flowPayload = {
  meeting_title: listItem.Title,
  participants: listItem.Participants.split(';'),
  notes: listItem.Notes,
  action_items: JSON.parse(listItem.ActionItems)
};
```

### Integration with Custom Application
```python
import requests
import json

def send_meeting_notes(title, participants, notes, action_items):
    flow_url = "YOUR_FLOW_TRIGGER_URL"
    payload = {
        "meeting_title": title,
        "participants": participants,
        "notes": notes,
        "action_items": action_items
    }

    response = requests.post(flow_url, json=payload)
    return response.json()

# Example usage
send_meeting_notes(
    title="Project Kickoff",
    participants=["team@company.com"],
    notes="Discussed project timeline and deliverables.",
    action_items=[
        {
            "task": "Create project charter",
            "assignee": "PM",
            "due_date": "2025-10-20"
        }
    ]
)
```

---

## Troubleshooting

### Common Issues and Solutions

#### Email Not Received
**Problem:** Flow runs successfully but email not received
**Solutions:**
- Check recipient email addresses are valid
- Verify email not in spam/junk folder
- Confirm sender has permission to send on behalf of organization
- Check Office 365 mail flow rules

#### HTML Formatting Issues
**Problem:** Email displays as plain text or formatting broken
**Solutions:**
- Ensure recipient email client supports HTML
- Test in different email clients (Outlook, Gmail, mobile)
- Validate HTML syntax in Compose action
- Check CSS inline styles are used (not external stylesheets)

#### Action Items Not Displaying
**Problem:** Action items array not rendering in email
**Solutions:**
- Verify action_items is valid JSON array
- Check condition logic in flow
- Ensure action item properties match schema (task, assignee, due_date)
- Review loop iteration in "Apply to each" action

#### Timeout Errors
**Problem:** Flow times out before completion
**Solutions:**
- Reduce number of action items processed
- Optimize HTML composition logic
- Check network connectivity to Office 365 services
- Implement retry policy on Send Email action

#### Authentication Failures
**Problem:** Flow fails with 401 Unauthorized
**Solutions:**
- Re-authenticate Office 365 connection
- Verify user permissions haven't changed
- Check OAuth token hasn't expired
- Confirm connection reference is correct

---

## Performance Considerations

### Flow Execution Metrics
- **Average Runtime:** 5-10 seconds
- **Maximum Input Size:** 10MB
- **Concurrent Executions:** Limited by Power Automate plan
- **Daily Execution Limit:** Based on license type

### Optimization Tips
1. **Minimize Action Items:** Keep action items list under 50 items
2. **HTML Size:** Keep composed HTML under 100KB
3. **Participant List:** Batch large participant lists (>100 recipients)
4. **Error Handling:** Add try-catch scope for graceful failures
5. **Logging:** Enable flow analytics for performance monitoring

---

## Advanced Customization

### Add Meeting Attachments
Add after "Compose - Email Body" action:
```json
{
  "emailMessage/Attachments": [
    {
      "Name": "meeting_notes.pdf",
      "ContentBytes": "@{base64(body('Get_File_Content'))}"
    }
  ]
}
```

### Send Calendar Invite
Add parallel action to create calendar event:
```json
{
  "operationId": "CreateEvent_V4",
  "parameters": {
    "eventItem/subject": "@{body('Parse_JSON_-_Meeting_Data')?['meeting_title']}",
    "eventItem/attendees": "@{variables('EmailRecipients')}"
  }
}
```

### Save to SharePoint
Add action to archive meeting notes:
```json
{
  "operationId": "CreateItem",
  "parameters": {
    "dataset": "YOUR_SHAREPOINT_SITE",
    "table": "Meeting Notes",
    "item": {
      "Title": "@{body('Parse_JSON_-_Meeting_Data')?['meeting_title']}",
      "Notes": "@{body('Parse_JSON_-_Meeting_Data')?['notes']}"
    }
  }
}
```

### Add Approval Step
Insert before "Send an email (V2)":
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_approvals",
      "operationId": "CreateApproval"
    },
    "parameters": {
      "approvalRequest/title": "Approve Meeting Notes",
      "approvalRequest/assignedTo": "manager@company.com"
    }
  }
}
```

---

## Monitoring and Maintenance

### Flow Analytics
Monitor these metrics in Power Automate portal:
- Total runs (success/failure rate)
- Average execution time
- Email delivery success rate
- Error frequency and types

### Recommended Alerts
Set up alerts for:
- Flow failure rate exceeds 5%
- Average execution time exceeds 30 seconds
- More than 3 consecutive failures
- Connection authentication expires

### Maintenance Schedule
- **Weekly:** Review error logs
- **Monthly:** Update connection credentials if needed
- **Quarterly:** Review and optimize flow logic
- **Annually:** Audit permissions and access

---

## Compliance and Security

### Data Handling
- Meeting notes stored temporarily in flow run history
- No persistent storage of sensitive information
- Emails subject to organization's retention policies

### Privacy Considerations
- Participant email addresses visible to all recipients
- Meeting notes accessible to all participants
- Consider data classification labels for sensitive meetings

### Audit Trail
- All flow runs logged in Power Automate history
- Email sending tracked in Office 365 audit logs
- Participant actions not tracked (read/open status)

---

## License Requirements

### Power Automate License
- **Minimum:** Power Automate Per User plan
- **Recommended:** Power Automate Premium (for advanced features)

### Office 365 License
- **Required:** Office 365 Business Basic or higher
- **Permissions:** Exchange Online Plan 1 or higher

---

## Support and Resources

### Documentation
- [Power Automate Documentation](https://docs.microsoft.com/power-automate/)
- [Office 365 Connector Reference](https://docs.microsoft.com/connectors/office365/)
- [Flow Best Practices](https://docs.microsoft.com/power-automate/guidance/planning/best-practices)

### Community Resources
- Power Automate Community Forums
- Microsoft Tech Community
- GitHub Power Automate Examples Repository

### Contact Information
For issues or questions:
- Submit support ticket via Power Platform admin center
- Contact your organization's Power Platform administrator
- Reference this flow by name: "Automated Meeting Notes Emailer"

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-14 | Initial release with core functionality |

---

## File Location
**Flow JSON:** `/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/AutomatedMeetingNotesEmailer.json`

**Documentation:** `/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/AutomatedMeetingNotesEmailer_README.md`
