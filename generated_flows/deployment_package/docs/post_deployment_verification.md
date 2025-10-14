# Post-Deployment Verification Guide
## AutomatedMeetingNotesEmailer Flow

**Document Version**: 1.0
**Generated**: 2025-10-14
**Flow**: AutomatedMeetingNotesEmailer

---

## Overview

This document provides comprehensive post-deployment verification procedures to ensure the AutomatedMeetingNotesEmailer flow has been successfully deployed and is functioning correctly in the target Power Platform environment.

---

## Immediate Post-Deployment Checks

### Step 1: Verify Solution Import

```bash
# Check solution exists in environment
pac solution list | grep -i "MeetingAutomation"

# Expected output should show:
# MeetingAutomation | 1.0.0.x | Unmanaged | [Publisher]

# Get detailed solution information
pac solution list --environment <ENV-ID>
```

**Validation Criteria:**
- ✓ Solution appears in solution list
- ✓ Solution version matches deployed version
- ✓ Solution type is correct (unmanaged for dev/test, managed for prod)
- ✓ Publisher name is correct
- ✓ No import errors or warnings

**If Solution Not Found:**
1. Review deployment logs for errors
2. Check authentication is still valid
3. Verify deployment script completed successfully
4. Consider re-running deployment

---

### Step 2: Verify Flow Presence

```bash
# List all flows in environment
pac flow list

# Search for AutomatedMeetingNotesEmailer flow
pac flow list | grep -i "AutomatedMeetingNotes"

# Expected output format:
# Flow Display Name | Flow ID | State | Created Date
```

**Validation Criteria:**
- ✓ Flow appears in flow list
- ✓ Flow display name is "Automated Meeting Notes Emailer"
- ✓ Flow state is visible
- ✓ Created/modified date is recent

**Capture Flow ID for Subsequent Steps:**
```bash
# Extract flow ID (format varies by pac version)
FLOW_ID=$(pac flow list | grep -i "AutomatedMeetingNotes" | awk '{print $3}')
echo "Flow ID: $FLOW_ID"
```

---

### Step 3: Check Flow Status

```bash
# Get detailed flow information
pac flow show --flow-id <FLOW-ID>

# Key information to verify:
# - State: On/Off
# - Trigger: Manual
# - Connection References: Configured/Not Configured
```

**Expected State:** "On" (enabled)

**If Flow is Off/Disabled:**
```bash
# Enable the flow
pac flow enable --flow-id <FLOW-ID>

# Verify enabled
pac flow show --flow-id <FLOW-ID>
```

**Validation Criteria:**
- ✓ Flow is enabled (state = On)
- ✓ No suspension errors
- ✓ Trigger is configured correctly
- ✓ No validation errors

---

## Connection Reference Verification

### Step 1: Check Connection References Status

Via Power Automate Portal:
1. Navigate to https://make.powerautomate.com
2. Select target environment (top right)
3. Go to Solutions → MeetingAutomation
4. Click on "Automated Meeting Notes Emailer" flow
5. Look for connection reference warnings (yellow triangle icons)

**Expected Result:**
- If connections configured: No warnings, green checkmarks
- If not configured: Yellow warning icons with "Connection not configured"

### Step 2: Configure Connection References (if needed)

**Manual Configuration via Portal:**

1. In the flow editor, click on any action with connection warning
2. Click "Add new connection" or "Select existing connection"
3. Choose existing Office 365 Outlook connection or create new:
   - Click "+ New connection"
   - Sign in with Microsoft 365 account
   - Grant permissions (Mail.Send)
   - Save connection
4. Assign connection to action
5. Repeat for all actions requiring connections
6. Click "Save" to update flow

**Verification:**
- All connection warnings resolved
- Green checkmarks on all connector actions
- No authentication errors

### Step 3: Test Connection

```bash
# List connections in environment
pac connection list

# Find Office 365 Outlook connection
pac connection list | grep -i "office365"

# Verify connection status (should show as active)
```

