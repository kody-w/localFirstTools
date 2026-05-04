# Live CRM API Implementation Guide

This document outlines the code changes needed to connect NeuAI CRM Data Mesh to live Salesforce and Dynamics 365 APIs.

---

## Current Architecture

The current implementation works with **local JSON files**:

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   CLI/API       │────▶│   DataMesh   │────▶│   JSON Files    │
│   commands.py   │     │   data_mesh  │     │   (local)       │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

## Target Architecture

With live API connectors:

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   CLI/API       │────▶│   DataMesh   │────▶│   Connectors    │
│   commands.py   │     │   data_mesh  │     │                 │
└─────────────────┘     └──────────────┘     │ ┌─────────────┐ │
                                             │ │ Salesforce  │ │
                                             │ │ Connector   │ │
                                             │ └─────────────┘ │
                                             │ ┌─────────────┐ │
                                             │ │ Dynamics365 │ │
                                             │ │ Connector   │ │
                                             │ └─────────────┘ │
                                             │ ┌─────────────┐ │
                                             │ │ Local File  │ │
                                             │ │ Connector   │ │
                                             │ └─────────────┘ │
                                             └─────────────────┘
```

---

## Required Dependencies

Add to `requirements.txt`:

```text
# Salesforce
simple-salesforce>=1.12.5

# Dynamics 365 / Azure AD
msal>=1.24.0
requests>=2.31.0

# Environment
python-dotenv>=1.0.0

