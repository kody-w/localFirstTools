"""
Intelligence Layer - AI-powered operations for the CRM data mesh.
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS
from neuai_crm.services.data_mesh import DataMesh


class IntelligenceLayer:
    """
    AI-powered operations for the CRM data mesh.

    Provides natural language query processing and intelligent
    recommendations for data operations.
    """

    def __init__(self, data_mesh: DataMesh):
        """
        Initialize the intelligence layer.

        Args:
            data_mesh: The data mesh instance to operate on
        """
        self.mesh = data_mesh
        self.conversation_history: List[Dict] = []

    def process_query(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Process a natural language query about the CRM data.

        Args:
            query: The natural language query
            context: Optional context dict

        Returns:
            Response dict with intent, action, and result
        """
        query_lower = query.lower()

        # Save to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })

        # Intent detection and handling
        if self._matches_intent(query_lower, ["sync", "synchronize", "update"]):
            response = self._handle_sync_intent(query, context)
        elif self._matches_intent(query_lower, ["migrate", "transfer", "move"]):
            response = self._handle_migrate_intent(query, context)
        elif self._matches_intent(query_lower, ["duplicate", "match", "find similar"]):
            response = self._handle_duplicate_intent(query, context)
        elif self._matches_intent(query_lower, ["conflict", "differ", "mismatch"]):
            response = self._handle_conflict_intent(query, context)
        elif self._matches_intent(query_lower, ["status", "stats", "count", "how many"]):
            response = self._handle_status_intent(query, context)
        elif self._matches_intent(query_lower, ["translate", "convert", "transform"]):
            response = self._handle_translate_intent(query, context)
        elif self._matches_intent(query_lower, ["schema", "mapping", "fields"]):
            response = self._handle_schema_intent(query, context)
        elif self._matches_intent(query_lower, ["help", "what can", "how do"]):
            response = self._handle_help_intent(query, context)
        elif self._matches_intent(query_lower, ["clear", "reset", "delete all"]):
            response = self._handle_clear_intent(query, context)
        elif self._matches_intent(query_lower, ["export", "download", "save"]):
            response = self._handle_export_intent(query, context)
        else:
            response = self._handle_general_intent(query, context)

        # Save response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        return response

    def _matches_intent(self, query: str, keywords: List[str]) -> bool:
        """Check if query matches any of the intent keywords."""
        return any(word in query for word in keywords)

    def _extract_platforms(self, query: str) -> Tuple[Optional[Platform], Optional[Platform]]:
        """Extract source and target platforms from query."""
        query_lower = query.lower()
        platforms_found = []

        if "salesforce" in query_lower or "sf " in query_lower or query_lower.endswith(" sf"):
            platforms_found.append(Platform.SALESFORCE)
        if "dynamics" in query_lower or "d365" in query_lower or "dynamics365" in query_lower:
            platforms_found.append(Platform.DYNAMICS365)
        if "local" in query_lower:
            platforms_found.append(Platform.LOCAL)

        if len(platforms_found) >= 2:
            return platforms_found[0], platforms_found[1]
        elif len(platforms_found) == 1:
            return platforms_found[0], None
        return None, None

    def _handle_sync_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle sync-related queries."""
        source, target = self._extract_platforms(query)

        if source and target:
            result = self.mesh.sync_platforms(source, target)
            return {
                "intent": "sync",
                "action": "sync_executed",
                "source": source.value,
                "target": target.value,
                "result": result,
                "message": f"Synced {result['synced']} records from {source.value} to {target.value}"
            }

        return {
            "intent": "sync",
            "action": "clarification_needed",
            "message": "Please specify source and target platforms. For example: 'Sync Salesforce to Dynamics 365'"
        }

    def _handle_migrate_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle migration-related queries."""
        source, target = self._extract_platforms(query)

        if source and target:
            # Check for conflicts first
            conflicts = self.mesh.get_conflicts(source, target)
            if conflicts:
                return {
                    "intent": "migrate",
                    "action": "conflicts_detected",
                    "conflict_count": len(conflicts),
                    "conflicts": conflicts[:5],  # Show first 5
                    "message": f"Found {len(conflicts)} conflicts between {source.value} and {target.value}. Please resolve before migrating."
                }

            result = self.mesh.sync_platforms(source, target)
            return {
                "intent": "migrate",
                "action": "migration_complete",
                "result": result,
                "message": f"Migration complete: {result['synced']} records moved from {source.value} to {target.value}"
            }

        return {
            "intent": "migrate",
            "action": "clarification_needed",
            "message": "Please specify source and target platforms for migration"
        }

    def _handle_duplicate_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle duplicate detection queries."""
        duplicates = self.mesh.detect_duplicates()

        return {
            "intent": "duplicate_detection",
            "action": "duplicates_found",
            "count": len(duplicates),
            "duplicates": duplicates[:10],  # Limit for response size
            "message": f"Found {len(duplicates)} potential duplicate records across platforms"
        }

    def _handle_conflict_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle conflict detection queries."""
        source, target = self._extract_platforms(query)

        if source and target:
            conflicts = self.mesh.get_conflicts(source, target)
            return {
                "intent": "conflict_detection",
                "action": "conflicts_found",
                "count": len(conflicts),
                "conflicts": conflicts,
                "message": f"Found {len(conflicts)} conflicts between {source.value} and {target.value}"
            }

        # Check all platform pairs
        all_conflicts = []
        platform_pairs = [
            (Platform.SALESFORCE, Platform.DYNAMICS365),
            (Platform.SALESFORCE, Platform.LOCAL),
            (Platform.DYNAMICS365, Platform.LOCAL)
        ]

        for s, t in platform_pairs:
            all_conflicts.extend(self.mesh.get_conflicts(s, t))

        return {
            "intent": "conflict_detection",
            "action": "conflicts_found",
            "count": len(all_conflicts),
            "conflicts": all_conflicts[:10],
            "message": f"Found {len(all_conflicts)} total conflicts across all platforms"
        }

    def _handle_status_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle status/stats queries."""
        stats = self.mesh.get_stats()
        total = sum(sum(v.values()) for v in stats.values())

        return {
            "intent": "status",
            "action": "stats_retrieved",
            "stats": stats,
            "total_records": total,
            "message": f"Total of {total} records across all platforms"
        }

    def _handle_translate_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle translation-related queries."""
        return {
            "intent": "translate",
            "action": "translation_info",
            "supported_platforms": [p.value for p in Platform],
            "supported_entities": ["contacts", "companies", "deals", "activities"],
            "message": "I can translate records between Salesforce, Dynamics 365, and Local CRM. Provide a record to translate."
        }

    def _handle_schema_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle schema/mapping queries."""
        return {
            "intent": "schema",
            "action": "schema_info",
            "schema_mappings": SCHEMA_MAPPINGS,
            "message": "Schema mappings available for all entities between platforms"
        }

    def _handle_help_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle help queries."""
        return {
            "intent": "help",
            "action": "help_provided",
            "capabilities": [
                "Sync data between Salesforce, Dynamics 365, and Local CRM",
                "Detect duplicate records across platforms",
                "Identify and resolve data conflicts",
                "Translate schemas between platforms",
                "Migrate entire datasets between systems",
                "Get statistics on all connected CRMs",
                "Export data in any platform format"
            ],
            "example_queries": [
                "Sync Salesforce to Dynamics 365",
                "Find duplicates across all systems",
                "Show me conflicts between local and Salesforce",
                "How many records are in each CRM?",
                "Migrate from Dynamics to Salesforce",
                "Export data for Salesforce",
                "Show me the schema mappings"
            ],
            "message": "I can help you manage CRM data across multiple platforms. Try any of the example queries above!"
        }

    def _handle_clear_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle clear/reset queries."""
        platform, _ = self._extract_platforms(query)

        if platform:
            result = self.mesh.clear_platform(platform)
            return {
                "intent": "clear",
                "action": "cleared",
                "platform": platform.value,
                "message": f"Cleared all data for {platform.value}"
            }

        return {
            "intent": "clear",
            "action": "clarification_needed",
            "message": "Which platform would you like to clear? (Salesforce, Dynamics 365, or Local)"
        }

    def _handle_export_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle export queries."""
        platform, _ = self._extract_platforms(query)

        if platform:
            data = self.mesh.export_to_platform(platform)
            record_count = sum(len(v) for v in data.values())
            return {
                "intent": "export",
                "action": "exported",
                "platform": platform.value,
                "data": data,
                "record_count": record_count,
                "message": f"Exported {record_count} records in {platform.value} format"
            }

        return {
            "intent": "export",
            "action": "clarification_needed",
            "message": "Which platform format would you like to export? (Salesforce, Dynamics 365, or Local)"
        }

    def _handle_general_intent(self, query: str, context: Optional[Dict]) -> Dict:
        """Handle general/unrecognized queries."""
        return {
            "intent": "general",
            "action": "response",
            "message": "I can help with syncing, migrating, and managing your CRM data. Try asking about syncing platforms, finding duplicates, checking system status, or viewing schema mappings."
        }

    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.conversation_history

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