**Via Portal:**
1. Go to Data → Connections
2. Find Office 365 Outlook connection
3. Click "..." menu → Test
4. Verify test succeeds

**Validation Criteria:**
- ✓ Office 365 connection exists
- ✓ Connection is active (not expired)
- ✓ Connection test passes
- ✓ Connection owner has proper permissions

---

## Trigger Configuration Verification

### Step 1: Obtain HTTP Trigger URL

**Via Power Automate Portal:**
1. Open flow in edit mode
2. Click on "manual" trigger (first step)
3. Copy the "HTTP POST URL"
4. Save this URL securely (treat as sensitive)

**Expected Format:**
```
https://prod-XX.REGION.logic.azure.com:443/workflows/FLOW-ID/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=SIGNATURE
```

**Document the URL:**
- Environment: [dev/test/prod]
- Flow ID: [FLOW-ID]
- Trigger URL: [FULL-URL]
- Date Retrieved: [DATE]

### Step 2: Verify Trigger Authentication

**Check Authentication Settings:**
1. In flow editor, expand "manual" trigger
2. Check "Who can trigger the flow?"
   - "Anyone" = No authentication required (⚠ not recommended)
   - "Specific users" = SAS token in URL required (✓ recommended)
   - "Only users in my organization" = Azure AD authentication required

**Recommended for Production:**
- Use "Specific users" with SAS token
- Document authorized applications/users
- Rotate SAS tokens periodically
- Monitor unauthorized access attempts

**Validation Criteria:**
- ✓ Trigger URL obtained
- ✓ Authentication configured appropriately
- ✓ URL tested successfully (see testing section)

---

## Functional Testing

### Test 1: Basic Flow Execution

**Prepare Test Payload:**
```json
{
  "meeting_title": "Post-Deployment Test Meeting",
  "participants": [
    "test.user1@contoso.com",
    "test.user2@contoso.com"
  ],
  "notes": "This is a test meeting to verify the AutomatedMeetingNotesEmailer flow is working correctly after deployment. Please confirm receipt.",
  "action_items": [
    {
      "task": "Confirm email receipt",
      "assignee": "test.user1@contoso.com",
      "due_date": "2025-10-15"
    }
  ]
}
```

**Execute Test via curl:**
```bash
# Save test payload to file
cat > test_payload.json << 'EOF'
{
  "meeting_title": "Post-Deployment Test Meeting",
  "participants": [
    "test.user1@contoso.com",
    "test.user2@contoso.com"
  ],
  "notes": "This is a test meeting to verify the AutomatedMeetingNotesEmailer flow is working correctly after deployment.",
  "action_items": [
    {
      "task": "Confirm email receipt",
      "assignee": "test.user1@contoso.com",
      "due_date": "2025-10-15"
    }
  ]
}
EOF

# Send test request
curl -X POST "<TRIGGER-URL>" \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# Expected response (HTTP 200):
{
  "status": "success",
  "message": "Meeting notes email sent successfully",
  "meeting_title": "Post-Deployment Test Meeting",
  "recipients_count": "2",
  "timestamp": "2025-10-14T10:30:00.000Z"
}
```

**Validation Criteria:**
- ✓ HTTP 200 status code received
- ✓ Response JSON is well-formed
- ✓ Response includes expected fields
- ✓ No error messages in response

### Test 2: Email Delivery Verification

**Check Email Delivery:**
1. Wait 1-2 minutes for email processing
2. Check test user inboxes (test.user1@contoso.com, test.user2@contoso.com)
3. Verify email received with correct:
   - Subject: "Meeting Notes: Post-Deployment Test Meeting"
   - From: Flow connection owner's email
   - To: All test participants
   - Body formatting: Professional HTML layout
   - Meeting notes displayed correctly
   - Action items listed with task, assignee, due date
   - Participants list shown
   - Timestamp included