# Async support (optional)
aiohttp>=3.9.0
```

Install:
```bash
pip install simple-salesforce msal requests python-dotenv aiohttp
```

---

## Implementation Plan

### File Structure

```
neuai-crm-mesh/
├── neuai_crm/
│   ├── connectors/           # NEW: API connectors
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract base connector
│   │   ├── salesforce.py     # Salesforce API connector
│   │   ├── dynamics365.py    # Dynamics 365 API connector
│   │   └── local.py          # Local file connector (existing)
│   ├── services/
│   │   └── data_mesh.py      # Update to use connectors
│   └── ...
├── config/
│   └── settings.py           # Update with CRM credentials
└── ...
```

---

## Step 1: Base Connector Interface

Create `neuai_crm/connectors/base.py`:

```python
"""Base connector interface for CRM platforms."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"


@dataclass
class ConnectionInfo:
    status: ConnectionStatus
    platform: str
    message: str = ""
    api_version: str = ""
    user: str = ""
    org_id: str = ""


class BaseConnector(ABC):
    """Abstract base class for CRM connectors."""

    def __init__(self):
        self.connection_info: Optional[ConnectionInfo] = None

    @abstractmethod
    async def connect(self) -> ConnectionInfo:
        """Establish connection to the CRM."""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Close the connection."""
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if connection is valid."""
        pass

    # CRUD Operations
    @abstractmethod
    async def get_accounts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve accounts/companies."""
        pass

    @abstractmethod
    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve contacts."""
        pass

    @abstractmethod
    async def get_opportunities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve opportunities/deals."""
        pass

    @abstractmethod
    async def get_activities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Retrieve activities/tasks."""
        pass

    @abstractmethod
    async def create_record(self, entity_type: str, data: Dict) -> Dict:
        """Create a new record."""
        pass

    @abstractmethod
    async def update_record(self, entity_type: str, record_id: str, data: Dict) -> Dict:
        """Update an existing record."""
        pass

    @abstractmethod
    async def delete_record(self, entity_type: str, record_id: str) -> bool:
        """Delete a record."""
        pass

    # Batch Operations
    @abstractmethod
    async def bulk_create(self, entity_type: str, records: List[Dict]) -> Dict:
        """Create multiple records."""
        pass

    @abstractmethod
    async def bulk_update(self, entity_type: str, records: List[Dict]) -> Dict:
        """Update multiple records."""
        pass

    # Query
    @abstractmethod
    async def query(self, query_string: str) -> List[Dict]:
        """Execute a platform-specific query."""
        pass

    # Metadata
    @abstractmethod
    async def get_schema(self, entity_type: str) -> Dict:
        """Get schema/metadata for an entity type."""
        pass

    @abstractmethod
    async def get_record_count(self, entity_type: str) -> int:
        """Get total record count for an entity type."""
        pass
```

---

## Step 2: Salesforce Connector

Create `neuai_crm/connectors/salesforce.py`:

```python
"""Salesforce API connector using simple-salesforce."""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from simple_salesforce import Salesforce, SalesforceLogin
from simple_salesforce.exceptions import SalesforceError

from .base import BaseConnector, ConnectionInfo, ConnectionStatus

logger = logging.getLogger(__name__)


class SalesforceConnector(BaseConnector):
    """Connector for Salesforce CRM using REST API."""

    # Entity type mapping: internal -> Salesforce
    ENTITY_MAP = {
        "accounts": "Account",
        "contacts": "Contact",
        "opportunities": "Opportunity",
        "tasks": "Task",
    }

    # Field mappings for standard entities
    FIELD_MAPS = {
        "Account": {
            "id": "Id",
            "name": "Name",
            "website": "Website",
            "phone": "Phone",
            "industry": "Industry",
            "description": "Description",
            "created_at": "CreatedDate",
            "updated_at": "LastModifiedDate",
        },
        "Contact": {
            "id": "Id",
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "Email",
            "phone": "Phone",
            "title": "Title",
            "account_id": "AccountId",
            "created_at": "CreatedDate",
            "updated_at": "LastModifiedDate",
        },
        "Opportunity": {
            "id": "Id",
            "name": "Name",
            "amount": "Amount",
            "stage": "StageName",
            "close_date": "CloseDate",
            "account_id": "AccountId",
            "probability": "Probability",
            "created_at": "CreatedDate",
            "updated_at": "LastModifiedDate",
        },
        "Task": {
            "id": "Id",
            "subject": "Subject",
            "description": "Description",
            "status": "Status",
            "priority": "Priority",
            "due_date": "ActivityDate",
            "contact_id": "WhoId",
            "account_id": "WhatId",
            "created_at": "CreatedDate",
            "updated_at": "LastModifiedDate",
        },
    }

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        security_token: Optional[str] = None,
        domain: str = "login",
    ):
        super().__init__()
        self.client_id = client_id or os.getenv("SALESFORCE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SALESFORCE_CLIENT_SECRET")
        self.username = username or os.getenv("SALESFORCE_USERNAME")
        self.password = password or os.getenv("SALESFORCE_PASSWORD")
        self.security_token = security_token or os.getenv("SALESFORCE_SECURITY_TOKEN", "")
        self.domain = domain or os.getenv("SALESFORCE_DOMAIN", "login").replace(".salesforce.com", "")

        self.sf: Optional[Salesforce] = None

    async def connect(self) -> ConnectionInfo:
        """Connect to Salesforce using username-password flow."""
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password + self.security_token,
                client_id=self.client_id,
                domain=self.domain,
            )

            # Get user info
            user_info = self.sf.query(
                f"SELECT Id, Name, Email FROM User WHERE Username = '{self.username}'"
            )

            self.connection_info = ConnectionInfo(
                status=ConnectionStatus.CONNECTED,
                platform="salesforce",
                message="Successfully connected to Salesforce",
                api_version=self.sf.sf_version,
                user=self.username,
                org_id=self.sf.sf_instance,
            )

            logger.info(f"Connected to Salesforce: {self.sf.sf_instance}")
            return self.connection_info

        except SalesforceError as e:
            self.connection_info = ConnectionInfo(
                status=ConnectionStatus.ERROR,
                platform="salesforce",
                message=str(e),
            )
            logger.error(f"Salesforce connection error: {e}")
            raise

    async def disconnect(self) -> bool:
        """Disconnect from Salesforce."""
        # Salesforce REST API doesn't require explicit disconnect
        self.sf = None
        self.connection_info = ConnectionInfo(
            status=ConnectionStatus.DISCONNECTED,
            platform="salesforce",
        )
        return True

    async def test_connection(self) -> bool:
        """Test Salesforce connection."""
        if not self.sf:
            return False
        try:
            self.sf.query("SELECT Id FROM Account LIMIT 1")
            return True
        except SalesforceError:
            return False

    async def get_accounts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Salesforce Accounts."""
        query = f"""
            SELECT Id, Name, Website, Phone, Industry, Description,
                   CreatedDate, LastModifiedDate
            FROM Account
            ORDER BY LastModifiedDate DESC
            LIMIT {limit} OFFSET {offset}
        """
        result = self.sf.query(query)
        return [self._normalize_record("Account", r) for r in result["records"]]

    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Salesforce Contacts."""
        query = f"""
            SELECT Id, FirstName, LastName, Email, Phone, Title, AccountId,
                   CreatedDate, LastModifiedDate
            FROM Contact
            ORDER BY LastModifiedDate DESC
            LIMIT {limit} OFFSET {offset}
        """
        result = self.sf.query(query)
        return [self._normalize_record("Contact", r) for r in result["records"]]

    async def get_opportunities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Salesforce Opportunities."""
        query = f"""
            SELECT Id, Name, Amount, StageName, CloseDate, AccountId, Probability,
                   CreatedDate, LastModifiedDate
            FROM Opportunity
            ORDER BY LastModifiedDate DESC
            LIMIT {limit} OFFSET {offset}
        """
        result = self.sf.query(query)
        return [self._normalize_record("Opportunity", r) for r in result["records"]]

    async def get_activities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Salesforce Tasks."""
        query = f"""
            SELECT Id, Subject, Description, Status, Priority, ActivityDate,
                   WhoId, WhatId, CreatedDate, LastModifiedDate
            FROM Task
            ORDER BY LastModifiedDate DESC
            LIMIT {limit} OFFSET {offset}
        """
        result = self.sf.query(query)
        return [self._normalize_record("Task", r) for r in result["records"]]

    async def create_record(self, entity_type: str, data: Dict) -> Dict:
        """Create a Salesforce record."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        sf_data = self._denormalize_record(sf_entity, data)

        # Remove read-only fields
        sf_data.pop("Id", None)
        sf_data.pop("CreatedDate", None)
        sf_data.pop("LastModifiedDate", None)

        result = getattr(self.sf, sf_entity).create(sf_data)
        return {"id": result["id"], "success": result["success"]}

    async def update_record(self, entity_type: str, record_id: str, data: Dict) -> Dict:
        """Update a Salesforce record."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        sf_data = self._denormalize_record(sf_entity, data)

        # Remove read-only fields
        sf_data.pop("Id", None)
        sf_data.pop("CreatedDate", None)
        sf_data.pop("LastModifiedDate", None)

        getattr(self.sf, sf_entity).update(record_id, sf_data)
        return {"id": record_id, "success": True}

    async def delete_record(self, entity_type: str, record_id: str) -> bool:
        """Delete a Salesforce record."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        getattr(self.sf, sf_entity).delete(record_id)
        return True

    async def bulk_create(self, entity_type: str, records: List[Dict]) -> Dict:
        """Bulk create Salesforce records."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        sf_records = [self._denormalize_record(sf_entity, r) for r in records]

        # Remove read-only fields from all records
        for r in sf_records:
            r.pop("Id", None)
            r.pop("CreatedDate", None)
            r.pop("LastModifiedDate", None)

        results = getattr(self.sf.bulk, sf_entity).insert(sf_records)

        success_count = sum(1 for r in results if r.get("success"))
        return {
            "total": len(records),
            "success": success_count,
            "failed": len(records) - success_count,
            "results": results,
        }

    async def bulk_update(self, entity_type: str, records: List[Dict]) -> Dict:
        """Bulk update Salesforce records."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        sf_records = [self._denormalize_record(sf_entity, r) for r in records]

        results = getattr(self.sf.bulk, sf_entity).update(sf_records)

        success_count = sum(1 for r in results if r.get("success"))
        return {
            "total": len(records),
            "success": success_count,
            "failed": len(records) - success_count,
            "results": results,
        }

    async def query(self, query_string: str) -> List[Dict]:
        """Execute a SOQL query."""
        result = self.sf.query_all(query_string)
        return result["records"]

    async def get_schema(self, entity_type: str) -> Dict:
        """Get Salesforce object metadata."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        describe = getattr(self.sf, sf_entity).describe()
        return {
            "name": describe["name"],
            "label": describe["label"],
            "fields": [
                {
                    "name": f["name"],
                    "label": f["label"],
                    "type": f["type"],
                    "required": not f["nillable"] and not f["defaultedOnCreate"],
                }
                for f in describe["fields"]
            ],
        }

    async def get_record_count(self, entity_type: str) -> int:
        """Get total record count."""
        sf_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        result = self.sf.query(f"SELECT COUNT() FROM {sf_entity}")
        return result["totalSize"]

    def _normalize_record(self, entity_type: str, record: Dict) -> Dict:
        """Convert Salesforce record to normalized format."""
        field_map = self.FIELD_MAPS.get(entity_type, {})
        normalized = {}

        # Reverse the field map
        reverse_map = {v: k for k, v in field_map.items()}

        for sf_field, value in record.items():
            if sf_field == "attributes":
                continue
            normalized_field = reverse_map.get(sf_field, sf_field.lower())
            normalized[normalized_field] = value

        return normalized

    def _denormalize_record(self, entity_type: str, record: Dict) -> Dict:
        """Convert normalized record to Salesforce format."""
        field_map = self.FIELD_MAPS.get(entity_type, {})
        sf_record = {}

        for norm_field, value in record.items():
            sf_field = field_map.get(norm_field, norm_field)
            sf_record[sf_field] = value

        return sf_record
```

---

## Step 3: Dynamics 365 Connector

Create `neuai_crm/connectors/dynamics365.py`:

```python
"""Dynamics 365 / Dataverse API connector using MSAL."""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import requests
from msal import ConfidentialClientApplication

from .base import BaseConnector, ConnectionInfo, ConnectionStatus

logger = logging.getLogger(__name__)


class Dynamics365Connector(BaseConnector):
    """Connector for Dynamics 365 / Dataverse using Web API."""

    # Entity type mapping: internal -> Dataverse
    ENTITY_MAP = {
        "accounts": "accounts",
        "contacts": "contacts",
        "opportunities": "opportunities",
        "activities": "activitypointers",
    }

    # Field mappings for standard entities
    FIELD_MAPS = {
        "accounts": {
            "id": "accountid",
            "name": "name",
            "website": "websiteurl",
            "phone": "telephone1",
            "industry": "industrycode",
            "description": "description",
            "created_at": "createdon",
            "updated_at": "modifiedon",
        },
        "contacts": {
            "id": "contactid",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "emailaddress1",
            "phone": "telephone1",
            "title": "jobtitle",
            "account_id": "_parentcustomerid_value",
            "created_at": "createdon",
            "updated_at": "modifiedon",
        },
        "opportunities": {
            "id": "opportunityid",
            "name": "name",
            "amount": "estimatedvalue",
            "stage": "salesstagecode",
            "close_date": "estimatedclosedate",
            "account_id": "_parentaccountid_value",
            "probability": "closeprobability",
            "created_at": "createdon",
            "updated_at": "modifiedon",
        },
        "activitypointers": {
            "id": "activityid",
            "subject": "subject",
            "description": "description",
            "status": "statecode",
            "priority": "prioritycode",
            "due_date": "scheduledend",
            "contact_id": "_regardingobjectid_value",
            "created_at": "createdon",
            "updated_at": "modifiedon",
        },
    }

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
        environment_url: Optional[str] = None,
        api_version: str = "v9.2",
    ):
        super().__init__()
        self.client_id = client_id or os.getenv("DYNAMICS_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("DYNAMICS_CLIENT_SECRET")
        self.tenant_id = tenant_id or os.getenv("DYNAMICS_TENANT_ID")
        self.environment_url = (
            environment_url or os.getenv("DYNAMICS_ENVIRONMENT_URL", "")
        ).rstrip("/")
        self.api_version = api_version or os.getenv("DYNAMICS_API_VERSION", "v9.2")

        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = [f"{self.environment_url}/.default"]
        self.api_base = f"{self.environment_url}/api/data/{self.api_version}"

        self.msal_app: Optional[ConfidentialClientApplication] = None
        self.access_token: Optional[str] = None

    async def connect(self) -> ConnectionInfo:
        """Connect to Dynamics 365 using client credentials."""
        try:
            self.msal_app = ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=self.authority,
            )

            # Acquire token
            result = self.msal_app.acquire_token_for_client(scopes=self.scope)

            if "access_token" not in result:
                raise Exception(
                    result.get("error_description", "Failed to acquire token")
                )

            self.access_token = result["access_token"]

            # Test connection
            response = self._make_request("GET", "/WhoAmI")
            user_id = response.get("UserId", "")

            self.connection_info = ConnectionInfo(
                status=ConnectionStatus.CONNECTED,
                platform="dynamics365",
                message="Successfully connected to Dynamics 365",
                api_version=self.api_version,
                user=user_id,
                org_id=response.get("OrganizationId", ""),
            )

            logger.info(f"Connected to Dynamics 365: {self.environment_url}")
            return self.connection_info

        except Exception as e:
            self.connection_info = ConnectionInfo(
                status=ConnectionStatus.ERROR,
                platform="dynamics365",
                message=str(e),
            )
            logger.error(f"Dynamics 365 connection error: {e}")
            raise

    async def disconnect(self) -> bool:
        """Disconnect from Dynamics 365."""
        self.access_token = None
        self.msal_app = None
        self.connection_info = ConnectionInfo(
            status=ConnectionStatus.DISCONNECTED,
            platform="dynamics365",
        )
        return True

    async def test_connection(self) -> bool:
        """Test Dynamics 365 connection."""
        if not self.access_token:
            return False
        try:
            self._make_request("GET", "/WhoAmI")
            return True
        except Exception:
            return False

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Prefer": "odata.include-annotations=*",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict:
        """Make an HTTP request to Dynamics 365 API."""
        url = f"{self.api_base}{endpoint}"
        headers = self._get_headers()

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
        )

        if response.status_code == 204:  # No content
            return {}

        if response.status_code >= 400:
            error = response.json().get("error", {})
            raise Exception(
                f"{response.status_code}: {error.get('message', response.text)}"
            )

        return response.json()

    async def get_accounts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Dynamics 365 accounts."""
        params = {
            "$select": "accountid,name,websiteurl,telephone1,industrycode,description,createdon,modifiedon",
            "$top": limit,
            "$skip": offset,
            "$orderby": "modifiedon desc",
        }
        result = self._make_request("GET", "/accounts", params=params)
        return [self._normalize_record("accounts", r) for r in result.get("value", [])]

    async def get_contacts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Dynamics 365 contacts."""
        params = {
            "$select": "contactid,firstname,lastname,emailaddress1,telephone1,jobtitle,_parentcustomerid_value,createdon,modifiedon",
            "$top": limit,
            "$skip": offset,
            "$orderby": "modifiedon desc",
        }
        result = self._make_request("GET", "/contacts", params=params)
        return [self._normalize_record("contacts", r) for r in result.get("value", [])]

    async def get_opportunities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Dynamics 365 opportunities."""
        params = {
            "$select": "opportunityid,name,estimatedvalue,salesstagecode,estimatedclosedate,_parentaccountid_value,closeprobability,createdon,modifiedon",
            "$top": limit,
            "$skip": offset,
            "$orderby": "modifiedon desc",
        }
        result = self._make_request("GET", "/opportunities", params=params)
        return [
            self._normalize_record("opportunities", r) for r in result.get("value", [])
        ]

    async def get_activities(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get Dynamics 365 activity pointers."""
        params = {
            "$select": "activityid,subject,description,statecode,prioritycode,scheduledend,_regardingobjectid_value,createdon,modifiedon",
            "$top": limit,
            "$skip": offset,
            "$orderby": "modifiedon desc",
        }
        result = self._make_request("GET", "/activitypointers", params=params)
        return [
            self._normalize_record("activitypointers", r)
            for r in result.get("value", [])
        ]

    async def create_record(self, entity_type: str, data: Dict) -> Dict:
        """Create a Dynamics 365 record."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        d365_data = self._denormalize_record(d365_entity, data)

        # Remove read-only fields
        for field in ["createdon", "modifiedon"]:
            d365_data.pop(field, None)

        response = self._make_request("POST", f"/{d365_entity}", data=d365_data)

        # Get the created record ID from response headers
        return {"id": response.get("@odata.id", "").split("(")[-1].rstrip(")")}

    async def update_record(self, entity_type: str, record_id: str, data: Dict) -> Dict:
        """Update a Dynamics 365 record."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        d365_data = self._denormalize_record(d365_entity, data)

        # Remove read-only fields and ID
        for field in ["createdon", "modifiedon", f"{d365_entity.rstrip('s')}id"]:
            d365_data.pop(field, None)

        self._make_request("PATCH", f"/{d365_entity}({record_id})", data=d365_data)
        return {"id": record_id, "success": True}

    async def delete_record(self, entity_type: str, record_id: str) -> bool:
        """Delete a Dynamics 365 record."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        self._make_request("DELETE", f"/{d365_entity}({record_id})")
        return True

    async def bulk_create(self, entity_type: str, records: List[Dict]) -> Dict:
        """Bulk create using batch requests."""
        results = []
        for record in records:
            try:
                result = await self.create_record(entity_type, record)
                results.append({"success": True, "id": result.get("id")})
            except Exception as e:
                results.append({"success": False, "error": str(e)})

        success_count = sum(1 for r in results if r.get("success"))
        return {
            "total": len(records),
            "success": success_count,
            "failed": len(records) - success_count,
            "results": results,
        }

    async def bulk_update(self, entity_type: str, records: List[Dict]) -> Dict:
        """Bulk update using batch requests."""
        results = []
        id_field = self._get_id_field(entity_type)

        for record in records:
            try:
                record_id = record.get(id_field) or record.get("id")
                if not record_id:
                    results.append({"success": False, "error": "Missing ID"})
                    continue
                result = await self.update_record(entity_type, record_id, record)
                results.append({"success": True, "id": record_id})
            except Exception as e:
                results.append({"success": False, "error": str(e)})

        success_count = sum(1 for r in results if r.get("success"))
        return {
            "total": len(records),
            "success": success_count,
            "failed": len(records) - success_count,
            "results": results,
        }

    async def query(self, query_string: str) -> List[Dict]:
        """Execute a FetchXML or OData query."""
        # If it looks like FetchXML, use fetchxml endpoint
        if query_string.strip().startswith("<"):
            params = {"fetchXml": query_string}
            result = self._make_request("GET", "/accounts", params=params)
        else:
            # Assume OData query string
            result = self._make_request("GET", f"/{query_string}")

        return result.get("value", [])

    async def get_schema(self, entity_type: str) -> Dict:
        """Get Dynamics 365 entity metadata."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)

        result = self._make_request(
            "GET",
            f"/EntityDefinitions(LogicalName='{d365_entity.rstrip('s')}')",
            params={"$expand": "Attributes"},
        )

        return {
            "name": result.get("LogicalName"),
            "label": result.get("DisplayName", {})
            .get("UserLocalizedLabel", {})
            .get("Label"),
            "fields": [
                {
                    "name": attr.get("LogicalName"),
                    "label": attr.get("DisplayName", {})
                    .get("UserLocalizedLabel", {})
                    .get("Label"),
                    "type": attr.get("AttributeType"),
                    "required": attr.get("RequiredLevel", {}).get("Value")
                    == "ApplicationRequired",
                }
                for attr in result.get("Attributes", [])
            ],
        }

    async def get_record_count(self, entity_type: str) -> int:
        """Get total record count."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        result = self._make_request(
            "GET", f"/{d365_entity}", params={"$count": "true", "$top": "0"}
        )
        return result.get("@odata.count", 0)

    def _get_id_field(self, entity_type: str) -> str:
        """Get the ID field name for an entity type."""
        d365_entity = self.ENTITY_MAP.get(entity_type, entity_type)
        return f"{d365_entity.rstrip('s')}id"

    def _normalize_record(self, entity_type: str, record: Dict) -> Dict:
        """Convert Dynamics record to normalized format."""
        field_map = self.FIELD_MAPS.get(entity_type, {})
        normalized = {}

        # Reverse the field map
        reverse_map = {v: k for k, v in field_map.items()}

        for d365_field, value in record.items():
            if d365_field.startswith("@odata"):
                continue
            normalized_field = reverse_map.get(d365_field, d365_field)
            normalized[normalized_field] = value

        return normalized

    def _denormalize_record(self, entity_type: str, record: Dict) -> Dict:
        """Convert normalized record to Dynamics format."""
        field_map = self.FIELD_MAPS.get(entity_type, {})
        d365_record = {}

        for norm_field, value in record.items():
            d365_field = field_map.get(norm_field, norm_field)
            d365_record[d365_field] = value

        return d365_record
