"""Tests for the schema translator service."""

import pytest
from neuai_crm.models.schemas import Platform
from neuai_crm.services.translator import SchemaTranslator


@pytest.fixture
def translator():
    """Create a translator instance for testing."""
    return SchemaTranslator()


class TestSchemaTranslator:
    """Test cases for SchemaTranslator."""

    def test_translate_contact_salesforce_to_dynamics(self, translator):
        """Test translating a contact from Salesforce to Dynamics 365."""
        sf_contact = {
            "Id": "003SF00001",
            "FirstName": "John",
            "LastName": "Doe",
            "Email": "john.doe@example.com",
            "Phone": "+1-555-123-4567",
            "AccountId": "001SF00001",
            "Title": "CTO",
            "CreatedDate": "2024-01-15T09:00:00Z"
        }

        result = translator.translate_entity(
            sf_contact,
            Platform.SALESFORCE,
            Platform.DYNAMICS365,
            "contacts"
        )

        assert result["contactid"] == "003SF00001"
        assert result["firstname"] == "John"
        assert result["lastname"] == "Doe"
        assert result["emailaddress1"] == "john.doe@example.com"
        assert result["telephone1"] == "+1-555-123-4567"
        assert result["parentcustomerid"] == "001SF00001"
        assert result["jobtitle"] == "CTO"

    def test_translate_contact_dynamics_to_local(self, translator):
        """Test translating a contact from Dynamics 365 to Local CRM."""
        d365_contact = {
            "contactid": "con-001",
            "firstname": "Jane",
            "lastname": "Smith",
            "emailaddress1": "jane.smith@example.com",
            "telephone1": "+1-555-987-6543",
            "parentcustomerid": "acc-001",
            "jobtitle": "CEO",
            "createdon": "2024-02-20T10:00:00Z"
        }

        result = translator.translate_entity(
            d365_contact,
            Platform.DYNAMICS365,
            Platform.LOCAL,
            "contacts"
        )

        assert result["id"] == "con-001"
        assert result["firstName"] == "Jane"
        assert result["lastName"] == "Smith"
        assert result["email"] == "jane.smith@example.com"
        assert result["phone"] == "+1-555-987-6543"
        assert result["companyId"] == "acc-001"
        assert result["jobTitle"] == "CEO"

    def test_translate_deal_with_stage(self, translator):
        """Test that deal stages are correctly translated."""
        local_deal = {
            "id": "deal-001",
            "name": "Big Deal",
            "value": 100000,
            "stage": "proposal",
            "companyId": "comp-001",
            "contactId": "cont-001",
            "probability": 60,
            "closeDate": "2024-06-30",
            "createdAt": "2024-01-20T10:00:00Z"
        }

        # Translate to Salesforce
        sf_result = translator.translate_entity(
            local_deal,
            Platform.LOCAL,
            Platform.SALESFORCE,
            "deals"
        )

        assert sf_result["StageName"] == "Proposal/Price Quote"

        # Translate to Dynamics 365
        d365_result = translator.translate_entity(
            local_deal,
            Platform.LOCAL,
            Platform.DYNAMICS365,
            "deals"
        )

        assert d365_result["stepname"] == "3 - Propose"

    def test_translate_batch(self, translator):
        """Test batch translation of records."""
        contacts = [
            {"Id": "001", "FirstName": "John", "LastName": "Doe", "Email": "john@example.com"},
            {"Id": "002", "FirstName": "Jane", "LastName": "Smith", "Email": "jane@example.com"}
        ]

        results = translator.translate_batch(
            contacts,
            Platform.SALESFORCE,
            Platform.LOCAL,
            "contacts"
        )

        assert len(results) == 2
        assert results[0]["firstName"] == "John"
        assert results[1]["firstName"] == "Jane"

    def test_get_field_mapping(self, translator):
        """Test getting field mappings between platforms."""
        mapping = translator.get_field_mapping(
            "contacts",
            Platform.SALESFORCE,
            Platform.DYNAMICS365
        )

        assert mapping["FirstName"] == "firstname"
        assert mapping["LastName"] == "lastname"
        assert mapping["Email"] == "emailaddress1"
        assert mapping["Phone"] == "telephone1"


class TestStageTranslation:
    """Test cases for deal stage translation."""

    def test_all_stages_salesforce_to_dynamics(self, translator):
        """Test all stage translations from Salesforce to Dynamics."""
        stage_mappings = [
            ("Prospecting", "1 - Qualify"),
            ("Qualification", "2 - Develop"),
            ("Proposal/Price Quote", "3 - Propose"),
            ("Negotiation/Review", "4 - Close"),
            ("Closed Won", "Won"),
            ("Closed Lost", "Lost")
        ]

        for sf_stage, expected_d365_stage in stage_mappings:
            deal = {
                "Id": "001",
                "Name": "Test Deal",
                "Amount": 1000,
                "StageName": sf_stage,
                "AccountId": "",
                "ContactId": "",
                "Probability": 50,
                "CloseDate": "2024-12-31",
                "CreatedDate": "2024-01-01"
            }

            result = translator.translate_entity(
                deal,
                Platform.SALESFORCE,
                Platform.DYNAMICS365,
                "deals"
            )

            assert result["stepname"] == expected_d365_stage, \
                f"Expected {expected_d365_stage} but got {result['stepname']}"

    def test_all_stages_local_to_salesforce(self, translator):
        """Test all stage translations from Local to Salesforce."""
        stage_mappings = [
            ("lead", "Prospecting"),
            ("qualified", "Qualification"),
            ("proposal", "Proposal/Price Quote"),
            ("negotiation", "Negotiation/Review"),
            ("won", "Closed Won"),
            ("lost", "Closed Lost")
        ]

        for local_stage, expected_sf_stage in stage_mappings:
            deal = {
                "id": "001",
                "name": "Test Deal",
                "value": 1000,
                "stage": local_stage,
                "companyId": "",
                "contactId": "",
                "probability": 50,
                "closeDate": "2024-12-31",
                "createdAt": "2024-01-01"
            }

            result = translator.translate_entity(
                deal,
                Platform.LOCAL,
                Platform.SALESFORCE,
                "deals"
            )

            assert result["StageName"] == expected_sf_stage, \
                f"Expected {expected_sf_stage} but got {result['StageName']}"