**If Email Not Received:**
- Check spam/junk folders
- Verify email addresses are correct
- Check Office 365 mail flow (may take 5-10 minutes)
- Review flow run history for errors

**Validation Criteria:**
- ✓ Email received by all participants
- ✓ Subject line correct
- ✓ HTML formatting displays properly
- ✓ All content sections present
- ✓ Action items formatted correctly

### Test 3: Run History Verification

**Check Flow Run History:**
1. Open Power Automate portal
2. Go to My flows or Solutions → MeetingAutomation
3. Click on "Automated Meeting Notes Emailer"
4. View "Run history"

**Expected Result:**
- Recent run entry with "Succeeded" status
- Start time matches test execution time
- Duration: 5-15 seconds typical

**Drill into Run Details:**
1. Click on run entry
2. Review each action:
   - Parse JSON: Succeeded
   - Initialize Variables: Succeeded
   - Condition Check: Succeeded
   - Apply to Each (if action items present): Succeeded
   - Compose Email Body: Succeeded
   - Send Email: Succeeded
   - Response: Succeeded

**Check for Errors:**
- Green checkmarks on all actions
- No red X marks
- No warnings or alerts
- Execution time reasonable

**Validation Criteria:**
- ✓ Run appears in history
- ✓ Status is "Succeeded"
- ✓ All actions completed successfully
- ✓ No errors or warnings
- ✓ Execution time within expected range

### Test 4: Edge Cases and Error Handling

**Test 4.1: Minimal Payload (No Action Items)**
```json
{
  "meeting_title": "Minimal Test Meeting",
  "participants": ["test.user1@contoso.com"],
  "notes": "This test has no action items."
}
```

**Expected:**
- Flow succeeds
- Email sent
- "No action items recorded" message displayed

**Test 4.2: Multiple Action Items**
```json
{
  "meeting_title": "Multi-Action Item Test",
  "participants": ["test.user1@contoso.com"],
  "notes": "Testing multiple action items.",
  "action_items": [
    {"task": "Task 1", "assignee": "user1@contoso.com", "due_date": "2025-10-15"},
    {"task": "Task 2", "assignee": "user2@contoso.com", "due_date": "2025-10-16"},
    {"task": "Task 3", "assignee": "user3@contoso.com", "due_date": "2025-10-17"}
  ]
}
```

**Expected:**
- Flow succeeds
- All three action items listed in email
- Formatted correctly with task, assignee, due date

**Test 4.3: Special Characters**
```json
{
  "meeting_title": "Test Meeting with Special Chars: <>&\"'",
  "participants": ["test.user1@contoso.com"],
  "notes": "Testing special characters: <html> & \"quotes\" and 'apostrophes'"
}
```

**Expected:**
- Flow succeeds
- Special characters properly escaped/encoded
- No HTML injection issues

**Test 4.4: Long Content**
```json
{
  "meeting_title": "Test Meeting with Long Notes",
  "participants": ["test.user1@contoso.com"],
  "notes": "[Paste 1000+ character text here to test long content handling]"
}
```

**Expected:**
- Flow succeeds
- Long notes displayed correctly
- No truncation or formatting issues

**Validation Criteria:**
- ✓ All edge case tests pass
- ✓ Flow handles optional fields correctly
- ✓ Flow handles multiple items correctly
- ✓ Special characters properly handled
- ✓ Long content supported

---

## Performance Verification

### Metric 1: Execution Time

**Measure Flow Execution Time:**
1. View run history for successful test run
2. Note "Duration" value
3. Compare to expected range: 5-15 seconds

**If Execution Time Exceeds Expected:**
- Check for network latency issues
- Verify email service is responding
- Review action execution times individually
- Check for throttling or rate limiting

**Validation Criteria:**
- ✓ Execution time within acceptable range (5-15s typical)
- ✓ No timeouts
- ✓ Consistent performance across multiple runs

### Metric 2: Email Delivery Time

