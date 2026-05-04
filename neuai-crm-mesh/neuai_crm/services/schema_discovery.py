"""
Schema Discovery - Automatic Schema Extraction and Mapping Proposal Engine

This module automatically:
1. Pulls metadata from live Salesforce and Dynamics 365 instances
2. Analyzes field types, names, and relationships
3. Proposes intelligent mappings between platforms
4. Queues proposals for human audit (not teaching - auditing!)

The human's job is to AUDIT and APPROVE, not to teach.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
import re

from neuai_crm.models.schemas import Platform


class FieldType(str, Enum):
    """Normalized field types across platforms."""
    STRING = "string"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    INTEGER = "integer"
    DECIMAL = "decimal"
    CURRENCY = "currency"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    PICKLIST = "picklist"
    MULTIPICKLIST = "multipicklist"
    REFERENCE = "reference"  # Foreign key / lookup
    TEXTAREA = "textarea"
    ID = "id"
    UNKNOWN = "unknown"


class AuditStatus(str, Enum):
    """Status of a proposed mapping in the audit queue."""
    PENDING = "pending"           # Waiting for human review
    APPROVED = "approved"         # Human approved
    REJECTED = "rejected"         # Human rejected
    MODIFIED = "modified"         # Human modified and approved
    AUTO_APPROVED = "auto"        # Auto-approved (high confidence + same type)


@dataclass
class FieldMetadata:
    """Metadata for a single field from a CRM."""
    name: str
    label: str
    field_type: FieldType
    platform: str
    entity: str
    required: bool = False
    unique: bool = False
    max_length: Optional[int] = None
    picklist_values: List[str] = field(default_factory=list)
    reference_to: Optional[str] = None  # For lookup fields
    description: Optional[str] = None
    default_value: Optional[Any] = None
    is_custom: bool = False
    is_system: bool = False
    api_name: str = ""  # Original API name

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'FieldMetadata':
        data['field_type'] = FieldType(data['field_type'])
        return cls(**data)


@dataclass
class MappingProposal:
    """A proposed field mapping for human audit."""
    id: str
    source_platform: str
    source_entity: str
    source_field: FieldMetadata
    target_platform: str
    target_entity: str
    target_field: Optional[FieldMetadata]
    confidence: float
    status: AuditStatus = AuditStatus.PENDING
    reasoning: List[str] = field(default_factory=list)
    alternatives: List[Tuple[str, float]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    human_notes: Optional[str] = None
    # For value mappings (picklists)
    value_mappings: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['source_field'] = self.source_field.to_dict()
        if self.target_field:
            d['target_field'] = self.target_field.to_dict()
        d['status'] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> 'MappingProposal':
        data['source_field'] = FieldMetadata.from_dict(data['source_field'])
        if data.get('target_field'):
            data['target_field'] = FieldMetadata.from_dict(data['target_field'])
        data['status'] = AuditStatus(data['status'])
        return cls(**data)


@dataclass
class DiscoveryResult:
    """Result of a schema discovery operation."""
    platform: str
    entities_discovered: int
    fields_discovered: int
    custom_fields: int
    timestamp: str
    duration_seconds: float
    errors: List[str] = field(default_factory=list)


class SchemaDiscovery:
    """
    Automatic schema discovery and mapping proposal engine.

    Pulls metadata from live CRMs and proposes mappings for human audit.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or self._default_storage_path()

        # Discovered schemas
        self.schemas: Dict[str, Dict[str, List[FieldMetadata]]] = {
            "salesforce": {},
            "dynamics365": {},
            "local": {}
        }

        # Audit queue
        self.audit_queue: List[MappingProposal] = []

        # Approved mappings (after audit)
        self.approved_mappings: Dict[str, MappingProposal] = {}

        # Discovery history
        self.discovery_history: List[DiscoveryResult] = []

        # Load existing data
        self._load_state()

    def _default_storage_path(self) -> str:
        base = Path(__file__).parent.parent.parent / "data" / "schema_discovery"
        base.mkdir(parents=True, exist_ok=True)
        return str(base)

    # =========================================================================
    # SALESFORCE METADATA EXTRACTION
    # =========================================================================

    def discover_salesforce(self, sf_client) -> DiscoveryResult:
        """
        Discover schema from Salesforce using the Describe API.

        Args:
            sf_client: simple_salesforce.Salesforce instance

        Returns:
            DiscoveryResult with discovery statistics
        """
        start_time = datetime.now()
        errors = []
        total_fields = 0
        custom_fields = 0

        # Standard objects we care about for CRM
        target_objects = [
            'Account', 'Contact', 'Opportunity', 'Task', 'Lead',
            'Campaign', 'Case', 'Event', 'Note'
        ]

        discovered_entities = {}

        for obj_name in target_objects:
            try:
                # Get object description
                describe = getattr(sf_client, obj_name).describe()

                fields = []
                for f in describe['fields']:
                    field_meta = self._parse_salesforce_field(f, obj_name)
                    fields.append(field_meta)
                    total_fields += 1
                    if field_meta.is_custom:
                        custom_fields += 1

                discovered_entities[obj_name.lower()] = fields

            except Exception as e:
                errors.append(f"Error describing {obj_name}: {str(e)}")

        # Also discover custom objects
        try:
            global_describe = sf_client.describe()
            for obj in global_describe['sobjects']:
                if obj['custom'] and obj['queryable']:
                    try:
                        describe = sf_client.query(f"SELECT Id FROM {obj['name']} LIMIT 0")
                        obj_describe = getattr(sf_client, obj['name']).describe()

                        fields = []
                        for f in obj_describe['fields']:
                            field_meta = self._parse_salesforce_field(f, obj['name'])
                            fields.append(field_meta)
                            total_fields += 1
                            custom_fields += 1

                        discovered_entities[obj['name'].lower()] = fields
                    except:
                        pass  # Skip objects we can't access
        except Exception as e:
            errors.append(f"Error discovering custom objects: {str(e)}")

        self.schemas["salesforce"] = discovered_entities

        duration = (datetime.now() - start_time).total_seconds()
        result = DiscoveryResult(
            platform="salesforce",
            entities_discovered=len(discovered_entities),
            fields_discovered=total_fields,
            custom_fields=custom_fields,
            timestamp=datetime.now().isoformat(),
            duration_seconds=duration,
            errors=errors
        )

        self.discovery_history.append(result)
        self._save_state()

        return result

    def _parse_salesforce_field(self, field_data: Dict, entity: str) -> FieldMetadata:
        """Parse Salesforce field description into normalized FieldMetadata."""
        sf_type = field_data.get('type', '').lower()

        # Map Salesforce types to normalized types
        type_map = {
            'id': FieldType.ID,
            'string': FieldType.STRING,
            'email': FieldType.EMAIL,
            'phone': FieldType.PHONE,
            'url': FieldType.URL,
            'int': FieldType.INTEGER,
            'integer': FieldType.INTEGER,
            'double': FieldType.DECIMAL,
            'currency': FieldType.CURRENCY,
            'percent': FieldType.DECIMAL,
            'boolean': FieldType.BOOLEAN,
            'date': FieldType.DATE,
            'datetime': FieldType.DATETIME,
            'picklist': FieldType.PICKLIST,
            'multipicklist': FieldType.MULTIPICKLIST,
            'reference': FieldType.REFERENCE,
            'textarea': FieldType.TEXTAREA,
            'address': FieldType.STRING,
            'combobox': FieldType.PICKLIST,
        }

        field_type = type_map.get(sf_type, FieldType.UNKNOWN)

        # Extract picklist values
        picklist_values = []
        if field_data.get('picklistValues'):
            picklist_values = [
                pv['value'] for pv in field_data['picklistValues']
                if pv.get('active', True)
            ]

        # Extract reference target
        reference_to = None
        if field_data.get('referenceTo'):
            reference_to = field_data['referenceTo'][0] if field_data['referenceTo'] else None

        return FieldMetadata(
            name=field_data['name'],
            label=field_data.get('label', field_data['name']),
            field_type=field_type,
            platform="salesforce",
            entity=entity,
            required=not field_data.get('nillable', True) and not field_data.get('defaultedOnCreate', False),
            unique=field_data.get('unique', False),
            max_length=field_data.get('length'),
            picklist_values=picklist_values,
            reference_to=reference_to,
            description=field_data.get('inlineHelpText'),
            default_value=field_data.get('defaultValue'),
            is_custom=field_data['name'].endswith('__c'),
            is_system=field_data.get('calculated', False) or not field_data.get('updateable', True),
            api_name=field_data['name']
        )

    # =========================================================================
    # DYNAMICS 365 METADATA EXTRACTION
    # =========================================================================

    def discover_dynamics365(self, access_token: str, environment_url: str) -> DiscoveryResult:
        """
        Discover schema from Dynamics 365 using EntityDefinitions API.

        Args:
            access_token: OAuth access token
            environment_url: Dynamics 365 environment URL

        Returns:
            DiscoveryResult with discovery statistics
        """
        import requests

        start_time = datetime.now()
        errors = []
        total_fields = 0
        custom_fields = 0

        headers = {
            'Authorization': f'Bearer {access_token}',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Prefer': 'odata.include-annotations=*'
        }

        base_url = environment_url.rstrip('/')
        api_url = f"{base_url}/api/data/v9.2"

        # Target entities for CRM
        target_entities = [
            'account', 'contact', 'opportunity', 'task', 'lead',
            'campaign', 'incident', 'appointment', 'annotation',
            'activitypointer', 'phonecall', 'email'
        ]

        discovered_entities = {}

        for entity_name in target_entities:
            try:
                # Get entity metadata
                url = f"{api_url}/EntityDefinitions(LogicalName='{entity_name}')?$expand=Attributes"
                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    errors.append(f"Error fetching {entity_name}: {response.status_code}")
                    continue

                entity_data = response.json()

                fields = []
                for attr in entity_data.get('Attributes', []):
                    field_meta = self._parse_dynamics_field(attr, entity_name)
                    if field_meta:  # Skip null returns
                        fields.append(field_meta)
                        total_fields += 1
                        if field_meta.is_custom:
                            custom_fields += 1

                discovered_entities[entity_name] = fields

            except Exception as e:
                errors.append(f"Error discovering {entity_name}: {str(e)}")

        self.schemas["dynamics365"] = discovered_entities

        duration = (datetime.now() - start_time).total_seconds()
        result = DiscoveryResult(
            platform="dynamics365",
            entities_discovered=len(discovered_entities),
            fields_discovered=total_fields,
            custom_fields=custom_fields,
            timestamp=datetime.now().isoformat(),
            duration_seconds=duration,
            errors=errors
        )

        self.discovery_history.append(result)
        self._save_state()

        return result

    def _parse_dynamics_field(self, attr_data: Dict, entity: str) -> Optional[FieldMetadata]:
        """Parse Dynamics 365 attribute metadata into normalized FieldMetadata."""
        attr_type = attr_data.get('AttributeType', '').lower()

        # Skip certain attribute types
        skip_types = ['virtual', 'entityname', 'uniqueidentifier']
        if attr_type in skip_types and attr_data.get('LogicalName') != f"{entity}id":
            return None

        # Map Dynamics types to normalized types
        type_map = {
            'string': FieldType.STRING,
            'memo': FieldType.TEXTAREA,
            'integer': FieldType.INTEGER,
            'bigint': FieldType.INTEGER,
            'decimal': FieldType.DECIMAL,
            'double': FieldType.DECIMAL,
            'money': FieldType.CURRENCY,
            'boolean': FieldType.BOOLEAN,
            'datetime': FieldType.DATETIME,
            'picklist': FieldType.PICKLIST,
            'state': FieldType.PICKLIST,
            'status': FieldType.PICKLIST,
            'multiselectpicklist': FieldType.MULTIPICKLIST,
            'lookup': FieldType.REFERENCE,
            'customer': FieldType.REFERENCE,
            'owner': FieldType.REFERENCE,
            'uniqueidentifier': FieldType.ID,
        }

        field_type = type_map.get(attr_type, FieldType.UNKNOWN)

        # Detect email/phone/url from name patterns
        logical_name = attr_data.get('LogicalName', '').lower()
        if 'email' in logical_name:
            field_type = FieldType.EMAIL
        elif 'phone' in logical_name or 'telephone' in logical_name:
            field_type = FieldType.PHONE
        elif 'url' in logical_name or 'website' in logical_name:
            field_type = FieldType.URL

        # Get display name
        display_name = attr_data.get('LogicalName', '')
        if attr_data.get('DisplayName'):
            localized = attr_data['DisplayName'].get('UserLocalizedLabel')
            if localized:
                display_name = localized.get('Label', display_name)

        # Check if custom field
        is_custom = logical_name.startswith('new_') or '_' in logical_name.split('_')[0] if '_' in logical_name else False

        return FieldMetadata(
            name=attr_data.get('LogicalName', ''),
            label=display_name,
            field_type=field_type,
            platform="dynamics365",
            entity=entity,
            required=attr_data.get('RequiredLevel', {}).get('Value') == 'ApplicationRequired',
            max_length=attr_data.get('MaxLength'),
            description=attr_data.get('Description', {}).get('UserLocalizedLabel', {}).get('Label'),
            is_custom=is_custom,
            is_system=not attr_data.get('IsValidForUpdate', True),
            api_name=attr_data.get('LogicalName', '')
        )

    # =========================================================================
    # AUTO-MAPPING PROPOSAL ENGINE
    # =========================================================================

    def generate_mapping_proposals(
        self,
        source_platform: str,
        target_platform: str,
        auto_approve_threshold: float = 0.95
    ) -> List[MappingProposal]:
        """
        Automatically generate mapping proposals between two platforms.

        This is where the AI does the work. Humans audit the results.

        Args:
            source_platform: Source platform name
            target_platform: Target platform name
            auto_approve_threshold: Confidence above which to auto-approve

        Returns:
            List of MappingProposals for human audit
        """
        proposals = []

        source_schemas = self.schemas.get(source_platform, {})
        target_schemas = self.schemas.get(target_platform, {})

        # Entity mapping (Account -> account, Contact -> contact, etc.)
        entity_pairs = self._match_entities(source_schemas.keys(), target_schemas.keys())

        for source_entity, target_entity, entity_confidence in entity_pairs:
            source_fields = source_schemas.get(source_entity, [])
            target_fields = target_schemas.get(target_entity, [])

            # Create field lookup for target
            target_lookup = {f.name.lower(): f for f in target_fields}
            target_by_label = {f.label.lower(): f for f in target_fields}
            target_by_type = defaultdict(list)
            for f in target_fields:
                target_by_type[f.field_type].append(f)

            for source_field in source_fields:
                # Skip system fields
                if source_field.is_system and source_field.field_type != FieldType.ID:
                    continue

                # Find best match
                best_match, confidence, reasoning, alternatives = self._find_best_field_match(
                    source_field, target_fields, target_lookup, target_by_label, target_by_type
                )

                # Generate proposal ID
                proposal_id = hashlib.md5(
                    f"{source_platform}:{source_entity}:{source_field.name}:{target_platform}:{target_entity}".encode()
                ).hexdigest()[:12]

                # Determine initial status
                status = AuditStatus.PENDING
                if confidence >= auto_approve_threshold and best_match:
                    # Auto-approve high confidence + same type
                    if best_match.field_type == source_field.field_type:
                        status = AuditStatus.AUTO_APPROVED

                proposal = MappingProposal(
                    id=proposal_id,
                    source_platform=source_platform,
                    source_entity=source_entity,
                    source_field=source_field,
                    target_platform=target_platform,
                    target_entity=target_entity,
                    target_field=best_match,
                    confidence=confidence,
                    status=status,
                    reasoning=reasoning,
                    alternatives=alternatives
                )

                # Generate value mappings for picklists
                if source_field.field_type == FieldType.PICKLIST and best_match:
                    proposal.value_mappings = self._generate_value_mappings(
                        source_field.picklist_values,
                        best_match.picklist_values if best_match else []
                    )

                proposals.append(proposal)

        # Add to audit queue
        self.audit_queue.extend([p for p in proposals if p.status == AuditStatus.PENDING])

        # Auto-approved go straight to approved
        for p in proposals:
            if p.status == AuditStatus.AUTO_APPROVED:
                self.approved_mappings[p.id] = p

        self._save_state()

        return proposals

    def _match_entities(
        self,
        source_entities: List[str],
        target_entities: List[str]
    ) -> List[Tuple[str, str, float]]:
        """Match entities between platforms."""
        # Known entity mappings
        known_mappings = {
            'account': ['account', 'companies', 'company'],
            'contact': ['contact', 'contacts'],
            'opportunity': ['opportunity', 'opportunities', 'deal', 'deals'],
            'task': ['task', 'tasks', 'activity', 'activities', 'activitypointer'],
            'lead': ['lead', 'leads'],
            'campaign': ['campaign', 'campaigns'],
            'case': ['incident', 'cases', 'case'],
            'event': ['appointment', 'events', 'event'],
        }

        matches = []

        for source in source_entities:
            source_lower = source.lower()
            best_target = None
            best_confidence = 0.0

            # Check known mappings first
            for canonical, variants in known_mappings.items():
                if source_lower in variants or source_lower == canonical:
                    for target in target_entities:
                        if target.lower() in variants or target.lower() == canonical:
                            best_target = target
                            best_confidence = 1.0
                            break
                    if best_target:
                        break

            # Fall back to string similarity
            if not best_target:
                for target in target_entities:
                    sim = SequenceMatcher(None, source_lower, target.lower()).ratio()
                    if sim > best_confidence:
                        best_confidence = sim
                        best_target = target

            if best_target and best_confidence >= 0.5:
                matches.append((source, best_target, best_confidence))

        return matches

    def _find_best_field_match(
        self,
        source_field: FieldMetadata,
        target_fields: List[FieldMetadata],
        target_lookup: Dict[str, FieldMetadata],
        target_by_label: Dict[str, FieldMetadata],
        target_by_type: Dict[FieldType, List[FieldMetadata]]
    ) -> Tuple[Optional[FieldMetadata], float, List[str], List[Tuple[str, float]]]:
        """
        Find the best matching target field for a source field.

        Returns:
            (best_match, confidence, reasoning, alternatives)
        """
        candidates: Dict[str, List[Tuple[float, str]]] = defaultdict(list)

        source_name = source_field.name.lower()
        source_label = source_field.label.lower()

        # Strategy 1: Exact name match
        if source_name in target_lookup:
            candidates[target_lookup[source_name].name].append((0.98, "Exact API name match"))

        # Strategy 2: Exact label match
        if source_label in target_by_label:
            candidates[target_by_label[source_label].name].append((0.95, "Exact label match"))

        # Strategy 3: Standard field name mappings
        standard_mappings = {
            # Salesforce -> Dynamics common mappings
            'id': ['id', 'accountid', 'contactid', 'opportunityid'],
            'name': ['name', 'fullname', 'subject'],
            'firstname': ['firstname'],
            'lastname': ['lastname'],
            'email': ['emailaddress1', 'emailaddress2', 'emailaddress3'],
            'phone': ['telephone1', 'telephone2', 'telephone3', 'mobilephone'],
            'website': ['websiteurl'],
            'industry': ['industrycode'],
            'description': ['description'],
            'billingstreet': ['address1_line1'],
            'billingcity': ['address1_city'],
            'billingstate': ['address1_stateorprovince'],
            'billingpostalcode': ['address1_postalcode'],
            'billingcountry': ['address1_country'],
            'amount': ['estimatedvalue', 'actualvalue'],
            'stagename': ['stepname', 'salesstagecode'],
            'closedate': ['estimatedclosedate', 'actualclosedate'],
            'probability': ['closeprobability'],
            'accountid': ['parentaccountid', 'customerid'],
            'ownerid': ['ownerid', 'owninguser'],
            'createddate': ['createdon'],
            'lastmodifieddate': ['modifiedon'],
            'title': ['jobtitle'],
        }

        # Check standard mappings
        clean_source = re.sub(r'__c$', '', source_name)  # Remove Salesforce custom suffix
        if clean_source in standard_mappings:
            for target_name in standard_mappings[clean_source]:
                if target_name in target_lookup:
                    candidates[target_lookup[target_name].name].append(
                        (0.92, f"Standard field mapping: {clean_source} -> {target_name}")
                    )

        # Strategy 4: Type + semantic name matching
        same_type_fields = target_by_type.get(source_field.field_type, [])
        for tf in same_type_fields:
            # Name similarity
            name_sim = SequenceMatcher(None, source_name, tf.name.lower()).ratio()
            label_sim = SequenceMatcher(None, source_label, tf.label.lower()).ratio()
            best_sim = max(name_sim, label_sim)

            if best_sim >= 0.6:
                candidates[tf.name].append(
                    (best_sim * 0.85, f"Name similarity ({best_sim:.0%}) + same type ({source_field.field_type.value})")
                )

        # Strategy 5: Semantic matching
        semantic_groups = [
            (['email', 'mail', 'e-mail'], ['emailaddress', 'email']),
            (['phone', 'tel', 'mobile', 'fax'], ['telephone', 'phone', 'mobile']),
            (['address', 'street', 'city', 'state', 'zip', 'postal', 'country'], ['address']),
            (['company', 'account', 'organization', 'org'], ['account', 'company', 'parent']),
            (['amount', 'value', 'price', 'revenue', 'budget'], ['value', 'amount', 'budget']),
            (['date', 'time', 'created', 'modified', 'updated'], ['date', 'on', 'time']),
            (['owner', 'assigned', 'rep', 'user'], ['owner', 'user', 'assigned']),
            (['stage', 'status', 'state', 'phase'], ['stage', 'status', 'state', 'step']),
            (['probability', 'likelihood', 'chance', 'percent'], ['probability', 'percent', 'chance']),
            (['description', 'notes', 'comment', 'details'], ['description', 'notes', 'memo']),
        ]

        for source_patterns, target_patterns in semantic_groups:
            if any(p in source_name or p in source_label for p in source_patterns):
                for tf in target_fields:
                    tf_name = tf.name.lower()
                    tf_label = tf.label.lower()
                    if any(p in tf_name or p in tf_label for p in target_patterns):
                        candidates[tf.name].append((0.75, "Semantic group match"))

        # Strategy 6: Reference field matching
        if source_field.field_type == FieldType.REFERENCE and source_field.reference_to:
            ref_lower = source_field.reference_to.lower()
            for tf in target_by_type.get(FieldType.REFERENCE, []):
                if ref_lower in tf.name.lower() or (tf.reference_to and ref_lower in tf.reference_to.lower()):
                    candidates[tf.name].append((0.8, f"Reference to same entity type"))

        # Aggregate scores
        if not candidates:
            return (None, 0.0, ["No matching field found"], [])

        scored = []
        for field_name, scores_reasons in candidates.items():
            total_score = sum(s for s, _ in scores_reasons) / len(scores_reasons)
            # Boost for multiple matching strategies
            if len(scores_reasons) > 1:
                total_score = min(total_score * (1 + 0.05 * len(scores_reasons)), 0.99)

            reasons = list(set(r for _, r in scores_reasons))
            scored.append((field_name, total_score, reasons))

        scored.sort(key=lambda x: x[1], reverse=True)

        best_name, best_score, reasons = scored[0]
        best_field = target_lookup.get(best_name)

        alternatives = [(name, score) for name, score, _ in scored[1:4]]

        return (best_field, best_score, reasons, alternatives)

    def _generate_value_mappings(
        self,
        source_values: List[str],
        target_values: List[str]
    ) -> Dict[str, str]:
        """Generate value mappings for picklist fields."""
        mappings = {}

        target_lower = {v.lower(): v for v in target_values}

        for sv in source_values:
            sv_lower = sv.lower()

            # Exact match
            if sv_lower in target_lower:
                mappings[sv] = target_lower[sv_lower]
                continue

            # Best similarity match
            best_match = None
            best_sim = 0.0
            for tv in target_values:
                sim = SequenceMatcher(None, sv_lower, tv.lower()).ratio()
                if sim > best_sim:
                    best_sim = sim
                    best_match = tv

            if best_sim >= 0.6:
                mappings[sv] = best_match

        return mappings

    # =========================================================================
    # AUDIT WORKFLOW
    # =========================================================================

    def get_audit_queue(self, status: Optional[AuditStatus] = None) -> List[MappingProposal]:
        """Get proposals pending human audit."""
        if status:
            return [p for p in self.audit_queue if p.status == status]
        return self.audit_queue

    def get_audit_summary(self) -> Dict:
        """Get summary of audit queue status."""
        total = len(self.audit_queue)
        by_status = defaultdict(int)
        by_confidence = {"high": 0, "medium": 0, "low": 0}

        for p in self.audit_queue:
            by_status[p.status.value] += 1
            if p.confidence >= 0.8:
                by_confidence["high"] += 1
            elif p.confidence >= 0.6:
                by_confidence["medium"] += 1
            else:
                by_confidence["low"] += 1

        return {
            "total_pending": total,
            "by_status": dict(by_status),
            "by_confidence": by_confidence,
            "auto_approved": len([m for m in self.approved_mappings.values()
                                  if m.status == AuditStatus.AUTO_APPROVED]),
            "human_approved": len([m for m in self.approved_mappings.values()
                                   if m.status in [AuditStatus.APPROVED, AuditStatus.MODIFIED]])
        }

    def approve_proposal(
        self,
        proposal_id: str,
        reviewer: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[MappingProposal]:
        """Approve a mapping proposal."""
        for i, p in enumerate(self.audit_queue):
            if p.id == proposal_id:
                p.status = AuditStatus.APPROVED
                p.reviewed_at = datetime.now().isoformat()
                p.reviewed_by = reviewer
                p.human_notes = notes

                # Move to approved
                self.approved_mappings[p.id] = p
                self.audit_queue.pop(i)
                self._save_state()
                return p
        return None

    def reject_proposal(
        self,
        proposal_id: str,
        reviewer: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[MappingProposal]:
        """Reject a mapping proposal."""
        for i, p in enumerate(self.audit_queue):
            if p.id == proposal_id:
                p.status = AuditStatus.REJECTED
                p.reviewed_at = datetime.now().isoformat()
                p.reviewed_by = reviewer
                p.human_notes = notes

                self.audit_queue.pop(i)
                self._save_state()
                return p
        return None

    def modify_proposal(
        self,
        proposal_id: str,
        new_target_field: str,
        reviewer: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[MappingProposal]:
        """Modify and approve a mapping proposal with a different target field."""
        for i, p in enumerate(self.audit_queue):
            if p.id == proposal_id:
                # Find the new target field metadata
                target_fields = self.schemas.get(p.target_platform, {}).get(p.target_entity, [])
                new_field = next((f for f in target_fields if f.name == new_target_field), None)

                if not new_field:
                    # Create minimal metadata for custom mapping
                    new_field = FieldMetadata(
                        name=new_target_field,
                        label=new_target_field,
                        field_type=p.source_field.field_type,
                        platform=p.target_platform,
                        entity=p.target_entity,
                        api_name=new_target_field
                    )

                p.target_field = new_field
                p.status = AuditStatus.MODIFIED
                p.confidence = 1.0  # Human-verified
                p.reviewed_at = datetime.now().isoformat()
                p.reviewed_by = reviewer
                p.human_notes = notes
                p.reasoning.append(f"Human corrected: {p.source_field.name} -> {new_target_field}")

                # Move to approved
                self.approved_mappings[p.id] = p
                self.audit_queue.pop(i)
                self._save_state()
                return p
        return None

    def bulk_approve(
        self,
        min_confidence: float = 0.9,
        reviewer: Optional[str] = None
    ) -> int:
        """Bulk approve all proposals above a confidence threshold."""
        approved_count = 0
        to_approve = [p for p in self.audit_queue if p.confidence >= min_confidence]

        for p in to_approve:
            self.approve_proposal(p.id, reviewer, f"Bulk approved (confidence >= {min_confidence})")
            approved_count += 1

        return approved_count

    # =========================================================================
    # PERSISTENCE
    # =========================================================================

    def _save_state(self):
        """Save discovery state to disk."""
        state_file = Path(self.storage_path) / "discovery_state.json"

        data = {
            "version": "1.0",
            "saved_at": datetime.now().isoformat(),
            "schemas": {
                platform: {
                    entity: [f.to_dict() for f in fields]
                    for entity, fields in entities.items()
                }
                for platform, entities in self.schemas.items()
            },
            "audit_queue": [p.to_dict() for p in self.audit_queue],
            "approved_mappings": {k: v.to_dict() for k, v in self.approved_mappings.items()},
            "discovery_history": [asdict(r) for r in self.discovery_history]
        }

        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_state(self):
        """Load discovery state from disk."""
        state_file = Path(self.storage_path) / "discovery_state.json"

        if not state_file.exists():
            return

        try:
            with open(state_file, 'r') as f:
                data = json.load(f)

            # Load schemas
            for platform, entities in data.get("schemas", {}).items():
                self.schemas[platform] = {
                    entity: [FieldMetadata.from_dict(f) for f in fields]
                    for entity, fields in entities.items()
                }

            # Load audit queue
            self.audit_queue = [
                MappingProposal.from_dict(p) for p in data.get("audit_queue", [])
            ]

            # Load approved mappings
            self.approved_mappings = {
                k: MappingProposal.from_dict(v)
                for k, v in data.get("approved_mappings", {}).items()
            }

            # Load history
            self.discovery_history = [
                DiscoveryResult(**r) for r in data.get("discovery_history", [])
            ]

        except Exception as e:
            print(f"Warning: Could not load discovery state: {e}")

    def export_approved_mappings(self) -> Dict:
        """Export approved mappings in a format usable by the Schema Brain."""
        export = {
            "generated_at": datetime.now().isoformat(),
            "total_mappings": len(self.approved_mappings),
            "mappings": []
        }

        for p in self.approved_mappings.values():
            if p.target_field:
                export["mappings"].append({
                    "source_platform": p.source_platform,
                    "source_entity": p.source_entity,
                    "source_field": p.source_field.name,
                    "target_platform": p.target_platform,
                    "target_entity": p.target_entity,
                    "target_field": p.target_field.name,
                    "confidence": p.confidence,
                    "status": p.status.value,
                    "value_mappings": p.value_mappings
                })

        return export


# Global instance
schema_discovery = SchemaDiscovery()
