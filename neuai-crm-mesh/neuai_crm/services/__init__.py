"""Service layer for NeuAI CRM Data Mesh."""

from neuai_crm.services.data_mesh import DataMesh
from neuai_crm.services.translator import SchemaTranslator
from neuai_crm.services.duplicates import DuplicateDetector
from neuai_crm.services.intelligence import IntelligenceLayer

__all__ = [
    "DataMesh",
    "SchemaTranslator",
    "DuplicateDetector",
    "IntelligenceLayer",
]
