"""
NeuAI CRM Data Mesh
===================

A unified platform for managing CRM data across Salesforce, Dynamics 365, and Local-First CRM.

This package provides:
- Schema translation between all three CRM platforms
- Duplicate detection across platforms
- Conflict resolution for data migrations
- REST API for frontend integration
- CLI tools for automation

Usage:
    # As a library
    from neuai_crm import DataMesh, Platform

    mesh = DataMesh()
    mesh.load_from_file(Platform.SALESFORCE, "data.json")
    result = mesh.sync_platforms(Platform.SALESFORCE, Platform.DYNAMICS365)

    # As CLI
    python -m neuai_crm serve --port 8080
    python -m neuai_crm translate --from salesforce --to dynamics365 --file data.json
"""

__version__ = "1.0.0"
__author__ = "NeuAI"

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS
from neuai_crm.models.entities import Contact, Company, Deal, Activity
from neuai_crm.services.data_mesh import DataMesh
from neuai_crm.services.intelligence import IntelligenceLayer
from neuai_crm.services.translator import SchemaTranslator
from neuai_crm.services.duplicates import DuplicateDetector

__all__ = [
    "Platform",
    "SCHEMA_MAPPINGS",
    "Contact",
    "Company",
    "Deal",
    "Activity",
    "DataMesh",
    "IntelligenceLayer",
    "SchemaTranslator",
    "DuplicateDetector",
]
