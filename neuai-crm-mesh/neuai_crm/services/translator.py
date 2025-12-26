"""
Schema translation service for converting records between CRM platforms.
"""

from typing import Dict, List, Any, Optional
from neuai_crm.models.schemas import (
    Platform,
    SCHEMA_MAPPINGS,
    get_field_mapping,
    translate_stage,
    get_local_entity_name,
)
from neuai_crm.models.entities import Contact, Company, Deal, Activity


class SchemaTranslator:
    """
    Translates CRM records between Salesforce, Dynamics 365, and Local CRM formats.
    """

    def __init__(self):
        self.schema = SCHEMA_MAPPINGS

    def translate_record(
        self,
        record: Dict,
        from_platform: Platform,
        to_platform: Platform,
        entity_type: str
    ) -> Dict:
        """
        Translate a single record from one platform format to another.

        Args:
            record: The record to translate
            from_platform: Source platform
            to_platform: Target platform
            entity_type: Type of entity (contacts, companies, deals, activities)

        Returns:
            Translated record in target platform format
        """
        # Normalize entity type to local format
        local_entity = get_local_entity_name(entity_type, from_platform)

        # Get field mappings
        from_fields = self.schema["fields"].get(local_entity, {}).get(from_platform.value, [])
        to_fields = self.schema["fields"].get(local_entity, {}).get(to_platform.value, [])

        translated = {}
        for i, from_field in enumerate(from_fields):
            if i < len(to_fields) and from_field in record:
                value = record[from_field]

                # Handle stage translation for deals/opportunities
                if self._is_stage_field(from_field):
                    value = translate_stage(value, from_platform, to_platform)

                # Handle status translation for activities
                if self._is_status_field(from_field):
                    value = self._translate_status(value, from_platform, to_platform)

                translated[to_fields[i]] = value

        return translated

    def translate_entity(
        self,
        record: Dict,
        from_platform: Platform,
        to_platform: Platform,
        entity_type: str
    ) -> Any:
        """
        Translate a record using strongly-typed entity classes.

        Args:
            record: The record to translate
            from_platform: Source platform
            to_platform: Target platform
            entity_type: Type of entity

        Returns:
            Translated record as platform-specific dict
        """
        local_entity = get_local_entity_name(entity_type, from_platform)

        entity_class = {
            "contacts": Contact,
            "companies": Company,
            "deals": Deal,
            "activities": Activity
        }.get(local_entity)

        if entity_class:
            entity = entity_class.from_platform(record, from_platform)
            return entity.to_platform(to_platform)

        # Fallback to generic translation
        return self.translate_record(record, from_platform, to_platform, entity_type)

    def translate_batch(
        self,
        records: List[Dict],
        from_platform: Platform,
        to_platform: Platform,
        entity_type: str
    ) -> List[Dict]:
        """
        Translate a batch of records.

        Args:
            records: List of records to translate
            from_platform: Source platform
            to_platform: Target platform
            entity_type: Type of entity

        Returns:
            List of translated records
        """
        return [
            self.translate_entity(record, from_platform, to_platform, entity_type)
            for record in records
        ]

    def get_field_mapping(
        self,
        entity_type: str,
        from_platform: Platform,
        to_platform: Platform
    ) -> Dict[str, str]:
        """
        Get the field mapping between two platforms for an entity type.

        Args:
            entity_type: Type of entity
            from_platform: Source platform
            to_platform: Target platform

        Returns:
            Dictionary mapping source fields to target fields
        """
        return get_field_mapping(entity_type, from_platform, to_platform)

    def _is_stage_field(self, field_name: str) -> bool:
        """Check if a field is a stage/pipeline field."""
        stage_fields = ["stage", "StageName", "stepname"]
        return field_name in stage_fields

    def _is_status_field(self, field_name: str) -> bool:
        """Check if a field is a status field."""
        status_fields = ["status", "Status", "statecode"]
        return field_name in status_fields

    def _translate_status(
        self,
        status: Any,
        from_platform: Platform,
        to_platform: Platform
    ) -> Any:
        """Translate activity status between platforms."""
        from_statuses = self.schema["status"].get(from_platform.value, [])
        to_statuses = self.schema["status"].get(to_platform.value, [])

        try:
            idx = from_statuses.index(status)
            return to_statuses[idx] if idx < len(to_statuses) else status
        except (ValueError, IndexError):
            return status


# Global translator instance
translator = SchemaTranslator()