```

---

## Step 4: Update Settings

Update `config/settings.py`:

```python
"""Configuration settings with CRM credentials."""

import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class SalesforceConfig:
    """Salesforce connection settings."""
    client_id: str = field(default_factory=lambda: os.getenv("SALESFORCE_CLIENT_ID", ""))
    client_secret: str = field(default_factory=lambda: os.getenv("SALESFORCE_CLIENT_SECRET", ""))
    username: str = field(default_factory=lambda: os.getenv("SALESFORCE_USERNAME", ""))
    password: str = field(default_factory=lambda: os.getenv("SALESFORCE_PASSWORD", ""))
    security_token: str = field(default_factory=lambda: os.getenv("SALESFORCE_SECURITY_TOKEN", ""))
    domain: str = field(default_factory=lambda: os.getenv("SALESFORCE_DOMAIN", "login"))
    api_version: str = field(default_factory=lambda: os.getenv("SALESFORCE_API_VERSION", "v59.0"))

    @property
    def is_configured(self) -> bool:
        return bool(self.client_id and self.username and self.password)


@dataclass
class Dynamics365Config:
    """Dynamics 365 connection settings."""
    client_id: str = field(default_factory=lambda: os.getenv("DYNAMICS_CLIENT_ID", ""))
    client_secret: str = field(default_factory=lambda: os.getenv("DYNAMICS_CLIENT_SECRET", ""))
    tenant_id: str = field(default_factory=lambda: os.getenv("DYNAMICS_TENANT_ID", ""))
    environment_url: str = field(default_factory=lambda: os.getenv("DYNAMICS_ENVIRONMENT_URL", ""))
    api_version: str = field(default_factory=lambda: os.getenv("DYNAMICS_API_VERSION", "v9.2"))

    @property
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.tenant_id and self.environment_url)


