# Flow Diagram - Automated Meeting Notes Emailer

## Visual Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLOW TRIGGER                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  HTTP Request (Manual Trigger)                                │  │
│  │  • Method: POST                                               │  │
│  │  • Content-Type: application/json                             │  │
│  │  • Authentication: All types supported                        │  │
│  │  • Input: JSON with meeting data                              │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ACTION 1: PARSE JSON                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Parse JSON - Meeting Data                                    │  │
│  │  • Parse meeting_title (string)                               │  │
│  │  • Parse participants (array)                                 │  │
│  │  • Parse notes (string)                                       │  │
│  │  • Parse action_items (array, optional)                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              ACTION 2: INITIALIZE EMAIL RECIPIENTS                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Initialize Variable - EmailRecipients                        │  │
│  │  • Type: String                                               │  │
│  │  • Value: join(participants, ';')                             │  │
│  │  • Example: "user1@co.com;user2@co.com"                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│            ACTION 3: INITIALIZE ACTION ITEMS HTML                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Initialize Variable - ActionItemsHTML                        │  │
│  │  • Type: String                                               │  │
│  │  • Value: "" (empty)                                          │  │
│  │  • Purpose: Store formatted HTML list                         │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│           ACTION 4: CONDITION - CHECK ACTION ITEMS                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  If length(action_items) > 0                                  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────┬───────────────────┘
                  │                               │
         YES      │                               │      NO
                  │                               │
                  ▼                               ▼
    ┌──────────────────────────┐    ┌──────────────────────────┐
    │  LOOP: For Each Action   │    │  Set Variable            │
    │  Item                    │    │  "No action items        │
    │  ┌────────────────────┐  │    │  recorded"               │
    │  │ Append to String:  │  │    └──────────┬───────────────┘
    │  │ • Task             │  │               │
    │  │ • Assignee         │  │               │
    │  │ • Due Date         │  │               │
    │  │ • Format as <li>   │  │               │
    │  └────────────────────┘  │               │
    └────────────┬─────────────┘               │
                 │                              │
                 └──────────────┬───────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 ACTION 5: COMPOSE EMAIL BODY                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Compose HTML Email                                           │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ HTML Structure:                                          │  │  │
