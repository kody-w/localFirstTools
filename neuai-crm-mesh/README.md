# NeuAI CRM Data Mesh

A unified platform for managing CRM data across Salesforce, Dynamics 365, and Local-First CRM systems. This tool solves the hardest challenge in CRM management: **seamless data migration and synchronization between platforms**.

## Features

- **Schema Translation** - Automatically translate records between Salesforce, Dynamics 365, and Local CRM formats
- **Duplicate Detection** - Find matching records across all connected platforms
- **Conflict Resolution** - Identify and resolve data conflicts before migration
- **Bidirectional Sync** - Sync data in any direction between platforms
- **Natural Language Interface** - Query your CRM data using plain English
- **REST API** - Full API for integration with frontend applications
- **CLI Tools** - Command-line interface for automation and scripting

## Quick Start

### Installation

```bash
# Clone or navigate to the directory
cd neuai-crm-mesh

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Start the API Server

```bash
# Default port 8080
python -m neuai_crm serve

# Custom port
python -m neuai_crm serve --port 3000

# With debug mode
python -m neuai_crm serve --port 8080 --debug
```

### CLI Usage

```bash
# Translate Salesforce data to Dynamics 365
python -m neuai_crm translate \
  --from salesforce \
  --to dynamics365 \
  --file examples/salesforce-data.json \
  --output dynamics-output.json

# Detect duplicates across platforms
python -m neuai_crm detect-duplicates \
  --salesforce examples/salesforce-data.json \
  --dynamics examples/dynamics-data.json \
  --local examples/local-data.json

# Sync platforms
python -m neuai_crm sync \
  --source salesforce \
  --target dynamics365 \
  --source-file examples/salesforce-data.json

# Migrate with conflict checking
python -m neuai_crm migrate \
  --from salesforce \
  --to dynamics365 \
  --source-file examples/salesforce-data.json \
  --output migrated-data.json

# Natural language query
python -m neuai_crm query "How many contacts are in each CRM?"

# Show statistics
python -m neuai_crm stats \
  --salesforce examples/salesforce-data.json \
  --dynamics examples/dynamics-data.json
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and health check |
| `/health` | GET | Health status |
| `/stats` | GET | Record counts across platforms |
| `/schema` | GET | Schema mappings reference |
| `/query` | POST | Natural language query processing |
| `/translate` | POST | Translate a record between platforms |
| `/sync` | POST | Sync data between platforms |
| `/duplicates` | GET | Detect duplicate records |
| `/conflicts/{source}/{target}` | GET | Get conflicts between platforms |
| `/load` | POST | Load data into a platform |
| `/export/{platform}` | GET | Export data in platform format |
| `/sync-log` | GET | View sync operation history |

### Example API Calls

```bash
# Get statistics
curl http://localhost:8080/stats

# Natural language query
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Find duplicates across all systems"}'

# Translate a record
curl -X POST http://localhost:8080/translate \
  -H "Content-Type: application/json" \
  -d '{
    "record": {"FirstName": "John", "LastName": "Doe", "Email": "john@example.com"},
    "from_platform": "salesforce",
    "to_platform": "dynamics365",
    "entity_type": "contacts"
  }'

# Sync platforms
curl -X POST http://localhost:8080/sync \
  -H "Content-Type: application/json" \
  -d '{"source": "salesforce", "target": "dynamics365"}'

# Load data
curl -X POST http://localhost:8080/load \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "salesforce",
    "data": {
      "Account": [{"Id": "001", "Name": "Acme Corp"}],
      "Contact": [{"Id": "003", "FirstName": "John", "LastName": "Doe"}]
    }
  }'

# Export data
curl http://localhost:8080/export/dynamics365
```

## Schema Mappings

### Entity Mappings

| Local CRM | Salesforce | Dynamics 365 |
|-----------|------------|--------------|
| companies | Account | account |
| contacts | Contact | contact |
| deals | Opportunity | opportunity |
| activities | Task | activitypointer |

### Field Mappings (Contacts)

| Concept | Local CRM | Salesforce | Dynamics 365 |
|---------|-----------|------------|--------------|
| First Name | firstName | FirstName | firstname |
| Last Name | lastName | LastName | lastname |
| Email | email | Email | emailaddress1 |
| Phone | phone | Phone | telephone1 |
| Company Link | companyId | AccountId | parentcustomerid |
| Job Title | jobTitle | Title | jobtitle |

### Stage Mappings (Deals/Opportunities)

| Local CRM | Salesforce | Dynamics 365 |
|-----------|------------|--------------|
| lead | Prospecting | 1 - Qualify |
| qualified | Qualification | 2 - Develop |
| proposal | Proposal/Price Quote | 3 - Propose |
| negotiation | Negotiation/Review | 4 - Close |
| won | Closed Won | Won |
| lost | Closed Lost | Lost |

## Project Structure

```
neuai-crm-mesh/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation
├── Dockerfile               # Container deployment
├── docker-compose.yml       # Multi-service deployment
├── config/
│   └── settings.py          # Configuration settings
├── neuai_crm/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── entities.py      # Data models (Contact, Company, Deal, Activity)
│   │   └── schemas.py       # Schema mapping definitions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_mesh.py     # Data mesh operations
│   │   ├── translator.py    # Schema translation
│   │   ├── duplicates.py    # Duplicate detection
│   │   └── intelligence.py  # AI/NLP query processing
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py        # FastAPI/Flask server
│   │   └── routes.py        # API route definitions
│   └── cli/
│       ├── __init__.py
│       └── commands.py      # CLI command implementations
├── examples/
│   ├── salesforce-data.json
│   ├── dynamics-data.json
│   └── local-data.json
└── tests/
    ├── __init__.py
    ├── test_translator.py
    ├── test_duplicates.py
    └── test_api.py
```

## Integration with Frontend

The API is designed to work with the NeuAI CRM Assistant frontend (`neuai-crm-assistant.html`). The frontend can:

1. Connect to the API at the configured endpoint
2. Send natural language queries via `/query`
3. Load/export data via `/load` and `/export`
4. Monitor sync status via `/stats` and `/sync-log`

### Frontend Configuration

In `neuai-crm-assistant.html`, update the API endpoint:

```javascript
const API_BASE = 'http://localhost:8080';

// Example: Process a query
async function processQuery(query) {
    const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    });
    return response.json();
}
```

## Docker Deployment

```bash
# Build the image
docker build -t neuai-crm-mesh .

# Run the container
docker run -p 8080:8080 neuai-crm-mesh

# Or use docker-compose
docker-compose up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | API server port |
| `HOST` | 0.0.0.0 | API server host |
| `DEBUG` | false | Enable debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `CORS_ORIGINS` | * | Allowed CORS origins |

## License

MIT License - Feel free to use and modify for your needs.