@dataclass
class Settings:
    """Application settings."""

    # Server settings
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8080")))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    # CORS settings
    cors_origins: List[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(",")
    )

    # Logging
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Data persistence
    data_dir: str = field(default_factory=lambda: os.getenv("DATA_DIR", "./data"))

    # Feature flags
    enable_ai_queries: bool = field(
        default_factory=lambda: os.getenv("ENABLE_AI_QUERIES", "true").lower() == "true"
    )
    enable_live_sync: bool = field(
        default_factory=lambda: os.getenv("ENABLE_LIVE_SYNC", "false").lower() == "true"
    )

    # Duplicate detection
    duplicate_threshold: float = field(
        default_factory=lambda: float(os.getenv("DUPLICATE_THRESHOLD", "0.8"))
    )

    # CRM Configurations
    salesforce: SalesforceConfig = field(default_factory=SalesforceConfig)
    dynamics365: Dynamics365Config = field(default_factory=Dynamics365Config)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the current settings instance."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global settings
    settings = Settings()
    return settings
```

---

## Step 5: Update DataMesh Service

Update `neuai_crm/services/data_mesh.py` to use connectors:

```python
# Add imports at top
from neuai_crm.connectors.salesforce import SalesforceConnector
from neuai_crm.connectors.dynamics365 import Dynamics365Connector
from config.settings import get_settings

