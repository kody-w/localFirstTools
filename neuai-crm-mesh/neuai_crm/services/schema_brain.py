"""
Schema Brain - Self-Improving Schema Translation Engine

The Schema Brain learns from every sync operation:
1. Detects unknown fields not in the base schema
2. Proposes intelligent mappings using multiple inference strategies
3. Collects human feedback on proposals
4. Learns from corrections to improve future predictions
5. Tracks confidence scores and mapping provenance

Over time, it evolves from handling ~60% of edge cases to 95%+.
"""

import json
import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS


class MappingSource(str, Enum):
    """How a mapping was learned."""
    BUILTIN = "builtin"           # Part of original schema
    INFERRED = "inferred"         # AI/algorithm proposed
    HUMAN_CORRECTED = "human"     # Human provided/corrected
    PATTERN_LEARNED = "pattern"   # Learned from similar mappings
    HYBRID = "hybrid"             # Multiple sources combined


class ConfidenceLevel(str, Enum):
    """Confidence in a mapping."""
    CERTAIN = "certain"           # 95%+ confidence (human verified or builtin)
    HIGH = "high"                 # 80-95% confidence
    MEDIUM = "medium"             # 60-80% confidence
    LOW = "low"                   # 40-60% confidence
    UNCERTAIN = "uncertain"       # <40% confidence, needs human review


@dataclass
class FieldMapping:
    """A learned field mapping between platforms."""
    source_platform: str
    source_field: str
    target_platform: str
    target_field: str
    entity_type: str
    confidence: float  # 0.0 to 1.0
    source: MappingSource
    times_used: int = 0
    times_corrected: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_used: Optional[str] = None
    notes: Optional[str] = None
    # For tracking inference reasoning
    inference_reasons: List[str] = field(default_factory=list)

    @property
    def confidence_level(self) -> ConfidenceLevel:
        if self.confidence >= 0.95:
            return ConfidenceLevel.CERTAIN
        elif self.confidence >= 0.80:
            return ConfidenceLevel.HIGH
        elif self.confidence >= 0.60:
            return ConfidenceLevel.MEDIUM
        elif self.confidence >= 0.40:
            return ConfidenceLevel.LOW
        return ConfidenceLevel.UNCERTAIN

    @property
    def reliability_score(self) -> float:
        """Calculate reliability based on usage and corrections."""
        if self.times_used == 0:
            return self.confidence
        correction_rate = self.times_corrected / self.times_used
        return self.confidence * (1 - correction_rate * 0.5)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'FieldMapping':
        # Handle backwards compatibility
        if 'inference_reasons' not in data:
            data['inference_reasons'] = []
        return cls(**data)


@dataclass
class ValueMapping:
    """A learned value translation (e.g., stage names)."""
    source_platform: str
    source_value: Any
    target_platform: str
    target_value: Any
    field_name: str
    entity_type: str
    confidence: float
    source: MappingSource
    times_used: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ValueMapping':
        return cls(**data)


@dataclass
class InferenceResult:
    """Result of attempting to infer a field mapping."""
    proposed_mapping: Optional[str]
    confidence: float
    reasons: List[str]
    alternatives: List[Tuple[str, float]]  # (field_name, confidence)
    needs_human_review: bool


