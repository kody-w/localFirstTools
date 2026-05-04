"""
Duplicate detection service for finding matching records across CRM platforms.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

from neuai_crm.models.schemas import Platform


@dataclass
class DuplicateMatch:
    """Represents a duplicate match between records."""
    entity_type: str
    match_field: str
    match_value: str
    confidence: float
    records: List[Dict]

    def to_dict(self) -> Dict:
        return {
            "type": self.entity_type,
            "match_field": self.match_field,
            "match_value": self.match_value,
            "confidence": self.confidence,
            "records": self.records
        }


class DuplicateDetector:
    """
    Detects duplicate records across CRM platforms using various matching strategies.
    """

    def __init__(self, threshold: float = 0.8):
        """
        Initialize the duplicate detector.

        Args:
            threshold: Minimum confidence score (0-1) for a match
        """
        self.threshold = threshold

    def detect_duplicates(self, data: Dict[Platform, Dict]) -> List[DuplicateMatch]:
        """
        Detect duplicate records across all platforms.

        Args:
            data: Dictionary of platform data {Platform: {entity: [records]}}

        Returns:
            List of DuplicateMatch objects
        """
        duplicates = []

        # Detect contact duplicates by email
        contact_dups = self._detect_contact_duplicates(data)
        duplicates.extend(contact_dups)

        # Detect company duplicates by name
        company_dups = self._detect_company_duplicates(data)
        duplicates.extend(company_dups)

        return duplicates

    def _detect_contact_duplicates(self, data: Dict[Platform, Dict]) -> List[DuplicateMatch]:
        """Detect duplicate contacts across platforms by email."""
        duplicates = []
        all_contacts = []

        for platform in Platform:
            contacts_key = "contacts"
            platform_data = data.get(platform, {})

            for contact in platform_data.get(contacts_key, []):
                email = self._extract_email(contact, platform)
                name = self._extract_name(contact, platform)
                phone = self._extract_phone(contact, platform)

                all_contacts.append({
                    "platform": platform.value,
                    "record": contact,
                    "email": email.lower() if email else "",
                    "name": name.lower() if name else "",
                    "phone": self._normalize_phone(phone) if phone else ""
                })

        # Group by email (exact match)
        email_groups = self._group_by_field(all_contacts, "email")
        for email, contacts in email_groups.items():
            if len(contacts) > 1:
                platforms = list(set(c["platform"] for c in contacts))
                if len(platforms) > 1:  # Only flag cross-platform duplicates
                    duplicates.append(DuplicateMatch(
                        entity_type="contact",
                        match_field="email",
                        match_value=email,
                        confidence=1.0,
                        records=contacts
                    ))

        # Group by normalized phone (if no email match)
        phone_groups = self._group_by_field(all_contacts, "phone")
        for phone, contacts in phone_groups.items():
            if phone and len(contacts) > 1:
                platforms = list(set(c["platform"] for c in contacts))
                # Check if these weren't already matched by email
                emails = [c["email"] for c in contacts if c["email"]]
                if len(platforms) > 1 and len(set(emails)) > 1:
                    duplicates.append(DuplicateMatch(
                        entity_type="contact",
                        match_field="phone",
                        match_value=phone,
                        confidence=0.9,
                        records=contacts
                    ))

        return duplicates

    def _detect_company_duplicates(self, data: Dict[Platform, Dict]) -> List[DuplicateMatch]:
        """Detect duplicate companies across platforms by name."""
        duplicates = []
        all_companies = []

        entity_keys = {
            Platform.LOCAL: "companies",
            Platform.SALESFORCE: "accounts",
            Platform.DYNAMICS365: "accounts"
        }

        for platform in Platform:
            entity_key = entity_keys[platform]
            platform_data = data.get(platform, {})

            for company in platform_data.get(entity_key, []):
                name = self._extract_company_name(company, platform)

                all_companies.append({
                    "platform": platform.value,
                    "record": company,
                    "name": self._normalize_company_name(name) if name else ""
                })

        # Group by normalized name
        name_groups = self._group_by_field(all_companies, "name")
        for name, companies in name_groups.items():
            if name and len(companies) > 1:
                platforms = list(set(c["platform"] for c in companies))
                if len(platforms) > 1:
                    duplicates.append(DuplicateMatch(
                        entity_type="company",
                        match_field="name",
                        match_value=name,
                        confidence=0.95,
                        records=companies
                    ))

        return duplicates

    def _group_by_field(self, records: List[Dict], field: str) -> Dict[str, List[Dict]]:
        """Group records by a specific field value."""
        groups = {}
        for record in records:
            value = record.get(field, "")
            if value:
                if value not in groups:
                    groups[value] = []
                groups[value].append(record)
        return groups

    def _extract_email(self, record: Dict, platform: Platform) -> Optional[str]:
        """Extract email from a contact record."""
        field_map = {
            Platform.LOCAL: "email",
            Platform.SALESFORCE: "Email",
            Platform.DYNAMICS365: "emailaddress1"
        }
        return record.get(field_map[platform])

    def _extract_name(self, record: Dict, platform: Platform) -> str:
        """Extract full name from a contact record."""
        if platform == Platform.LOCAL:
            return f"{record.get('firstName', '')} {record.get('lastName', '')}".strip()
        elif platform == Platform.SALESFORCE:
            return f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()
        else:
            return f"{record.get('firstname', '')} {record.get('lastname', '')}".strip()

    def _extract_phone(self, record: Dict, platform: Platform) -> Optional[str]:
        """Extract phone from a contact record."""
        field_map = {
            Platform.LOCAL: "phone",
            Platform.SALESFORCE: "Phone",
            Platform.DYNAMICS365: "telephone1"
        }
        return record.get(field_map[platform])

    def _extract_company_name(self, record: Dict, platform: Platform) -> Optional[str]:
        """Extract company name from an account record."""
        field_map = {
            Platform.LOCAL: "name",
            Platform.SALESFORCE: "Name",
            Platform.DYNAMICS365: "name"
        }
        return record.get(field_map[platform])

    def _normalize_phone(self, phone: str) -> str:
        """Normalize a phone number for comparison."""
        # Remove all non-digit characters
        return re.sub(r'\D', '', phone)

    def _normalize_company_name(self, name: str) -> str:
        """Normalize a company name for comparison."""
        # Remove common suffixes and normalize
        normalized = name.lower().strip()
        suffixes = [
            " inc", " inc.", " incorporated",
            " llc", " l.l.c.",
            " ltd", " ltd.", " limited",
            " corp", " corp.", " corporation",
            " co", " co.", " company"
        ]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
        return normalized.strip()

    def find_matches_for_record(
        self,
        record: Dict,
        platform: Platform,
        entity_type: str,
        data: Dict[Platform, Dict]
    ) -> List[DuplicateMatch]:
        """
        Find matching records for a specific record.

        Args:
            record: The record to find matches for
            platform: The platform of the source record
            entity_type: Type of entity
            data: All platform data

        Returns:
            List of matching records
        """
        matches = []

        if entity_type in ["contact", "contacts"]:
            email = self._extract_email(record, platform)
            if email:
                # Search all platforms for matching email
                for target_platform in Platform:
                    if target_platform != platform:
                        for contact in data.get(target_platform, {}).get("contacts", []):
                            target_email = self._extract_email(contact, target_platform)
                            if target_email and target_email.lower() == email.lower():
                                matches.append(DuplicateMatch(
                                    entity_type="contact",
                                    match_field="email",
                                    match_value=email,
                                    confidence=1.0,
                                    records=[
                                        {"platform": platform.value, "record": record},
                                        {"platform": target_platform.value, "record": contact}
                                    ]
                                ))

        return matches


# Global detector instance
detector = DuplicateDetector()