class DataMesh:
    def __init__(self):
        # ... existing init ...

        # Initialize connectors
        self.connectors = {
            Platform.SALESFORCE: SalesforceConnector(),
            Platform.DYNAMICS365: Dynamics365Connector(),
        }
        self._connected = {
            Platform.SALESFORCE: False,
            Platform.DYNAMICS365: False,
        }

    async def connect_platform(self, platform: Platform) -> bool:
        """Connect to a live CRM platform."""
        if platform == Platform.LOCAL:
            return True  # Local doesn't need connection

        connector = self.connectors.get(platform)
        if not connector:
            return False

        try:
            await connector.connect()
            self._connected[platform] = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {platform}: {e}")
            return False

    async def sync_from_live(self, platform: Platform) -> Dict:
        """Sync data from live CRM into local data store."""
        if not self._connected.get(platform):
            await self.connect_platform(platform)

        connector = self.connectors[platform]

        # Fetch from live API
        accounts = await connector.get_accounts()
        contacts = await connector.get_contacts()
        opportunities = await connector.get_opportunities()
        activities = await connector.get_activities()

        # Store locally
        if platform == Platform.SALESFORCE:
            self.data[platform] = {
                "accounts": accounts,
                "contacts": contacts,
                "opportunities": opportunities,
                "tasks": activities,
            }
        elif platform == Platform.DYNAMICS365:
            self.data[platform] = {
                "accounts": accounts,
                "contacts": contacts,
                "opportunities": opportunities,
                "activities": activities,
            }

        total = len(accounts) + len(contacts) + len(opportunities) + len(activities)
        return {"status": "success", "records_synced": total}

    async def push_to_live(self, platform: Platform) -> Dict:
        """Push local data to live CRM."""
        if not self._connected.get(platform):
            await self.connect_platform(platform)

        connector = self.connectors[platform]
        results = {"created": 0, "updated": 0, "errors": []}

        # Implementation would iterate through local data
        # and create/update records in the live CRM
        # ...

        return results
