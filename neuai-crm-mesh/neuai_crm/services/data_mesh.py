"""
Data Mesh service - unified data store for managing records across CRM platforms.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS
from neuai_crm.services.translator import SchemaTranslator
from neuai_crm.services.duplicates import DuplicateDetector, DuplicateMatch


class DataMesh:
    """
    Unified data store managing records across all CRM platforms.

    The DataMesh serves as the central hub for:
    - Loading and storing data from multiple CRM platforms
    - Translating records between platform formats
    - Syncing data between platforms
    - Detecting duplicates and conflicts
    """

    def __init__(self):
        """Initialize the data mesh with empty data stores."""
        self.data: Dict[Platform, Dict[str, List[Dict]]] = {
            Platform.SALESFORCE: {"accounts": [], "contacts": [], "opportunities": [], "tasks": []},
            Platform.DYNAMICS365: {"accounts": [], "contacts": [], "opportunities": [], "activities": []},
            Platform.LOCAL: {"companies": [], "contacts": [], "deals": [], "activities": []}
        }
        self.id_mappings: Dict[str, Dict[Platform, str]] = {}
        self.sync_log: List[Dict] = []
        self.translator = SchemaTranslator()
        self.duplicate_detector = DuplicateDetector()

    def load_from_file(self, platform: Platform, filepath: str) -> Dict:
        """
        Load data from a JSON file into the mesh.

        Args:
            platform: The platform to load data into
            filepath: Path to the JSON file

        Returns:
            Status dict with records loaded count
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        normalized = self._normalize_import(platform, data)
        self.data[platform] = normalized

        self._log_operation("load", platform=platform.value, file=filepath,
                           records=sum(len(v) for v in normalized.values()))

        return {
            "status": "success",
            "records_loaded": sum(len(v) for v in normalized.values())
        }

    def load_data(self, platform: Platform, data: Dict) -> Dict:
        """
        Load data directly into the mesh.

        Args:
            platform: The platform to load data into
            data: The data to load

        Returns:
            Status dict with records loaded count
        """
        normalized = self._normalize_import(platform, data)
        self.data[platform] = normalized

        self._log_operation("load", platform=platform.value,
                           records=sum(len(v) for v in normalized.values()))

        return {
            "status": "success",
            "records_loaded": sum(len(v) for v in normalized.values())
        }

    def _normalize_import(self, platform: Platform, data: Dict) -> Dict:
        """Normalize imported data to platform's expected structure."""
        if platform == Platform.SALESFORCE:
            return {
                "accounts": data.get("Account", data.get("accounts", [])),
                "contacts": data.get("Contact", data.get("contacts", [])),
                "opportunities": data.get("Opportunity", data.get("opportunities", [])),
                "tasks": data.get("Task", data.get("tasks", []))
            }
        elif platform == Platform.DYNAMICS365:
            return {
                "accounts": data.get("account", data.get("accounts", [])),
                "contacts": data.get("contact", data.get("contacts", [])),
                "opportunities": data.get("opportunity", data.get("opportunities", [])),
                "activities": data.get("activitypointer", data.get("activities", []))
            }
        else:  # LOCAL
            return {
                "companies": data.get("companies", []),
                "contacts": data.get("contacts", []),
                "deals": data.get("deals", []),
                "activities": data.get("activities", [])
            }

    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get record counts across all platforms.

        Returns:
            Dict mapping platform names to entity counts
        """
        return {
            platform.value: {
                entity: len(records)
                for entity, records in self.data[platform].items()
            }
            for platform in Platform
        }

    def translate_record(
        self,
        record: Dict,
        from_platform: Platform,
        to_platform: Platform,
        entity_type: str
    ) -> Dict:
        """
        Translate a single record between platforms.

        Args:
            record: The record to translate
            from_platform: Source platform
            to_platform: Target platform
            entity_type: Type of entity

        Returns:
            Translated record
        """
        return self.translator.translate_entity(
            record, from_platform, to_platform, entity_type
        )

    def sync_platforms(self, source: Platform, target: Platform) -> Dict:
        """
        Sync all data from source to target platform.

        Args:
            source: Source platform
            target: Target platform

        Returns:
            Dict with sync results
        """
        results = {"synced": 0, "errors": [], "entity_counts": {}}

        entity_mapping = {
            Platform.LOCAL: ["companies", "contacts", "deals", "activities"],
            Platform.SALESFORCE: ["accounts", "contacts", "opportunities", "tasks"],
            Platform.DYNAMICS365: ["accounts", "contacts", "opportunities", "activities"]
        }

        source_entities = entity_mapping[source]
        target_entities = entity_mapping[target]

        for i, source_entity in enumerate(source_entities):
            target_entity = target_entities[i]
            source_records = self.data[source].get(source_entity, [])
            translated_records = []

            for record in source_records:
                try:
                    translated = self.translator.translate_entity(
                        record, source, target, source_entity
                    )
                    translated_records.append(translated)
                    results["synced"] += 1
                except Exception as e:
                    results["errors"].append({
                        "record": record,
                        "error": str(e)
                    })

            self.data[target][target_entity] = translated_records
            results["entity_counts"][target_entity] = len(translated_records)

        self._log_operation("sync", source=source.value, target=target.value,
                           records=results["synced"])

        return results

    def detect_duplicates(self, threshold: float = 0.8) -> List[Dict]:
        """
        Detect duplicate records across all platforms.

        Args:
            threshold: Minimum confidence for a match

        Returns:
            List of duplicate matches
        """
        self.duplicate_detector.threshold = threshold
        duplicates = self.duplicate_detector.detect_duplicates(self.data)
        return [d.to_dict() for d in duplicates]

    def get_conflicts(self, source: Platform, target: Platform) -> List[Dict]:
        """
        Identify conflicting records between platforms.

        Args:
            source: Source platform
            target: Target platform

        Returns:
            List of conflicts
        """
        conflicts = []
        duplicates = self.duplicate_detector.detect_duplicates(self.data)

        for dup in duplicates:
            source_records = [r for r in dup.records if r["platform"] == source.value]
            target_records = [r for r in dup.records if r["platform"] == target.value]

            if source_records and target_records:
                conflicts.append({
                    "type": dup.entity_type,
                    "match_field": dup.match_field,
                    "match_value": dup.match_value,
                    "source_record": source_records[0]["record"],
                    "target_record": target_records[0]["record"],
                    "recommendation": "merge"
                })

        return conflicts

    def resolve_conflict(
        self,
        conflict_id: str,
        resolution: str,
        merged_record: Optional[Dict] = None
    ) -> Dict:
        """
        Resolve a specific conflict.

        Args:
            conflict_id: ID of the conflict
            resolution: Resolution strategy (keep_source, keep_target, merge)
            merged_record: Merged record if resolution is "merge"

        Returns:
            Resolution status
        """
        self._log_operation("resolve_conflict", conflict_id=conflict_id,
                           resolution=resolution)

        return {
            "status": "resolved",
            "conflict_id": conflict_id,
            "resolution": resolution,
            "timestamp": datetime.now().isoformat()
        }

    def export_to_platform(self, platform: Platform) -> Dict:
        """
        Export all data in platform-specific format.

        Args:
            platform: The platform format to export in

        Returns:
            Data in platform-specific format
        """
        if platform == Platform.SALESFORCE:
            return {
                "Account": self.data[platform]["accounts"],
                "Contact": self.data[platform]["contacts"],
                "Opportunity": self.data[platform]["opportunities"],
                "Task": self.data[platform]["tasks"]
            }
        elif platform == Platform.DYNAMICS365:
            return {
                "account": self.data[platform]["accounts"],
                "contact": self.data[platform]["contacts"],
                "opportunity": self.data[platform]["opportunities"],
                "activitypointer": self.data[platform]["activities"]
            }
        else:  # LOCAL
            return {
                "companies": self.data[platform]["companies"],
                "contacts": self.data[platform]["contacts"],
                "deals": self.data[platform]["deals"],
                "activities": self.data[platform]["activities"]
            }

    def save_to_file(self, platform: Platform, filepath: str) -> Dict:
        """
        Save platform data to a JSON file.

        Args:
            platform: The platform to export
            filepath: Path to save the file

        Returns:
            Status dict
        """
        data = self.export_to_platform(platform)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return {
            "status": "success",
            "file": filepath,
            "records": sum(len(v) for v in data.values())
        }

    def get_sync_log(self) -> List[Dict]:
        """Get the sync operation log."""
        return self.sync_log

    def clear_platform(self, platform: Platform) -> Dict:
        """
        Clear all data for a platform.

        Args:
            platform: The platform to clear

        Returns:
            Status dict
        """
        if platform == Platform.SALESFORCE:
            self.data[platform] = {"accounts": [], "contacts": [], "opportunities": [], "tasks": []}
        elif platform == Platform.DYNAMICS365:
            self.data[platform] = {"accounts": [], "contacts": [], "opportunities": [], "activities": []}
        else:
            self.data[platform] = {"companies": [], "contacts": [], "deals": [], "activities": []}

        self._log_operation("clear", platform=platform.value)

        return {"status": "success", "platform": platform.value}

    def _log_operation(self, action: str, **kwargs) -> None:
        """Log an operation to the sync log."""
        self.sync_log.append({
            "action": action,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        })


# Global data mesh instance
data_mesh = DataMesh()