**Measure End-to-End Time:**
- Trigger invocation to email receipt
- Expected: 2-10 minutes (includes Exchange processing)

**If Delays Observed:**
- Check Exchange Online mail flow
- Verify no mail flow rules blocking automated emails
- Check for email throttling
- Review Office 365 service health

**Validation Criteria:**
- ✓ Email delivered within reasonable timeframe
- ✓ No significant delays
- ✓ Consistent delivery times

### Metric 3: Resource Utilization

**Check API Limits:**
```bash
# View environment capacity (via admin portal)
# Power Platform Admin Center → Environments → [Env] → Capacity
```

**Monitor:**
- API requests per day
- Flow runs per day
- Dataverse storage

**Validation Criteria:**
- ✓ Flow execution within API quota
- ✓ No throttling errors
- ✓ Acceptable resource consumption

---

## Security Verification

### Check 1: Authentication Security

**Verify:**
- Trigger authentication configured (not "Anyone")
- Connection uses OAuth (not hardcoded credentials)
- SAS tokens in URLs are secured
- API endpoints not publicly exposed

### Check 2: Data Privacy

**Verify:**
- No logging of sensitive data
- Email content appropriate for audience
- Participant data handled securely
- Run history respects data retention policies

### Check 3: Access Controls

**Verify:**
- Flow owner has appropriate permissions
- Connection owner documented
- Run-only users configured (if applicable)
- Solution is in correct security role

**Validation Criteria:**
- ✓ Authentication properly configured
- ✓ No security warnings
- ✓ Data privacy requirements met
- ✓ Access controls appropriate

---

## Integration Verification

### Check 1: API Integration

**If Flow is Called by Application:**
1. Test integration from calling application
2. Verify application receives correct response
3. Check error handling in application
4. Verify retry logic (if implemented)

### Check 2: Downstream Dependencies

**Verify:**
- Email recipients can receive emails
- No mail flow rules blocking delivery
- No email client rendering issues
- Links/references in email work correctly

**Validation Criteria:**
- ✓ Integration with calling applications works
- ✓ Downstream systems functioning correctly
- ✓ No integration errors

---

## Monitoring Setup Verification

### Check 1: Run History Retention

**Verify:**
1. Run history is accessible
2. Retention period is appropriate
3. Historical runs preserved

**Configure Retention (if needed):**
- Power Platform Admin Center
- Environments → [Env] → Settings
- Product → Features
- Set "Flow run retention" period

**Recommended:** 28 days minimum for production

### Check 2: Error Alerting

**Verify Error Notifications:**
1. Check flow owner receives failure notifications
2. Test by causing intentional failure (optional)
3. Verify notification email/channel

**Configure Alerts (if needed):**
- Flow settings → Alert settings
- Enable "Notify me by email if my flow fails"
- Configure alert recipients

**Validation Criteria:**
- ✓ Run history accessible
- ✓ Retention period appropriate
- ✓ Error alerts configured
- ✓ Monitoring in place

---

## Documentation Verification

### Check 1: API Endpoint Documentation

**Verify Documentation Includes:**
- Flow trigger URL
- Authentication requirements
- Request schema
- Response schema
- Example payloads
- Error codes

**Update Documentation:**
- Document actual trigger URL from deployment
- Update environment-specific details
- Note any configuration differences

### Check 2: Operational Runbook

**Verify Runbook Includes:**
- Flow description and purpose
- Connection dependencies
- Monitoring procedures
- Troubleshooting steps
- Escalation contacts
- Rollback procedures

**Validation Criteria:**
- ✓ API documentation complete
- ✓ Operational runbook ready
- ✓ Contact information current
- ✓ Troubleshooting guide available

---

## Post-Deployment Checklist

### Deployment Verification

- [ ] Solution imported successfully
- [ ] Flow appears in environment
- [ ] Flow is enabled
- [ ] Connection references configured
- [ ] Trigger URL obtained
- [ ] Authentication configured

