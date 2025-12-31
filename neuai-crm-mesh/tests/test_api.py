"""Tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient

from neuai_crm.api.server import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "NeuAI CRM Data Mesh API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["services"]["data_mesh"] == "online"


class TestDataEndpoints:
    """Test data management endpoints."""

    def test_get_stats_empty(self, client):
        """Test getting stats with no data."""
        response = client.get("/stats")

        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "total_records" in data

    def test_load_data(self, client):
        """Test loading data into a platform."""
        payload = {
            "platform": "salesforce",
            "data": {
                "Account": [
                    {"Id": "001", "Name": "Test Corp"}
                ],
                "Contact": [
                    {"Id": "003", "FirstName": "John", "LastName": "Doe"}
                ]
            }
        }

        response = client.post("/load", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["records_loaded"] == 2

    def test_load_data_invalid_platform(self, client):
        """Test loading data with invalid platform."""
        payload = {
            "platform": "invalid_platform",
            "data": {}
        }

        response = client.post("/load", json=payload)

        assert response.status_code == 400

    def test_export_data(self, client):
        """Test exporting data from a platform."""
        # First load some data
        client.post("/load", json={
            "platform": "local",
            "data": {
                "companies": [{"id": "001", "name": "Test Corp"}],
                "contacts": [],
                "deals": [],
                "activities": []
            }
        })

        response = client.get("/export/local")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "companies" in data["data"]


class TestSchemaEndpoints:
    """Test schema-related endpoints."""

    def test_get_schema(self, client):
        """Test getting the full schema."""
        response = client.get("/schema")

        assert response.status_code == 200
        data = response.json()
        assert "mappings" in data
        assert "platforms" in data
        assert "salesforce" in data["platforms"]

    def test_get_entity_schema(self, client):
        """Test getting schema for a specific entity."""
        response = client.get("/schema/contacts")

        assert response.status_code == 200
        data = response.json()
        assert data["entity_type"] == "contacts"
        assert "fields" in data

    def test_get_entity_schema_not_found(self, client):
        """Test getting schema for non-existent entity."""
        response = client.get("/schema/nonexistent")

        assert response.status_code == 404


class TestTranslationEndpoints:
    """Test translation endpoints."""

    def test_translate_record(self, client):
        """Test translating a record between platforms."""
        payload = {
            "record": {
                "FirstName": "John",
                "LastName": "Doe",
                "Email": "john@example.com"
            },
            "from_platform": "salesforce",
            "to_platform": "dynamics365",
            "entity_type": "contacts"
        }

        response = client.post("/translate", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "translated" in data
        assert data["translated"]["firstname"] == "John"
        assert data["translated"]["emailaddress1"] == "john@example.com"

    def test_translate_invalid_platform(self, client):
        """Test translation with invalid platform."""
        payload = {
            "record": {"FirstName": "John"},
            "from_platform": "invalid",
            "to_platform": "dynamics365",
            "entity_type": "contacts"
        }

        response = client.post("/translate", json=payload)

        assert response.status_code == 400


class TestQueryEndpoints:
    """Test natural language query endpoints."""

    def test_process_query(self, client):
        """Test processing a natural language query."""
        payload = {
            "query": "How many records are in each CRM?"
        }

        response = client.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "intent" in data
        assert "message" in data

    def test_help_query(self, client):
        """Test help query."""
        payload = {
            "query": "What can you help me with?"
        }

        response = client.post("/query", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "help"
        assert "capabilities" in data


class TestSyncEndpoints:
    """Test sync-related endpoints."""

    def test_sync_platforms(self, client):
        """Test syncing data between platforms."""
        # First load some data
        client.post("/load", json={
            "platform": "salesforce",
            "data": {
                "Account": [{"Id": "001", "Name": "Test Corp"}],
                "Contact": [],
                "Opportunity": [],
                "Task": []
            }
        })

        # Then sync
        response = client.post("/sync", json={
            "source": "salesforce",
            "target": "dynamics365"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_sync_log(self, client):
        """Test getting the sync log."""
        response = client.get("/sync-log")

        assert response.status_code == 200
        data = response.json()
        assert "log" in data
        assert "count" in data


class TestDuplicateEndpoints:
    """Test duplicate detection endpoints."""

    def test_detect_duplicates(self, client):
        """Test detecting duplicates."""
        response = client.get("/duplicates")

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "duplicates" in data
        assert "threshold" in data

    def test_detect_duplicates_with_threshold(self, client):
        """Test detecting duplicates with custom threshold."""
        response = client.get("/duplicates?threshold=0.5")

        assert response.status_code == 200
        data = response.json()
        assert data["threshold"] == 0.5


class TestConflictEndpoints:
    """Test conflict-related endpoints."""

    def test_get_conflicts(self, client):
        """Test getting conflicts between platforms."""
        response = client.get("/conflicts/salesforce/dynamics365")

        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "conflicts" in data

    def test_get_conflicts_invalid_platform(self, client):
        """Test getting conflicts with invalid platform."""
        response = client.get("/conflicts/invalid/dynamics365")

        assert response.status_code == 400
