"""
Schema definitions and mappings between CRM platforms.
"""

from enum import Enum
from typing import Dict, List


class Platform(str, Enum):
    """Supported CRM platforms."""
    SALESFORCE = "salesforce"
    DYNAMICS365 = "dynamics365"
    LOCAL = "local"


# Complete schema mappings between all platforms
SCHEMA_MAPPINGS: Dict = {
    "entities": {
        "local": {
            "companies": "companies",
            "contacts": "contacts",
            "deals": "deals",
            "activities": "activities"
        },
        "salesforce": {
            "companies": "Account",
            "contacts": "Contact",
            "deals": "Opportunity",
            "activities": "Task"
        },
        "dynamics365": {
            "companies": "account",
            "contacts": "contact",
            "deals": "opportunity",
            "activities": "activitypointer"
        }
    },
    "fields": {
        "contacts": {
            "local": [
                "id", "firstName", "lastName", "email", "phone",
                "companyId", "jobTitle", "createdAt"
            ],
            "salesforce": [
                "Id", "FirstName", "LastName", "Email", "Phone",
                "AccountId", "Title", "CreatedDate"
            ],
            "dynamics365": [
                "contactid", "firstname", "lastname", "emailaddress1", "telephone1",
                "parentcustomerid", "jobtitle", "createdon"
            ]
        },
        "companies": {
            "local": [
                "id", "name", "industry", "website", "phone", "address", "createdAt"
            ],
            "salesforce": [
                "Id", "Name", "Industry", "Website", "Phone", "BillingAddress", "CreatedDate"
            ],
            "dynamics365": [
                "accountid", "name", "industrycode", "websiteurl", "telephone1",
                "address1_composite", "createdon"
            ]
        },
        "deals": {
            "local": [
                "id", "name", "value", "stage", "companyId", "contactId",
                "probability", "closeDate", "createdAt"
            ],
            "salesforce": [
                "Id", "Name", "Amount", "StageName", "AccountId", "ContactId",
                "Probability", "CloseDate", "CreatedDate"
            ],
            "dynamics365": [
                "opportunityid", "name", "estimatedvalue", "stepname", "parentaccountid",
                "parentcontactid", "closeprobability", "estimatedclosedate", "createdon"
            ]
        },
        "activities": {
            "local": [
                "id", "type", "subject", "description", "dueDate",
                "status", "contactId", "dealId", "createdAt"
            ],
            "salesforce": [
                "Id", "TaskSubtype", "Subject", "Description", "ActivityDate",
                "Status", "WhoId", "WhatId", "CreatedDate"
            ],
            "dynamics365": [
                "activityid", "activitytypecode", "subject", "description", "scheduledend",
                "statecode", "regardingobjectid", "regardingobjectid", "createdon"
            ]
        }
    },
    "stages": {
        "local": ["lead", "qualified", "proposal", "negotiation", "won", "lost"],
        "salesforce": [
            "Prospecting", "Qualification", "Proposal/Price Quote",
            "Negotiation/Review", "Closed Won", "Closed Lost"
        ],
        "dynamics365": [
            "1 - Qualify", "2 - Develop", "3 - Propose",
            "4 - Close", "Won", "Lost"
        ]
    },
    "activity_types": {
        "local": ["call", "email", "meeting", "task", "note"],
        "salesforce": ["Call", "Email", "Meeting", "Task", "Note"],
        "dynamics365": ["phonecall", "email", "appointment", "task", "annotation"]
    },
    "status": {
        "local": ["pending", "in_progress", "completed", "cancelled"],
        "salesforce": ["Not Started", "In Progress", "Completed", "Deferred"],
        "dynamics365": [0, 1, 2, 3]  # Open, Completed, Canceled, Scheduled
    }
}


def get_entity_name(local_entity: str, platform: Platform) -> str:
    """Get the platform-specific entity name."""
    return SCHEMA_MAPPINGS["entities"][platform.value].get(local_entity, local_entity)


def get_field_mapping(entity: str, from_platform: Platform, to_platform: Platform) -> Dict[str, str]:
    """Get field mapping between two platforms for an entity."""
    from_fields = SCHEMA_MAPPINGS["fields"].get(entity, {}).get(from_platform.value, [])
    to_fields = SCHEMA_MAPPINGS["fields"].get(entity, {}).get(to_platform.value, [])

    mapping = {}
    for i, from_field in enumerate(from_fields):
        if i < len(to_fields):
            mapping[from_field] = to_fields[i]

    return mapping


def translate_stage(stage: str, from_platform: Platform, to_platform: Platform) -> str:
    """Translate a deal stage between platforms."""
    from_stages = SCHEMA_MAPPINGS["stages"].get(from_platform.value, [])
    to_stages = SCHEMA_MAPPINGS["stages"].get(to_platform.value, [])

    try:
        idx = from_stages.index(stage)
        return to_stages[idx] if idx < len(to_stages) else stage
    except (ValueError, IndexError):
        return stage


def get_local_entity_name(entity_type: str, platform: Platform) -> str:
    """Get the normalized (local) entity name from a platform-specific name."""
    entity_map = SCHEMA_MAPPINGS["entities"][platform.value]
    for local_name, platform_name in entity_map.items():
        if platform_name.lower() == entity_type.lower():
            return local_name
    return entity_type
