"""Tests for the duplicate detection service."""

import pytest
from neuai_crm.models.schemas import Platform
from neuai_crm.services.duplicates import DuplicateDetector


@pytest.fixture
def detector():
    """Create a detector instance for testing."""
    return DuplicateDetector(threshold=0.8)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return {
        Platform.SALESFORCE: {
            "accounts": [
                {"Id": "001", "Name": "Acme Corp", "Industry": "Technology"}
            ],
            "contacts": [
                {"Id": "003", "FirstName": "John", "LastName": "Doe",
                 "Email": "john.doe@acme.com", "Phone": "+1-555-123-4567"}
            ],
            "opportunities": [],
            "tasks": []
        },
        Platform.DYNAMICS365: {
            "accounts": [
                {"accountid": "acc-001", "name": "Acme Corporation", "industrycode": "Tech"}
            ],
            "contacts": [
                {"contactid": "con-001", "firstname": "John", "lastname": "Doe",
                 "emailaddress1": "john.doe@acme.com", "telephone1": "5551234567"}
            ],
            "opportunities": [],
            "activities": []
        },
        Platform.LOCAL: {
            "companies": [],
            "contacts": [],
            "deals": [],
            "activities": []
        }
    }


class TestDuplicateDetector:
    """Test cases for DuplicateDetector."""

    def test_detect_duplicate_contacts_by_email(self, detector, sample_data):
        """Test detecting duplicate contacts across platforms by email."""
        duplicates = detector.detect_duplicates(sample_data)

        # Should find one duplicate (John Doe in SF and D365)
        contact_dups = [d for d in duplicates if d.entity_type == "contact"]
        assert len(contact_dups) == 1

        dup = contact_dups[0]
        assert dup.match_field == "email"
        assert dup.match_value == "john.doe@acme.com"
        assert dup.confidence == 1.0
        assert len(dup.records) == 2

        platforms = {r["platform"] for r in dup.records}
        assert platforms == {"salesforce", "dynamics365"}

    def test_detect_duplicate_companies_by_name(self, detector):
        """Test detecting duplicate companies by normalized name."""
        data = {
            Platform.SALESFORCE: {
                "accounts": [
                    {"Id": "001", "Name": "Acme Inc", "Industry": "Tech"}
                ],
                "contacts": [],
                "opportunities": [],
                "tasks": []
            },
            Platform.DYNAMICS365: {
                "accounts": [
                    {"accountid": "acc-001", "name": "Acme Incorporated", "industrycode": "Tech"}
                ],
                "contacts": [],
                "opportunities": [],
                "activities": []
            },
            Platform.LOCAL: {
                "companies": [],
                "contacts": [],
                "deals": [],
                "activities": []
            }
        }

        duplicates = detector.detect_duplicates(data)

        company_dups = [d for d in duplicates if d.entity_type == "company"]
        assert len(company_dups) == 1

        dup = company_dups[0]
        assert dup.match_field == "name"
        assert "acme" in dup.match_value.lower()

    def test_no_duplicates_different_emails(self, detector):
        """Test that different emails don't trigger duplicates."""
        data = {
            Platform.SALESFORCE: {
                "accounts": [],
                "contacts": [
                    {"Id": "001", "FirstName": "John", "LastName": "Doe",
                     "Email": "john@company1.com", "Phone": ""}
                ],
                "opportunities": [],
                "tasks": []
            },
            Platform.DYNAMICS365: {
                "accounts": [],
                "contacts": [
                    {"contactid": "001", "firstname": "John", "lastname": "Doe",
                     "emailaddress1": "john@company2.com", "telephone1": ""}
                ],
                "opportunities": [],
                "activities": []
            },
            Platform.LOCAL: {
                "companies": [],
                "contacts": [],
                "deals": [],
                "activities": []
            }
        }

        duplicates = detector.detect_duplicates(data)

        # Same name but different email should not be flagged as email duplicate
        email_dups = [d for d in duplicates if d.match_field == "email"]
        assert len(email_dups) == 0

    def test_normalize_phone(self, detector):
        """Test phone number normalization."""
        assert detector._normalize_phone("+1-555-123-4567") == "15551234567"
        assert detector._normalize_phone("(555) 123-4567") == "5551234567"
        assert detector._normalize_phone("555.123.4567") == "5551234567"
        assert detector._normalize_phone("5551234567") == "5551234567"

    def test_normalize_company_name(self, detector):
        """Test company name normalization."""
        assert detector._normalize_company_name("Acme Inc") == "acme"
        assert detector._normalize_company_name("Acme Inc.") == "acme"
        assert detector._normalize_company_name("Acme Incorporated") == "acme"
        assert detector._normalize_company_name("Acme LLC") == "acme"
        assert detector._normalize_company_name("Acme Corp") == "acme"
        assert detector._normalize_company_name("Acme Corporation") == "acme"
        assert detector._normalize_company_name("ACME COMPANY") == "acme"

    def test_to_dict_conversion(self, detector, sample_data):
        """Test that DuplicateMatch converts to dict correctly."""
        duplicates = detector.detect_duplicates(sample_data)

        for dup in duplicates:
            dup_dict = dup.to_dict()

            assert "type" in dup_dict
            assert "match_field" in dup_dict
            assert "match_value" in dup_dict
            assert "confidence" in dup_dict
            assert "records" in dup_dict
            assert isinstance(dup_dict["records"], list)


class TestCrossplatformDuplicates:
    """Test cross-platform duplicate detection scenarios."""

    def test_three_way_duplicate(self, detector):
        """Test detecting the same contact across all three platforms."""
        data = {
            Platform.SALESFORCE: {
                "accounts": [],
                "contacts": [
                    {"Id": "sf-001", "FirstName": "Sarah", "LastName": "Chen",
                     "Email": "sarah@example.com", "Phone": ""}
                ],
                "opportunities": [],
                "tasks": []
            },
            Platform.DYNAMICS365: {
                "accounts": [],
                "contacts": [
                    {"contactid": "d365-001", "firstname": "Sarah", "lastname": "Chen",
                     "emailaddress1": "sarah@example.com", "telephone1": ""}
                ],
                "opportunities": [],
                "activities": []
            },
            Platform.LOCAL: {
                "companies": [],
                "contacts": [
                    {"id": "local-001", "firstName": "Sarah", "lastName": "Chen",
                     "email": "sarah@example.com", "phone": ""}
                ],
                "deals": [],
                "activities": []
            }
        }

        duplicates = detector.detect_duplicates(data)

        # Should find duplicates involving all three platforms
        contact_dups = [d for d in duplicates if d.entity_type == "contact"]
        assert len(contact_dups) >= 1

        # At least one duplicate should span multiple platforms
        for dup in contact_dups:
            platforms = {r["platform"] for r in dup.records}
            assert len(platforms) >= 2
