"""Data models for NeuAI CRM Data Mesh."""

from neuai_crm.models.entities import Contact, Company, Deal, Activity
from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS

__all__ = [
    "Contact",
    "Company",
    "Deal",
    "Activity",
    "Platform",
    "SCHEMA_MAPPINGS",
]