│  │  │ ┌─────────────────────────────────────────────────────┐ │  │  │
│  │  │ │ <div class="header">                                │ │  │  │
│  │  │ │   <h1>{meeting_title}</h1>                          │ │  │  │
│  │  │ │ </div>                                              │ │  │  │
│  │  │ └─────────────────────────────────────────────────────┘ │  │  │
│  │  │ ┌─────────────────────────────────────────────────────┐ │  │  │
│  │  │ │ <div class="content">                               │ │  │  │
│  │  │ │   <div class="section">                             │ │  │  │
│  │  │ │     <h2>Meeting Notes</h2>                          │ │  │  │
│  │  │ │     <p>{notes}</p>                                  │ │  │  │
│  │  │ │   </div>                                            │ │  │  │
│  │  │ │   <div class="section">                             │ │  │  │
│  │  │ │     <h2>Action Items</h2>                           │ │  │  │
│  │  │ │     <ul>{ActionItemsHTML}</ul>                      │ │  │  │
│  │  │ │   </div>                                            │ │  │  │
│  │  │ │   <div class="section">                             │ │  │  │
│  │  │ │     <h2>Participants</h2>                           │ │  │  │
│  │  │ │     <p>{participants}</p>                           │ │  │  │
│  │  │ │   </div>                                            │ │  │  │
│  │  │ │ </div>                                              │ │  │  │
│  │  │ └─────────────────────────────────────────────────────┘ │  │  │
│  │  │ ┌─────────────────────────────────────────────────────┐ │  │  │
│  │  │ │ <div class="footer">                                │ │  │  │
│  │  │ │   <p>Auto-generated by Power Automate</p>           │ │  │  │
│  │  │ │   <p>Timestamp: {utcNow()}</p>                      │ │  │  │
│  │  │ │ </div>                                              │ │  │  │
│  │  │ └─────────────────────────────────────────────────────┘ │  │  │
│  │  │                                                          │  │  │
│  │  │ CSS Styling:                                             │  │  │
│  │  │ • Header: Blue (#0078d4) background                      │  │  │
│  │  │ • Sections: White with borders                           │  │  │
│  │  │ • Responsive layout                                      │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  ACTION 6: SEND EMAIL                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Send an email (V2) - Office 365                             │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │ To: {EmailRecipients}                                   │ │  │
│  │  │ Subject: "Meeting Notes: {meeting_title}"               │ │  │
│  │  │ Body: {ComposedHTML}                                    │ │  │
│  │  │ Importance: Normal                                      │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  │                                                               │  │
│  │  Connection: Office 365 Outlook                              │  │
│  │  Authentication: OAuth 2.0                                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                ACTION 7: HTTP RESPONSE                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Response - Success                                           │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │ Status Code: 200                                        │ │  │
│  │  │ Headers: {"Content-Type": "application/json"}           │ │  │
│  │  │ Body: {                                                 │ │  │
│  │  │   "status": "success",                                  │ │  │
│  │  │   "message": "Email sent successfully",                 │ │  │
│  │  │   "meeting_title": "{meeting_title}",                   │ │  │
│  │  │   "recipients_count": {count},                          │ │  │
│  │  │   "timestamp": "{utcNow()}"                             │ │  │
│  │  │ }                                                        │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
                          ╔═══════════╗
                          ║  SUCCESS  ║
                          ╚═══════════╝
```

---

## Data Flow Diagram

```
┌───────────────┐
│  HTTP POST    │
│  Request      │
│               │
│  JSON Input:  │
│  - title      │
│  - participants│
│  - notes      │
│  - actions    │
└───────┬───────┘
        │
        ▼
┌───────────────────────────────┐
│  Parse & Extract              │
│  ┌─────────────────────────┐  │
│  │ meeting_title  → String │  │
│  │ participants   → Array  │  │
│  │ notes          → String │  │
│  │ action_items   → Array  │  │
│  └─────────────────────────┘  │
└───────────────┬───────────────┘
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
┌───────────────┐  ┌───────────────┐
│ Transform     │  │ Transform     │
│ Participants  │  │ Action Items  │
│               │  │               │
│ Array → String│  │ Array → HTML  │
│ Semicolon     │  │ List          │
│ Separated     │  │               │
└───────┬───────┘  └───────┬───────┘
        │                  │
        └────────┬─────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Compose        │
        │ HTML Email     │
        │                │
        │ Combine:       │
        │ • Header       │
        │ • Notes        │
        │ • Actions      │
        │ • Participants │
        │ • Footer       │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Office 365     │
        │ Send Email     │
        │                │
        │ To: Recipients │
        │ Body: HTML     │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Return         │
        │ Success        │
        │ Response       │
        │                │
        │ HTTP 200       │
        │ JSON Body      │
        └────────────────┘
```

---

## Error Handling Flow

```
                    ┌──────────────┐
                    │ Any Action   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Succeeded?  │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
            YES                        NO
              │                         │
              ▼                         ▼
    ┌──────────────────┐    ┌──────────────────┐
    │ Continue to      │    │ Flow Fails       │
    │ Next Action      │    │                  │
    └──────────────────┘    │ Error captured   │
                            │ in run history   │
                            │                  │
                            │ No email sent    │
                            │                  │
                            │ HTTP 500 or      │
                            │ no response      │
                            └──────────────────┘

Note: Current implementation does not include explicit
error handling (try-catch scope). All errors result in
flow failure and no email sent. Consider adding error
handling scope for production use.
```

---

## Connection Dependencies

```
┌─────────────────────────────────────────────────┐
│          Power Automate Flow                    │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  Flow Definition                          │ │
│  │  • Triggers                               │ │
│  │  • Actions                                │ │
│  │  • Variables                              │ │
│  └───────────────┬───────────────────────────┘ │
│                  │                             │
│                  │ requires                    │
│                  ▼                             │
│  ┌───────────────────────────────────────────┐ │
│  │  Connection Reference                     │ │
│  │  • Name: shared_office365                 │ │
│  │  • Type: OAuth 2.0                        │ │
│  │  • Logical Name: shared_office365_conn... │ │
│  └───────────────┬───────────────────────────┘ │
└──────────────────┼───────────────────────────────┘
                   │
                   │ authenticates with
                   ▼
┌─────────────────────────────────────────────────┐
│          Office 365 Outlook Connector           │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  API Operations                           │ │
│  │  • SendEmailV2                            │ │
│  │  • GetEmails                              │ │
│  │  • CreateEvent                            │ │
│  └───────────────┬───────────────────────────┘ │
└──────────────────┼───────────────────────────────┘
                   │
                   │ calls
                   ▼
┌─────────────────────────────────────────────────┐
│       Microsoft Graph API / Exchange Online     │
│                                                 │
│  • Send emails                                  │
│  • Access mailbox                               │
│  • Manage calendar                              │
└─────────────────────────────────────────────────┘
```

---

## Timeline Diagram

```
Time →

0s     │ HTTP Request received
       │
0.5s   │ Parse JSON completed
       │
1s     │ Initialize EmailRecipients variable
       │
1.5s   │ Initialize ActionItemsHTML variable
       │
2s     │ Evaluate condition (action items exist?)
       │
       │ ┌─────────────────────────────┐
2-4s   │ │ Loop through action items   │
       │ │ (if present)                │
       │ └─────────────────────────────┘
       │
4.5s   │ Compose HTML email body
       │
       │ ┌─────────────────────────────┐
5-8s   │ │ Send email via Office 365   │ ← Longest operation
       │ │ (network call)              │
       │ └─────────────────────────────┘
       │
8.5s   │ Compose success response
       │
9s     │ Return HTTP 200 response
       │
       ▼ Flow Complete

Total: ~5-10 seconds (average)
```

---

## Email Rendering Preview

```
┌─────────────────────────────────────────────────────────┐
│ From: your.name@company.com                             │
│ To: participant1@company.com; participant2@company.com  │
│ Subject: Meeting Notes: Q4 Planning Session             │
└─────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Q4 Planning Session                                    ┃ ← Blue header
┃  Meeting Notes Summary                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Meeting Notes                                          │ ← Section title
│  ├─────────────────────────────────────────────────┐   │
│  │ Discussed Q4 objectives and key initiatives:    │   │
│  │                                                 │   │
│  │ 1. Launch new product line in October          │   │
│  │ 2. Expand marketing budget by 15%              │   │
│  │ 3. Hire 3 additional team members              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Action Items                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ • Finalize product specifications               │   │
│  │   Assignee: John Smith                          │   │
│  │   Due Date: 2025-10-20                          │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ • Create marketing campaign proposal            │   │
│  │   Assignee: Sarah Jones                         │   │
│  │   Due Date: 2025-10-25                          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Participants                                           │
│  john.smith@company.com, sarah.jones@company.com,       │
│  mike.wilson@company.com                                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  This email was automatically generated by              │
│  Power Automate.                                        │
│  Meeting Date: 2025-10-14T10:48:00Z                     │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Points

```
External Systems/Triggers → Power Automate Flow → Recipients

┌──────────────────┐
│ Microsoft Teams  │───┐
└──────────────────┘   │
                       │
┌──────────────────┐   │
│ SharePoint List  │───┤
└──────────────────┘   │
                       │     ┌─────────────────────────┐
┌──────────────────┐   ├────→│ Meeting Notes Emailer   │
│ Custom Web App   │───┤     │ Power Automate Flow     │
└──────────────────┘   │     └───────────┬─────────────┘
                       │                 │
┌──────────────────┐   │                 │
│ Mobile App       │───┤                 ▼
└──────────────────┘   │     ┌─────────────────────────┐
                       │     │ Office 365 Outlook      │
┌──────────────────┐   │     └───────────┬─────────────┘
│ Voice Assistant  │───┤                 │
└──────────────────┘   │                 │
                       │                 ▼
┌──────────────────┐   │     ┌─────────────────────────┐
│ Scheduled Flow   │───┘     │ Email Recipients        │
└──────────────────┘         │ • Participant 1         │
                             │ • Participant 2         │
                             │ • Participant N         │
                             └─────────────────────────┘
```

---

## State Machine Diagram

```
┌───────────┐
│   IDLE    │
└─────┬─────┘
      │
      │ HTTP POST received
      ▼
┌───────────┐
│  PARSING  │ ← Validate JSON schema
└─────┬─────┘
      │
      │ Valid input
      ▼
┌─────────────┐
│ PROCESSING  │ ← Transform data
└─────┬───────┘
      │
      │ Data transformed
      ▼
┌──────────────┐
│  COMPOSING   │ ← Build HTML email
└─────┬────────┘
      │
      │ HTML ready
      ▼
┌──────────────┐
│   SENDING    │ ← Send via Office 365
└─────┬────────┘
      │
      │ Email sent
      ▼
┌──────────────┐
│ RESPONDING   │ ← Build HTTP response
└─────┬────────┘
      │
      │ Response ready
      ▼
┌──────────────┐
│   SUCCESS    │
└──────────────┘

Note: Any failure in any state results in ERROR state
```

---

**Legend:**

```
┌─────┐  ┏━━━━━┓  ╔═════╗
│ Box │  ┃ Bold┃  ║Thick║  Different box styles
└─────┘  ┗━━━━━┛  ╚═════╝

   │        ▼        →        Flow direction arrows

┌──┴──┐                     Decision point
│ Yes/No│
└──┬──┘
```

---

This diagram provides a complete visual reference for understanding
the flow structure, data transformations, and execution sequence.