@dataclass
class LearningEvent:
    """Record of a learning event for audit trail."""
    timestamp: str
    event_type: str  # "new_mapping", "correction", "confirmation", "rejection"
    source_platform: str
    target_platform: str
    entity_type: str
    field_name: str
    old_value: Optional[str]
    new_value: str
    confidence_change: float
    user_id: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class SchemaBrain:
    """
    The self-improving schema translation brain.

    Learns from every translation operation to get smarter over time.
    """

    def __init__(self, memory_path: Optional[str] = None):
        """Initialize the Schema Brain."""
        self.memory_path = memory_path or self._default_memory_path()

        # In-memory stores
        self.field_mappings: Dict[str, FieldMapping] = {}
        self.value_mappings: Dict[str, ValueMapping] = {}
        self.learning_log: List[LearningEvent] = []

        # Statistics
        self.stats = {
            "total_translations": 0,
            "unknown_fields_encountered": 0,
            "successful_inferences": 0,
            "human_corrections": 0,
            "auto_resolved": 0
        }

        # Pattern memory for learning
        self.field_patterns: Dict[str, List[str]] = defaultdict(list)
        self.value_patterns: Dict[str, Dict[str, str]] = defaultdict(dict)

        # Load existing memory
        self._load_memory()

        # Bootstrap with builtin mappings
        self._bootstrap_from_builtins()

    def _default_memory_path(self) -> str:
        """Get default path for schema memory storage."""
        base = Path(__file__).parent.parent.parent / "data" / "schema_memory"
        base.mkdir(parents=True, exist_ok=True)
        return str(base)

    def _mapping_key(self, source_platform: str, source_field: str,
                     target_platform: str, entity_type: str) -> str:
        """Generate unique key for a field mapping."""
        return f"{source_platform}:{source_field}:{target_platform}:{entity_type}"

    def _value_key(self, source_platform: str, source_value: str,
                   target_platform: str, field_name: str) -> str:
        """Generate unique key for a value mapping."""
        return f"{source_platform}:{source_value}:{target_platform}:{field_name}"

    # =========================================================================
    # CORE TRANSLATION WITH LEARNING
    # =========================================================================

    def translate_field(
        self,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str,
        record: Optional[Dict] = None
    ) -> Tuple[Optional[str], float, bool]:
        """
        Translate a field name, learning if unknown.

        Returns:
            Tuple of (translated_field, confidence, needs_review)
        """
        self.stats["total_translations"] += 1

        key = self._mapping_key(
            source_platform.value, field_name,
            target_platform.value, entity_type
        )

        # Check if we already know this mapping
        if key in self.field_mappings:
            mapping = self.field_mappings[key]
            mapping.times_used += 1
            mapping.last_used = datetime.now().isoformat()
            return (mapping.target_field, mapping.confidence,
                    mapping.confidence_level == ConfidenceLevel.UNCERTAIN)

        # Unknown field - attempt inference
        self.stats["unknown_fields_encountered"] += 1
        inference = self._infer_field_mapping(
            field_name, source_platform, target_platform, entity_type, record
        )

        if inference.proposed_mapping and inference.confidence >= 0.4:
            # Store the inferred mapping
            new_mapping = FieldMapping(
                source_platform=source_platform.value,
                source_field=field_name,
                target_platform=target_platform.value,
                target_field=inference.proposed_mapping,
                entity_type=entity_type,
                confidence=inference.confidence,
                source=MappingSource.INFERRED,
                inference_reasons=inference.reasons
            )
            self.field_mappings[key] = new_mapping
            self.stats["successful_inferences"] += 1

            self._log_learning_event(
                "new_mapping",
                source_platform.value, target_platform.value, entity_type,
                field_name, None, inference.proposed_mapping,
                inference.confidence
            )

            return (inference.proposed_mapping, inference.confidence,
                    inference.needs_human_review)

        # Could not infer - needs human help
        return (None, 0.0, True)

    def translate_value(
        self,
        value: Any,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str
    ) -> Tuple[Any, float]:
        """
        Translate a field value (e.g., stage names, status codes).

        Returns:
            Tuple of (translated_value, confidence)
        """
        key = self._value_key(
            source_platform.value, str(value),
            target_platform.value, field_name
        )

        if key in self.value_mappings:
            mapping = self.value_mappings[key]
            mapping.times_used += 1
            return (mapping.target_value, mapping.confidence)

        # Try to infer value mapping
        inferred_value, confidence = self._infer_value_mapping(
            value, field_name, source_platform, target_platform, entity_type
        )

        if inferred_value is not None and confidence >= 0.5:
            new_mapping = ValueMapping(
                source_platform=source_platform.value,
                source_value=value,
                target_platform=target_platform.value,
                target_value=inferred_value,
                field_name=field_name,
                entity_type=entity_type,
                confidence=confidence,
                source=MappingSource.INFERRED
            )
            self.value_mappings[key] = new_mapping
            return (inferred_value, confidence)

        # Return original value if can't translate
        return (value, 0.0)

    # =========================================================================
    # INFERENCE ENGINE
    # =========================================================================

    def _infer_field_mapping(
        self,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str,
        record: Optional[Dict] = None
    ) -> InferenceResult:
        """
        Use multiple strategies to infer a field mapping.
        """
        candidates: Dict[str, List[Tuple[float, str]]] = defaultdict(list)

        # Strategy 1: Exact name match (case-insensitive)
        target_fields = self._get_known_target_fields(target_platform, entity_type)
        for tf in target_fields:
            if tf.lower() == field_name.lower():
                candidates[tf].append((0.95, "Exact name match (case-insensitive)"))

        # Strategy 2: Common suffix/prefix patterns
        patterns = self._extract_field_patterns(field_name)
        for tf in target_fields:
            tf_patterns = self._extract_field_patterns(tf)
            overlap = patterns & tf_patterns
            if overlap:
                score = 0.7 + (len(overlap) * 0.05)
                candidates[tf].append((min(score, 0.9),
                    f"Shared patterns: {', '.join(overlap)}"))

        # Strategy 3: String similarity (Levenshtein-like)
        for tf in target_fields:
            similarity = SequenceMatcher(None,
                field_name.lower(), tf.lower()).ratio()
            if similarity >= 0.6:
                candidates[tf].append((similarity * 0.85,
                    f"String similarity: {similarity:.0%}"))

        # Strategy 4: Semantic matching via common field name mappings
        semantic_matches = self._semantic_field_match(field_name, target_fields)
        for tf, score in semantic_matches:
            candidates[tf].append((score, "Semantic similarity"))

        # Strategy 5: Learn from existing mappings for similar entities
        pattern_matches = self._pattern_based_match(
            field_name, source_platform, target_platform, entity_type
        )
        for tf, score, reason in pattern_matches:
            candidates[tf].append((score, reason))

        # Strategy 6: Value-based inference (if record provided)
        if record and field_name in record:
            value = record[field_name]
            value_matches = self._value_type_inference(value, target_fields, target_platform)
            for tf, score in value_matches:
                candidates[tf].append((score, f"Value type match for: {type(value).__name__}"))

        # Aggregate scores and pick best candidate
        if not candidates:
            return InferenceResult(
                proposed_mapping=None,
                confidence=0.0,
                reasons=["No viable candidates found"],
                alternatives=[],
                needs_human_review=True
            )

        scored = []
        for field, scores_reasons in candidates.items():
            # Combine multiple signals
            total_score = sum(s for s, _ in scores_reasons) / len(scores_reasons)
            # Boost if multiple strategies agree
            if len(scores_reasons) > 1:
                total_score = min(total_score * 1.1, 0.99)
            scored.append((field, total_score, [r for _, r in scores_reasons]))

        scored.sort(key=lambda x: x[1], reverse=True)
        best_field, best_score, reasons = scored[0]

        return InferenceResult(
            proposed_mapping=best_field,
            confidence=best_score,
            reasons=reasons,
            alternatives=[(f, s) for f, s, _ in scored[1:4]],
            needs_human_review=best_score < 0.8
        )

    def _infer_value_mapping(
        self,
        value: Any,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str
    ) -> Tuple[Optional[Any], float]:
        """Infer a value translation."""
        # Check builtin mappings first (stages, statuses, etc.)
        if field_name.lower() in ['stage', 'stagename', 'stepname', 'status', 'statecode']:
            builtin = self._check_builtin_value_mapping(
                value, field_name, source_platform, target_platform
            )
            if builtin:
                return builtin

        # Try pattern-based inference
        pattern_key = f"{source_platform.value}:{field_name}"
        if pattern_key in self.value_patterns:
            patterns = self.value_patterns[pattern_key]
            str_value = str(value).lower()
            for pattern, target_value in patterns.items():
                if pattern.lower() in str_value or str_value in pattern.lower():
                    return (target_value, 0.7)

        # Try similarity matching against known values
        known_values = self._get_known_values(field_name, target_platform)
        if known_values:
            best_match, best_score = None, 0.0
            for kv in known_values:
                sim = SequenceMatcher(None, str(value).lower(), str(kv).lower()).ratio()
                if sim > best_score:
                    best_match, best_score = kv, sim
            if best_score >= 0.7:
                return (best_match, best_score)

        return (None, 0.0)

    def _extract_field_patterns(self, field_name: str) -> Set[str]:
        """Extract common patterns from a field name."""
        patterns = set()

        # Common prefixes
        prefixes = ['is', 'has', 'can', 'should', 'billing', 'shipping',
                    'primary', 'secondary', 'created', 'modified', 'last', 'first']
        for p in prefixes:
            if field_name.lower().startswith(p):
                patterns.add(f"prefix:{p}")

        # Common suffixes
        suffixes = ['id', 'name', 'date', 'time', 'at', 'on', 'by', 'url',
                    'email', 'phone', 'address', 'code', 'type', 'status']
        for s in suffixes:
            if field_name.lower().endswith(s):
                patterns.add(f"suffix:{s}")

        # Camel case / snake case components
        components = re.split(r'[_\s]|(?=[A-Z])', field_name)
        for c in components:
            if len(c) > 2:
                patterns.add(f"component:{c.lower()}")

        return patterns

    def _semantic_field_match(
        self,
        source_field: str,
        target_fields: List[str]
    ) -> List[Tuple[str, float]]:
        """Match fields based on semantic meaning."""
        # Common semantic equivalences
        semantic_groups = [
            {'id', 'identifier', 'key', 'uid', 'guid'},
            {'name', 'title', 'label', 'subject'},
            {'email', 'emailaddress', 'mail', 'emailaddress1'},
            {'phone', 'telephone', 'mobile', 'cell', 'telephone1'},
            {'company', 'account', 'organization', 'org', 'employer'},
            {'address', 'location', 'street', 'city', 'zip', 'postal'},
            {'created', 'createdon', 'createddate', 'createdat'},
            {'modified', 'updated', 'modifiedon', 'lastmodified', 'updatedat'},
            {'description', 'desc', 'details', 'notes', 'body', 'content'},
            {'status', 'state', 'statecode', 'stage'},
            {'amount', 'value', 'price', 'cost', 'total', 'estimatedvalue'},
            {'probability', 'likelihood', 'chance', 'closeprobability'},
            {'owner', 'assignee', 'assignedto', 'ownerid'},
            {'parent', 'parentid', 'parentcustomerid'},
            {'website', 'url', 'websiteurl', 'homepage'},
            {'industry', 'industrycode', 'sector', 'vertical'},
        ]

        source_lower = source_field.lower()
        # Remove common prefixes/suffixes for matching
        source_clean = re.sub(r'^(billing|shipping|primary|secondary)', '', source_lower)
        source_clean = re.sub(r'(id|date|time|at|on)$', '', source_clean)

        matches = []
        for tf in target_fields:
            tf_lower = tf.lower()
            tf_clean = re.sub(r'^(billing|shipping|primary|secondary)', '', tf_lower)
            tf_clean = re.sub(r'(id|date|time|at|on)$', '', tf_clean)

            for group in semantic_groups:
                source_in = any(g in source_clean for g in group)
                target_in = any(g in tf_clean for g in group)
                if source_in and target_in:
                    # Higher score if both match same semantic group
                    matches.append((tf, 0.8))
                    break

        return matches

    def _pattern_based_match(
        self,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str
    ) -> List[Tuple[str, float, str]]:
        """Learn from existing mappings to propose new ones."""
        matches = []

        # Look for similar field names in other entities that we've already mapped
        field_lower = field_name.lower()

        for key, mapping in self.field_mappings.items():
            if mapping.source_platform != source_platform.value:
                continue
            if mapping.target_platform != target_platform.value:
                continue

            # Check if source field is similar
            sim = SequenceMatcher(None,
                mapping.source_field.lower(), field_lower).ratio()

            if sim >= 0.8 and mapping.confidence >= 0.7:
                # Propose similar target field
                matches.append((
                    mapping.target_field,
                    sim * mapping.confidence * 0.9,
                    f"Similar to known mapping: {mapping.source_field} -> {mapping.target_field}"
                ))

        return matches

    def _value_type_inference(
        self,
        value: Any,
        target_fields: List[str],
        target_platform: Platform
    ) -> List[Tuple[str, float]]:
        """Infer field based on value type and content."""
        matches = []

        # Email pattern
        if isinstance(value, str) and '@' in value and '.' in value:
            for tf in target_fields:
                if 'email' in tf.lower() or 'mail' in tf.lower():
                    matches.append((tf, 0.85))

        # URL pattern
        if isinstance(value, str) and (value.startswith('http') or 'www.' in value):
            for tf in target_fields:
                if 'url' in tf.lower() or 'website' in tf.lower() or 'web' in tf.lower():
                    matches.append((tf, 0.85))

        # Phone pattern
        if isinstance(value, str) and re.match(r'^[\d\s\-\+\(\)]+$', value) and len(value) >= 7:
            for tf in target_fields:
                if 'phone' in tf.lower() or 'tel' in tf.lower() or 'mobile' in tf.lower():
                    matches.append((tf, 0.8))

        # Date pattern
        if isinstance(value, str):
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # ISO
                r'\d{2}/\d{2}/\d{4}',  # US
                r'\d{2}-\d{2}-\d{4}',  # EU
            ]
            for pattern in date_patterns:
                if re.match(pattern, value):
                    for tf in target_fields:
                        if 'date' in tf.lower() or 'time' in tf.lower() or tf.lower().endswith('on') or tf.lower().endswith('at'):
                            matches.append((tf, 0.75))
                    break

        # Numeric (could be amount, probability, etc.)
        if isinstance(value, (int, float)):
            if 0 <= value <= 1:  # Probability
                for tf in target_fields:
                    if 'prob' in tf.lower() or 'percent' in tf.lower() or 'rate' in tf.lower():
                        matches.append((tf, 0.7))
            elif value >= 0:  # Positive number - could be amount
                for tf in target_fields:
                    if 'amount' in tf.lower() or 'value' in tf.lower() or 'price' in tf.lower():
                        matches.append((tf, 0.65))

        return matches

    def _get_known_target_fields(self, platform: Platform, entity_type: str) -> List[str]:
        """Get all known field names for a target platform/entity."""
        fields = set()

        # From builtin schema
        entity_fields = SCHEMA_MAPPINGS["fields"].get(entity_type, {})
        if platform.value in entity_fields:
            fields.update(entity_fields[platform.value])

        # From learned mappings
        for mapping in self.field_mappings.values():
            if mapping.target_platform == platform.value and mapping.entity_type == entity_type:
                fields.add(mapping.target_field)

        return list(fields)

    def _get_known_values(self, field_name: str, platform: Platform) -> List[Any]:
        """Get known values for a field from builtin mappings."""
        known = []

        # Check stages
        if 'stage' in field_name.lower() or 'step' in field_name.lower():
            known.extend(SCHEMA_MAPPINGS.get("stages", {}).get(platform.value, []))

        # Check statuses
        if 'status' in field_name.lower() or 'state' in field_name.lower():
            known.extend(SCHEMA_MAPPINGS.get("status", {}).get(platform.value, []))

        # Check activity types
        if 'type' in field_name.lower() or 'activity' in field_name.lower():
            known.extend(SCHEMA_MAPPINGS.get("activity_types", {}).get(platform.value, []))

        return known

    def _check_builtin_value_mapping(
        self,
        value: Any,
        field_name: str,
        source_platform: Platform,
        target_platform: Platform
    ) -> Optional[Tuple[Any, float]]:
        """Check if value is in builtin mappings."""
        # Determine which mapping to use
        if 'stage' in field_name.lower() or 'step' in field_name.lower():
            mapping_key = 'stages'
        elif 'status' in field_name.lower() or 'state' in field_name.lower():
            mapping_key = 'status'
        elif 'type' in field_name.lower():
            mapping_key = 'activity_types'
        else:
            return None

        source_values = SCHEMA_MAPPINGS.get(mapping_key, {}).get(source_platform.value, [])
        target_values = SCHEMA_MAPPINGS.get(mapping_key, {}).get(target_platform.value, [])

        try:
            idx = source_values.index(value)
            if idx < len(target_values):
                return (target_values[idx], 1.0)
        except (ValueError, IndexError):
            pass

        return None

    # =========================================================================
    # HUMAN FEEDBACK LOOP
    # =========================================================================

    def provide_feedback(
        self,
        source_platform: str,
        source_field: str,
        target_platform: str,
        entity_type: str,
        correct_mapping: str,
        user_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> FieldMapping:
        """
        Accept human correction for a field mapping.

        This is the key learning mechanism - human corrections are weighted heavily.
        """
        key = self._mapping_key(source_platform, source_field, target_platform, entity_type)

        old_mapping = self.field_mappings.get(key)
        old_value = old_mapping.target_field if old_mapping else None

        if old_mapping and old_mapping.target_field != correct_mapping:
            # Correction - decrease confidence in old mapping
            old_mapping.times_corrected += 1
            old_mapping.confidence = max(0.1, old_mapping.confidence * 0.7)

        # Create or update with human-verified mapping
        new_mapping = FieldMapping(
            source_platform=source_platform,
            source_field=source_field,
            target_platform=target_platform,
            target_field=correct_mapping,
            entity_type=entity_type,
            confidence=0.98,  # Human-verified is near-certain
            source=MappingSource.HUMAN_CORRECTED,
            times_used=old_mapping.times_used + 1 if old_mapping else 1,
            times_corrected=0,
            notes=notes
        )

        self.field_mappings[key] = new_mapping
        self.stats["human_corrections"] += 1

        # Log the learning event
        self._log_learning_event(
            "correction" if old_value else "new_mapping",
            source_platform, target_platform, entity_type,
            source_field, old_value, correct_mapping,
            0.98, user_id, notes
        )

        # Learn patterns from this correction
        self._learn_from_correction(source_field, correct_mapping, entity_type)

        # Save memory
        self._save_memory()

        return new_mapping

    def confirm_mapping(
        self,
        source_platform: str,
        source_field: str,
        target_platform: str,
        entity_type: str
    ) -> Optional[FieldMapping]:
        """Confirm an inferred mapping is correct (boosts confidence)."""
        key = self._mapping_key(source_platform, source_field, target_platform, entity_type)

        if key in self.field_mappings:
            mapping = self.field_mappings[key]
            # Boost confidence but not above 0.95 without explicit human verification
            mapping.confidence = min(0.95, mapping.confidence * 1.15)
            mapping.times_used += 1

            self._log_learning_event(
                "confirmation",
                source_platform, target_platform, entity_type,
                source_field, mapping.target_field, mapping.target_field,
                mapping.confidence
            )

            self._save_memory()
            return mapping

        return None

    def reject_mapping(
        self,
        source_platform: str,
        source_field: str,
        target_platform: str,
        entity_type: str,
        reason: Optional[str] = None
    ) -> bool:
        """Reject an inferred mapping (decreases confidence significantly)."""
        key = self._mapping_key(source_platform, source_field, target_platform, entity_type)

        if key in self.field_mappings:
            mapping = self.field_mappings[key]
            old_confidence = mapping.confidence
            mapping.confidence *= 0.5  # Significant decrease
            mapping.times_corrected += 1

            self._log_learning_event(
                "rejection",
                source_platform, target_platform, entity_type,
                source_field, mapping.target_field, "REJECTED",
                mapping.confidence - old_confidence, notes=reason
            )

            if mapping.confidence < 0.2:
                # Remove very low confidence mappings
                del self.field_mappings[key]

            self._save_memory()
            return True

        return False

    def _learn_from_correction(self, source_field: str, target_field: str, entity_type: str):
        """Extract patterns from a correction to apply to future inferences."""
        source_patterns = self._extract_field_patterns(source_field)
        target_patterns = self._extract_field_patterns(target_field)

        # Store pattern associations
        for sp in source_patterns:
            for tp in target_patterns:
                pattern_key = f"{sp}:{entity_type}"
                if pattern_key not in self.field_patterns:
                    self.field_patterns[pattern_key] = []
                if tp not in self.field_patterns[pattern_key]:
                    self.field_patterns[pattern_key].append(tp)

    # =========================================================================
    # UNKNOWN FIELD DETECTION & PROPOSALS
    # =========================================================================

    def analyze_record(
        self,
        record: Dict,
        source_platform: Platform,
        target_platform: Platform,
        entity_type: str
    ) -> Dict[str, InferenceResult]:
        """
        Analyze a record and return mapping proposals for all unknown fields.
        """
        proposals = {}

        for field_name, value in record.items():
            key = self._mapping_key(
                source_platform.value, field_name,
                target_platform.value, entity_type
            )

            if key not in self.field_mappings:
                inference = self._infer_field_mapping(
                    field_name, source_platform, target_platform,
                    entity_type, record
                )
                proposals[field_name] = inference

        return proposals

    def get_pending_reviews(self) -> List[Dict]:
        """Get all mappings that need human review."""
        pending = []

        for key, mapping in self.field_mappings.items():
            if mapping.confidence_level in [ConfidenceLevel.LOW, ConfidenceLevel.UNCERTAIN]:
                pending.append({
                    "key": key,
                    "mapping": mapping.to_dict(),
                    "confidence_level": mapping.confidence_level.value,
                    "reasons": mapping.inference_reasons
                })

        # Sort by confidence (lowest first - most need review)
        pending.sort(key=lambda x: x["mapping"]["confidence"])
        return pending

    def get_mapping_stats(self) -> Dict:
        """Get statistics about learned mappings."""
        by_source = defaultdict(int)
        by_confidence = defaultdict(int)
        by_entity = defaultdict(int)

        for mapping in self.field_mappings.values():
            by_source[mapping.source.value] += 1
            by_confidence[mapping.confidence_level.value] += 1
            by_entity[mapping.entity_type] += 1

        return {
            "total_mappings": len(self.field_mappings),
            "by_source": dict(by_source),
            "by_confidence": dict(by_confidence),
            "by_entity": dict(by_entity),
            "stats": self.stats,
            "coverage_estimate": self._estimate_coverage()
        }

    def _estimate_coverage(self) -> float:
        """Estimate what percentage of fields can be auto-translated."""
        if self.stats["unknown_fields_encountered"] == 0:
            return 1.0

        auto_handled = (self.stats["successful_inferences"] +
                       len([m for m in self.field_mappings.values()
                            if m.source == MappingSource.BUILTIN]))
        total = self.stats["unknown_fields_encountered"] + auto_handled

        return auto_handled / total if total > 0 else 0.0

    # =========================================================================
    # PERSISTENCE
    # =========================================================================

    def _bootstrap_from_builtins(self):
        """Initialize with builtin schema mappings."""
        platforms = [Platform.SALESFORCE, Platform.DYNAMICS365, Platform.LOCAL]

        for entity_type in ["contacts", "companies", "deals", "activities"]:
            entity_fields = SCHEMA_MAPPINGS["fields"].get(entity_type, {})

            for source_platform in platforms:
                source_fields = entity_fields.get(source_platform.value, [])

                for target_platform in platforms:
                    if source_platform == target_platform:
                        continue

                    target_fields = entity_fields.get(target_platform.value, [])

                    for i, source_field in enumerate(source_fields):
                        if i < len(target_fields):
                            key = self._mapping_key(
                                source_platform.value, source_field,
                                target_platform.value, entity_type
                            )

                            if key not in self.field_mappings:
                                self.field_mappings[key] = FieldMapping(
                                    source_platform=source_platform.value,
                                    source_field=source_field,
                                    target_platform=target_platform.value,
                                    target_field=target_fields[i],
                                    entity_type=entity_type,
                                    confidence=1.0,
                                    source=MappingSource.BUILTIN
                                )

    def _save_memory(self):
        """Save learned mappings to disk."""
        memory_file = Path(self.memory_path) / "schema_brain.json"

        data = {
            "version": "1.0",
            "saved_at": datetime.now().isoformat(),
            "field_mappings": {k: v.to_dict() for k, v in self.field_mappings.items()
                              if v.source != MappingSource.BUILTIN},  # Don't save builtins
            "value_mappings": {k: v.to_dict() for k, v in self.value_mappings.items()},
            "field_patterns": dict(self.field_patterns),
            "value_patterns": dict(self.value_patterns),
            "stats": self.stats
        }

        with open(memory_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Also save learning log separately (can get large)
        log_file = Path(self.memory_path) / "learning_log.json"
        with open(log_file, 'w') as f:
            json.dump([e.to_dict() for e in self.learning_log[-1000:]], f, indent=2)

    def _load_memory(self):
        """Load previously learned mappings from disk."""
        memory_file = Path(self.memory_path) / "schema_brain.json"

        if not memory_file.exists():
            return

        try:
            with open(memory_file, 'r') as f:
                data = json.load(f)

            for k, v in data.get("field_mappings", {}).items():
                self.field_mappings[k] = FieldMapping.from_dict(v)

            for k, v in data.get("value_mappings", {}).items():
                self.value_mappings[k] = ValueMapping.from_dict(v)

            self.field_patterns = defaultdict(list, data.get("field_patterns", {}))
            self.value_patterns = defaultdict(dict, data.get("value_patterns", {}))
            self.stats = data.get("stats", self.stats)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load schema memory: {e}")

    def _log_learning_event(
        self,
        event_type: str,
        source_platform: str,
        target_platform: str,
        entity_type: str,
        field_name: str,
        old_value: Optional[str],
        new_value: str,
        confidence_change: float,
        user_id: Optional[str] = None,
        notes: Optional[str] = None
    ):
        """Log a learning event for audit trail."""
        event = LearningEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            source_platform=source_platform,
            target_platform=target_platform,
            entity_type=entity_type,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            confidence_change=confidence_change,
            user_id=user_id,
            notes=notes
        )
        self.learning_log.append(event)

    # =========================================================================
    # EXPORT / REPORTING
    # =========================================================================

    def export_mappings(self, format: str = "json") -> str:
        """Export all learned mappings."""
        mappings = []

        for mapping in self.field_mappings.values():
            mappings.append({
                "from": f"{mapping.source_platform}.{mapping.source_field}",
                "to": f"{mapping.target_platform}.{mapping.target_field}",
                "entity": mapping.entity_type,
                "confidence": f"{mapping.confidence:.0%}",
                "source": mapping.source.value,
                "used": mapping.times_used,
                "reliability": f"{mapping.reliability_score:.0%}"
            })

        if format == "json":
            return json.dumps(mappings, indent=2)
        elif format == "markdown":
            lines = ["# Schema Mappings\n"]
            lines.append("| From | To | Entity | Confidence | Source | Used |")
            lines.append("|------|-----|--------|------------|--------|------|")
            for m in mappings:
                lines.append(f"| {m['from']} | {m['to']} | {m['entity']} | "
                           f"{m['confidence']} | {m['source']} | {m['used']} |")
            return "\n".join(lines)

        return str(mappings)

    def generate_report(self) -> str:
        """Generate a human-readable report of the Schema Brain's state."""
        stats = self.get_mapping_stats()
        pending = self.get_pending_reviews()

        report = []
        report.append("=" * 60)
        report.append("  SCHEMA BRAIN STATUS REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"Total Mappings: {stats['total_mappings']}")
        report.append(f"Coverage Estimate: {stats['coverage_estimate']:.0%}")
        report.append("")
        report.append("Mappings by Source:")
        for source, count in stats['by_source'].items():
            report.append(f"  - {source}: {count}")
        report.append("")
        report.append("Mappings by Confidence:")
        for level, count in stats['by_confidence'].items():
            report.append(f"  - {level}: {count}")
        report.append("")
        report.append(f"Pending Human Review: {len(pending)}")

        if pending[:5]:
            report.append("")
            report.append("Top 5 needing review:")
            for item in pending[:5]:
                m = item['mapping']
                report.append(f"  - {m['source_field']} -> {m['target_field']} "
                            f"({m['confidence']:.0%})")

        report.append("")
        report.append("Activity Stats:")
        for key, value in stats['stats'].items():
            report.append(f"  - {key}: {value}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


# Global instance
schema_brain = SchemaBrain()
