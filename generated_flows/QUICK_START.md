# Quick Start Guide - Automated Meeting Notes Emailer

## 5-Minute Setup

### Step 1: Import the Flow
1. Open [Power Automate Portal](https://make.powerautomate.com)
2. Click **My flows** → **Import** → **Import Package (Legacy)**
3. Upload `AutomatedMeetingNotesEmailer.json`
4. Click **Import**

### Step 2: Configure Connection
1. During import, you'll be prompted to select a connection
2. Choose existing **Office 365 Outlook** connection OR create new
3. Sign in with your organizational account
4. Grant permissions when prompted

### Step 3: Get Trigger URL
1. Open the imported flow
2. Click on the **manual trigger** step
3. Copy the **HTTP POST URL**
4. Save this URL securely (you'll use it to trigger the flow)

### Step 4: Test the Flow
```bash
curl -X POST "YOUR_HTTP_POST_URL_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "Test Meeting",
    "participants": ["your.email@company.com"],
    "notes": "This is a test meeting note.",
    "action_items": [
      {
        "task": "Test the flow",
        "assignee": "You",
        "due_date": "2025-10-15"
      }
    ]
  }'
```

### Step 5: Check Your Email
You should receive a professionally formatted email with:
- Meeting title
- Notes
- Action items
- Participant list
- Timestamp

---

## Minimal JSON Example

```json
{
  "meeting_title": "Weekly Team Sync",
  "participants": ["team@company.com"],
  "notes": "Discussed project status and next steps."
}
```

---

## Common Use Cases

### 1. Manual Trigger from Browser
Save this as HTML and open in browser:

```html
<!DOCTYPE html>
<html>
<head><title>Send Meeting Notes</title></head>
<body>
  <h2>Meeting Notes Sender</h2>
  <form id="meetingForm">
    <input type="text" id="title" placeholder="Meeting Title" required><br>
    <input type="email" id="participant" placeholder="participant@company.com" required><br>
    <textarea id="notes" placeholder="Meeting notes..." required></textarea><br>
    <button type="submit">Send Notes</button>
  </form>

  <script>
    document.getElementById('meetingForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const response = await fetch('YOUR_FLOW_URL', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          meeting_title: document.getElementById('title').value,
          participants: [document.getElementById('participant').value],
          notes: document.getElementById('notes').value
        })
      });
      alert('Email sent!');
    });
  </script>
</body>
</html>
```

### 2. Integration with Microsoft Teams
Add this to your Teams bot:

```javascript
const axios = require('axios');

async function sendMeetingNotes(meetingData) {
  await axios.post('YOUR_FLOW_URL', {
    meeting_title: meetingData.title,
    participants: meetingData.attendees,
    notes: meetingData.transcript,
    action_items: meetingData.tasks
  });
}
```

### 3. Schedule via Power Automate
Create a scheduled flow that triggers this flow:
1. Trigger: **Recurrence** (e.g., every Friday at 5 PM)
2. Action: **HTTP** → POST to flow URL
3. Body: Your standard meeting notes JSON

---

## Troubleshooting in 3 Steps

### Problem: Email not received
1. Check spam/junk folder
2. Verify email address spelling
3. Test with your own email first

### Problem: Flow fails
1. Check Office 365 connection is active
2. Verify JSON format is valid
3. Review flow run history for error details

### Problem: HTML not formatted
1. Open email in Outlook (not mobile app)
2. Enable HTML display in email client
3. Check if organization blocks HTML emails

---

## Need Help?

- **Full Documentation:** See `AutomatedMeetingNotesEmailer_README.md`
- **Flow Definition:** See `AutomatedMeetingNotesEmailer.json`
- **Support:** Contact your Power Platform administrator

---

**Created:** 2025-10-14
**Version:** 1.0.0
**License Required:** Power Automate Per User + Office 365