```

---

## Testing

### Unit Tests

Create `tests/test_connectors.py`:

```python
"""Tests for CRM connectors."""

import pytest
import os
from unittest.mock import Mock, patch

from neuai_crm.connectors.salesforce import SalesforceConnector
from neuai_crm.connectors.dynamics365 import Dynamics365Connector


@pytest.fixture
def sf_connector():
    return SalesforceConnector(
        client_id="test_client",
        client_secret="test_secret",
        username="test@example.com",
        password="test_password",
        security_token="test_token",
    )


@pytest.fixture
def d365_connector():
    return Dynamics365Connector(
        client_id="test-client-id",
        client_secret="test-secret",
        tenant_id="test-tenant-id",
        environment_url="https://test.crm.dynamics.com",
    )


class TestSalesforceConnector:
    @patch("simple_salesforce.Salesforce")
    async def test_connect_success(self, mock_sf, sf_connector):
        mock_sf.return_value.sf_instance = "test.salesforce.com"
        mock_sf.return_value.sf_version = "59.0"
        mock_sf.return_value.query.return_value = {"records": [{"Name": "Test User"}]}

        result = await sf_connector.connect()

        assert result.status.value == "connected"
        assert result.platform == "salesforce"

    async def test_normalize_record(self, sf_connector):
        sf_record = {
            "Id": "001ABC",
            "Name": "Test Account",
            "Website": "https://test.com",
            "attributes": {"type": "Account"},
        }

        normalized = sf_connector._normalize_record("Account", sf_record)

        assert normalized["id"] == "001ABC"
        assert normalized["name"] == "Test Account"
        assert "attributes" not in normalized