### Functional Testing

- [ ] Basic flow execution test passed
- [ ] Email delivery verified
- [ ] Run history shows success
- [ ] Edge cases tested
- [ ] Error handling verified

### Performance Verification

- [ ] Execution time acceptable
- [ ] Email delivery time reasonable
- [ ] Resource utilization normal
- [ ] No throttling or rate limiting

### Security Verification

- [ ] Authentication properly configured
- [ ] Data privacy requirements met
- [ ] Access controls appropriate
- [ ] No security warnings

### Integration Verification

- [ ] API integration tested (if applicable)
- [ ] Downstream systems verified
- [ ] No integration errors

### Monitoring Verification

- [ ] Run history accessible
- [ ] Retention period configured
- [ ] Error alerts enabled
- [ ] Monitoring tools configured

### Documentation Verification

- [ ] API endpoint documented
- [ ] Operational runbook complete
- [ ] Contact information updated
- [ ] Troubleshooting guide available

---

## Sign-Off

### Deployment Verification Complete

**Verified By**: _____________________________ Date: __________

**Technical Lead**: _____________________________ Date: __________

**Business Owner**: _____________________________ Date: __________

---

## Known Issues and Limitations

### Known Issues

[Document any known issues discovered during verification]

**Example:**
- None at this time

### Limitations

[Document any known limitations]

**Examples:**
- Email delivery depends on Exchange Online service availability
- Maximum 100 participants recommended for single email
- HTML email may render differently in various email clients

---

## Next Steps

After completing verification:

1. **Update Status**: Mark deployment as complete in change management system
2. **Notify Stakeholders**: Inform relevant parties deployment is successful
3. **Enable Monitoring**: Ensure monitoring and alerting is active
4. **Document Lessons Learned**: Record any issues and resolutions
5. **Plan for Enhancements**: Note any improvement opportunities
6. **Schedule Review**: Plan post-deployment review meeting

---

## Troubleshooting

### Issue: Flow Not Found After Deployment

**Possible Causes:**
- Deployment failed silently
- Wrong environment selected
- Solution import incomplete

**Solutions:**
1. Re-check authentication and environment
2. Review deployment logs
3. Re-run deployment if necessary
4. Contact Power Platform support if issue persists

### Issue: Connection Not Configured

**Possible Causes:**
- Connection not created before deployment
- Connection reference mapping incorrect
- OAuth authentication not completed

**Solutions:**
1. Create Office 365 connection in environment
2. Open flow and configure connection manually
3. Verify connection test passes
4. Save and re-test flow

### Issue: Email Not Delivered

**Possible Causes:**
- Connection not configured
- Email addresses invalid
- Mail flow rules blocking
- Exchange service issue

**Solutions:**
1. Verify connection is working
2. Check email addresses are valid
3. Review Exchange Admin Center for mail flow issues
4. Check Office 365 service health
5. Review flow run history for specific error

### Issue: Flow Execution Fails

**Possible Causes:**
- Connection expired or invalid
- Malformed input data
- Permission issue
- Service outage

**Solutions:**
1. Check run history for specific error
2. Verify connection is active
3. Validate input payload matches schema
4. Check user permissions
5. Verify Power Platform service health

---

## Support Contacts

**Technical Support:**
- Flow Owner: [NAME/EMAIL]
- Power Platform Admin: [NAME/EMAIL]
- Microsoft Support: https://admin.powerplatform.microsoft.com (Support tab)

**Business Contacts:**
- Product Owner: [NAME/EMAIL]
- Business Sponsor: [NAME/EMAIL]

**Escalation:**
- Level 1: Flow Owner
- Level 2: Power Platform Admin
- Level 3: Microsoft Support

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-14 | Power Platform Deployment Agent | Initial version |

**Related Documents**:
- Pre-Deployment Validation Guide
- Flow Analysis Report
- Deployment Readiness Checklist
- Deployment Script Documentation
- Rollback Procedures