class TestDynamics365Connector:
    @patch("msal.ConfidentialClientApplication")
    @patch("requests.request")
    async def test_connect_success(self, mock_request, mock_msal, d365_connector):
        mock_msal.return_value.acquire_token_for_client.return_value = {
            "access_token": "test_token"
        }
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "UserId": "test-user-id",
            "OrganizationId": "test-org-id",
        }

        result = await d365_connector.connect()

        assert result.status.value == "connected"
        assert result.platform == "dynamics365"
```

### Integration Tests

Create `tests/test_integration.py`:

```python
"""Integration tests (requires live credentials)."""

import pytest
import os

# Skip if credentials not available
pytestmark = pytest.mark.skipif(
    not os.getenv("SALESFORCE_CLIENT_ID"),
    reason="Salesforce credentials not configured"
)


class TestSalesforceIntegration:
    @pytest.fixture
    def connector(self):
        from neuai_crm.connectors.salesforce import SalesforceConnector
        return SalesforceConnector()

    async def test_connect_and_query(self, connector):
        await connector.connect()

        accounts = await connector.get_accounts(limit=5)
        assert isinstance(accounts, list)

        await connector.disconnect()
```

---

## CLI Updates

Add new commands for live sync in `cli/commands.py`:

```python
def cmd_connect(args):
    """Connect to live CRM platforms."""
    import asyncio

    async def do_connect():
        if args.platform == "salesforce":
            connector = SalesforceConnector()
        elif args.platform == "dynamics365":
            connector = Dynamics365Connector()
        else:
            print(f"Unknown platform: {args.platform}")
            return

        print(f"Connecting to {args.platform}...")
        result = await connector.connect()
        print(f"Status: {result.status.value}")
        print(f"Message: {result.message}")

        if result.status.value == "connected":
            print(f"User: {result.user}")
            print(f"API Version: {result.api_version}")

    asyncio.run(do_connect())


def cmd_live_sync(args):
    """Sync data from live CRM."""
    import asyncio

    async def do_sync():
        platform = Platform(args.platform)
        result = await data_mesh.sync_from_live(platform)
        print(f"Synced {result['records_synced']} records from {args.platform}")

    asyncio.run(do_sync())
```

---

## Summary

After implementing these changes, the NeuAI CRM Data Mesh will support:

| Feature | File-Based | Live API |
|---------|------------|----------|
| Load data | `load_from_file()` | `sync_from_live()` |
| Save data | `save_to_file()` | `push_to_live()` |
| Real-time sync | N/A | `connect_platform()` |
| Batch operations | Supported | Supported |
| Duplicate detection | Supported | Supported |

### Implementation Priority

1. **Phase 1**: Base connector interface + Salesforce connector
2. **Phase 2**: Dynamics 365 connector
3. **Phase 3**: Bi-directional sync + conflict resolution
4. **Phase 4**: Webhook support for real-time updates

---

*Last updated: December 2024*
