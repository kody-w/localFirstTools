"""
FastAPI server for NeuAI CRM Data Mesh API.
"""

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from neuai_crm.models.schemas import Platform, SCHEMA_MAPPINGS
from neuai_crm.services.data_mesh import DataMesh
from neuai_crm.services.intelligence import IntelligenceLayer


# Initialize core services
data_mesh = DataMesh()
intelligence = IntelligenceLayer(data_mesh)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="NeuAI CRM Data Mesh API",
        description="""
Unified API for managing CRM data across Salesforce, Dynamics 365, and Local CRM.

## Features

- **Schema Translation**: Convert records between platform formats
- **Duplicate Detection**: Find matching records across platforms
- **Conflict Resolution**: Identify and resolve data conflicts
- **Data Sync**: Synchronize data between platforms
- **Natural Language Queries**: Process queries in plain English

## Platforms Supported

- Salesforce (Account, Contact, Opportunity, Task)
- Dynamics 365 (account, contact, opportunity, activitypointer)
- Local CRM (companies, contacts, deals, activities)
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


# Create the application
app = create_app()


# =============================================================================
# Request/Response Models
# =============================================================================

class QueryRequest(BaseModel):
    """Natural language query request."""
    query: str = Field(..., description="Natural language query", min_length=1)
    context: Optional[Dict] = Field(None, description="Additional context")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "How many contacts are in each CRM?",
                "context": None
            }
        }


class TranslateRequest(BaseModel):
    """Record translation request."""
    record: Dict = Field(..., description="Record to translate")
    from_platform: str = Field(..., description="Source platform")
    to_platform: str = Field(..., description="Target platform")
    entity_type: str = Field(..., description="Entity type")

    class Config:
        json_schema_extra = {
            "example": {
                "record": {
                    "FirstName": "John",
                    "LastName": "Doe",
                    "Email": "john.doe@example.com"
                },
                "from_platform": "salesforce",
                "to_platform": "dynamics365",
                "entity_type": "contacts"
            }
        }


class SyncRequest(BaseModel):
    """Platform sync request."""
    source: str = Field(..., description="Source platform")
    target: str = Field(..., description="Target platform")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "salesforce",
                "target": "dynamics365"
            }
        }


class LoadDataRequest(BaseModel):
    """Load data request."""
    platform: str = Field(..., description="Platform to load data into")
    data: Dict = Field(..., description="Data to load")

    class Config:
        json_schema_extra = {
            "example": {
                "platform": "salesforce",
                "data": {
                    "Account": [{"Id": "001", "Name": "Acme Corp"}],
                    "Contact": [{"Id": "003", "FirstName": "John", "LastName": "Doe"}]
                }
            }
        }


class ConflictResolutionRequest(BaseModel):
    """Conflict resolution request."""
    conflict_id: str = Field(..., description="ID of the conflict to resolve")
    resolution: str = Field(..., description="Resolution strategy")
    merged_record: Optional[Dict] = Field(None, description="Merged record if applicable")


# =============================================================================
# API Routes
# =============================================================================

@app.get("/", tags=["Health"])
async def root():
    """API root - returns basic info."""
    return {
        "name": "NeuAI CRM Data Mesh API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "data_mesh": "online",
            "intelligence": "online"
        }
    }


@app.get("/stats", tags=["Data"])
async def get_stats():
    """Get record counts across all platforms."""
    stats = data_mesh.get_stats()
    total = sum(sum(v.values()) for v in stats.values())
    return {
        "stats": stats,
        "total_records": total
    }


@app.get("/schema", tags=["Schema"])
async def get_schema():
    """Get schema mappings between platforms."""
    return {
        "mappings": SCHEMA_MAPPINGS,
        "platforms": [p.value for p in Platform]
    }


@app.get("/schema/{entity_type}", tags=["Schema"])
async def get_entity_schema(entity_type: str):
    """Get schema mapping for a specific entity type."""
    if entity_type not in SCHEMA_MAPPINGS["fields"]:
        raise HTTPException(
            status_code=404,
            detail=f"Entity type '{entity_type}' not found"
        )

    return {
        "entity_type": entity_type,
        "fields": SCHEMA_MAPPINGS["fields"][entity_type],
        "entities": {
            platform: SCHEMA_MAPPINGS["entities"][platform].get(entity_type)
            for platform in ["local", "salesforce", "dynamics365"]
        }
    }


@app.post("/query", tags=["Intelligence"])
async def process_query(request: QueryRequest):
    """
    Process a natural language query.

    Examples:
    - "How many contacts are in each CRM?"
    - "Sync Salesforce to Dynamics 365"
    - "Find duplicates across all systems"
    """
    result = intelligence.process_query(request.query, request.context)
    return result


@app.post("/translate", tags=["Translation"])
async def translate_record(request: TranslateRequest):
    """Translate a record between platforms."""
    try:
        from_platform = Platform(request.from_platform)
        to_platform = Platform(request.to_platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    translated = data_mesh.translate_record(
        request.record,
        from_platform,
        to_platform,
        request.entity_type
    )

    return {
        "status": "success",
        "original": request.record,
        "translated": translated,
        "from_platform": request.from_platform,
        "to_platform": request.to_platform
    }


@app.post("/sync", tags=["Sync"])
async def sync_platforms(request: SyncRequest):
    """Sync data between platforms."""
    try:
        source = Platform(request.source)
        target = Platform(request.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    result = data_mesh.sync_platforms(source, target)

    return {
        "status": "success",
        "source": request.source,
        "target": request.target,
        "result": result
    }


@app.get("/duplicates", tags=["Duplicates"])
async def detect_duplicates(
    threshold: float = Query(0.8, ge=0.0, le=1.0, description="Match confidence threshold")
):
    """Detect duplicate records across platforms."""
    duplicates = data_mesh.detect_duplicates(threshold)

    return {
        "count": len(duplicates),
        "threshold": threshold,
        "duplicates": duplicates
    }


@app.get("/conflicts/{source}/{target}", tags=["Conflicts"])
async def get_conflicts(source: str, target: str):
    """Get conflicts between two platforms."""
    try:
        source_platform = Platform(source)
        target_platform = Platform(target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    conflicts = data_mesh.get_conflicts(source_platform, target_platform)

    return {
        "source": source,
        "target": target,
        "count": len(conflicts),
        "conflicts": conflicts
    }


@app.post("/conflicts/resolve", tags=["Conflicts"])
async def resolve_conflict(request: ConflictResolutionRequest):
    """Resolve a specific conflict."""
    result = data_mesh.resolve_conflict(
        request.conflict_id,
        request.resolution,
        request.merged_record
    )

    return result


@app.post("/load", tags=["Data"])
async def load_data(request: LoadDataRequest):
    """Load data into a platform."""
    try:
        platform = Platform(request.platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    result = data_mesh.load_data(platform, request.data)

    return {
        "status": "success",
        "platform": request.platform,
        **result
    }


@app.get("/export/{platform}", tags=["Data"])
async def export_data(platform: str):
    """Export data in platform-specific format."""
    try:
        platform_enum = Platform(platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    data = data_mesh.export_to_platform(platform_enum)

    return {
        "platform": platform,
        "data": data,
        "record_count": sum(len(v) for v in data.values())
    }


@app.delete("/clear/{platform}", tags=["Data"])
async def clear_platform(platform: str):
    """Clear all data for a platform."""
    try:
        platform_enum = Platform(platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    result = data_mesh.clear_platform(platform_enum)

    return result


@app.get("/sync-log", tags=["Sync"])
async def get_sync_log():
    """Get the sync operation log."""
    return {
        "log": data_mesh.get_sync_log(),
        "count": len(data_mesh.get_sync_log())
    }


@app.get("/conversation", tags=["Intelligence"])
async def get_conversation():
    """Get the conversation history."""
    return {
        "history": intelligence.get_conversation_history(),
        "count": len(intelligence.get_conversation_history())
    }


@app.delete("/conversation", tags=["Intelligence"])
async def clear_conversation():
    """Clear the conversation history."""
    intelligence.clear_history()
    return {"status": "cleared"}


# =============================================================================
# Schema Brain API Routes
# =============================================================================

from neuai_crm.services.schema_brain import schema_brain, MappingSource


class TeachMappingRequest(BaseModel):
    """Request to teach a new mapping."""
    source_platform: str = Field(..., description="Source platform")
    source_field: str = Field(..., description="Source field name")
    target_platform: str = Field(..., description="Target platform")
    target_field: str = Field(..., description="Target field name")
    entity_type: str = Field(..., description="Entity type")
    notes: Optional[str] = Field(None, description="Optional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "source_platform": "salesforce",
                "source_field": "CustomField__c",
                "target_platform": "dynamics365",
                "target_field": "new_customfield",
                "entity_type": "contacts",
                "notes": "Custom field mapping for legacy data"
            }
        }


class ConfirmMappingRequest(BaseModel):
    """Request to confirm or reject a mapping."""
    source_platform: str
    source_field: str
    target_platform: str
    entity_type: str


class AnalyzeRecordRequest(BaseModel):
    """Request to analyze a record for unknown fields."""
    record: Dict = Field(..., description="Record to analyze")
    source_platform: str = Field(..., description="Source platform")
    target_platform: str = Field(..., description="Target platform")
    entity_type: str = Field(..., description="Entity type")


@app.get("/brain/status", tags=["Schema Brain"])
async def get_brain_status():
    """Get Schema Brain status and statistics."""
    stats = schema_brain.get_mapping_stats()
    return {
        "status": "online",
        "stats": stats,
        "report": schema_brain.generate_report()
    }


@app.get("/brain/mappings", tags=["Schema Brain"])
async def get_learned_mappings(
    entity: Optional[str] = Query(None, description="Filter by entity type"),
    source: Optional[str] = Query(None, description="Filter by mapping source"),
    min_confidence: Optional[float] = Query(None, description="Minimum confidence")
):
    """Get all learned schema mappings."""
    mappings = []

    for key, mapping in schema_brain.field_mappings.items():
        if entity and mapping.entity_type != entity:
            continue
        if source and mapping.source.value != source:
            continue
        if min_confidence and mapping.confidence < min_confidence:
            continue

        mappings.append(mapping.to_dict())

    # Sort by confidence
    mappings.sort(key=lambda x: x['confidence'], reverse=True)

    return {
        "count": len(mappings),
        "mappings": mappings
    }


@app.get("/brain/pending", tags=["Schema Brain"])
async def get_pending_reviews():
    """Get mappings that need human review."""
    pending = schema_brain.get_pending_reviews()
    return {
        "count": len(pending),
        "pending": pending
    }


@app.post("/brain/teach", tags=["Schema Brain"])
async def teach_mapping(request: TeachMappingRequest):
    """Teach the Schema Brain a new field mapping."""
    mapping = schema_brain.provide_feedback(
        source_platform=request.source_platform,
        source_field=request.source_field,
        target_platform=request.target_platform,
        entity_type=request.entity_type,
        correct_mapping=request.target_field,
        notes=request.notes
    )

    return {
        "status": "learned",
        "mapping": mapping.to_dict(),
        "message": f"Schema Brain learned: {request.source_field} -> {request.target_field}"
    }


@app.post("/brain/confirm", tags=["Schema Brain"])
async def confirm_mapping(request: ConfirmMappingRequest):
    """Confirm an inferred mapping is correct (boosts confidence)."""
    mapping = schema_brain.confirm_mapping(
        source_platform=request.source_platform,
        source_field=request.source_field,
        target_platform=request.target_platform,
        entity_type=request.entity_type
    )

    if mapping:
        return {
            "status": "confirmed",
            "mapping": mapping.to_dict(),
            "new_confidence": mapping.confidence
        }
    else:
        raise HTTPException(status_code=404, detail="Mapping not found")


@app.post("/brain/reject", tags=["Schema Brain"])
async def reject_mapping(request: ConfirmMappingRequest):
    """Reject an inferred mapping (decreases confidence)."""
    success = schema_brain.reject_mapping(
        source_platform=request.source_platform,
        source_field=request.source_field,
        target_platform=request.target_platform,
        entity_type=request.entity_type
    )

    if success:
        return {"status": "rejected", "message": "Mapping rejected and confidence reduced"}
    else:
        raise HTTPException(status_code=404, detail="Mapping not found")


@app.post("/brain/analyze", tags=["Schema Brain"])
async def analyze_record(request: AnalyzeRecordRequest):
    """Analyze a record and propose mappings for unknown fields."""
    try:
        source = Platform(request.source_platform)
        target = Platform(request.target_platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    proposals = schema_brain.analyze_record(
        request.record,
        source,
        target,
        request.entity_type
    )

    result = {}
    for field_name, inference in proposals.items():
        result[field_name] = {
            "proposed_mapping": inference.proposed_mapping,
            "confidence": inference.confidence,
            "reasons": inference.reasons,
            "alternatives": [
                {"field": f, "confidence": c}
                for f, c in inference.alternatives
            ],
            "needs_review": inference.needs_human_review
        }

    return {
        "unknown_fields": len(proposals),
        "proposals": result
    }


@app.post("/brain/translate", tags=["Schema Brain"])
async def smart_translate(request: TranslateRequest):
    """
    Translate a record using the Schema Brain's learned mappings.

    This uses the self-improving translator that learns from corrections.
    """
    try:
        source = Platform(request.from_platform)
        target = Platform(request.to_platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid platform: {e}")

    translated = {}
    field_info = {}
    needs_review = []

    for field_name, value in request.record.items():
        # Translate field name
        target_field, confidence, review_needed = schema_brain.translate_field(
            field_name, source, target, request.entity_type, request.record
        )

        if target_field:
            # Translate value
            new_value, val_confidence = schema_brain.translate_value(
                value, field_name, source, target, request.entity_type
            )
            translated[target_field] = new_value

            field_info[field_name] = {
                "mapped_to": target_field,
                "confidence": confidence,
                "value_changed": value != new_value
            }

            if review_needed:
                needs_review.append(field_name)
        else:
            # Could not translate - keep original
            translated[field_name] = value
            field_info[field_name] = {
                "mapped_to": None,
                "confidence": 0,
                "error": "No mapping found"
            }
            needs_review.append(field_name)

    return {
        "status": "success",
        "original": request.record,
        "translated": translated,
        "field_mappings": field_info,
        "needs_review": needs_review,
        "review_count": len(needs_review)
    }


@app.get("/brain/export", tags=["Schema Brain"])
async def export_mappings(
    format: str = Query("json", description="Export format (json or markdown)")
):
    """Export all learned mappings."""
    output = schema_brain.export_mappings(format)
    return {
        "format": format,
        "content": output
    }


# =============================================================================
# Schema Discovery API Routes (Audit-First Workflow)
# =============================================================================

from neuai_crm.services.schema_discovery import schema_discovery, AuditStatus, FieldMetadata


class DiscoverSalesforceRequest(BaseModel):
    """Request to discover Salesforce schema."""
    username: str = Field(..., description="Salesforce username")
    password: str = Field(..., description="Salesforce password")
    security_token: str = Field(..., description="Salesforce security token")
    domain: str = Field("login", description="Salesforce domain (login or test)")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "password123",
                "security_token": "XXXXXXXXXXXX",
                "domain": "login"
            }
        }


class DiscoverDynamicsRequest(BaseModel):
    """Request to discover Dynamics 365 schema."""
    access_token: str = Field(..., description="OAuth access token")
    environment_url: str = Field(..., description="Dynamics 365 environment URL")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAi...",
                "environment_url": "https://yourorg.crm.dynamics.com"
            }
        }


class GenerateProposalsRequest(BaseModel):
    """Request to generate mapping proposals."""
    source_platform: str = Field(..., description="Source platform")
    target_platform: str = Field(..., description="Target platform")
    auto_approve_threshold: float = Field(0.95, description="Confidence threshold for auto-approval")

    class Config:
        json_schema_extra = {
            "example": {
                "source_platform": "salesforce",
                "target_platform": "dynamics365",
                "auto_approve_threshold": 0.95
            }
        }


class ApproveProposalRequest(BaseModel):
    """Request to approve a proposal."""
    reviewer: Optional[str] = Field(None, description="Reviewer name")
    notes: Optional[str] = Field(None, description="Review notes")


class ModifyProposalRequest(BaseModel):
    """Request to modify and approve a proposal."""
    new_target_field: str = Field(..., description="New target field name")
    reviewer: Optional[str] = Field(None, description="Reviewer name")
    notes: Optional[str] = Field(None, description="Review notes")

    class Config:
        json_schema_extra = {
            "example": {
                "new_target_field": "emailaddress2",
                "reviewer": "admin",
                "notes": "Corrected to secondary email field"
            }
        }


class BulkApproveRequest(BaseModel):
    """Request to bulk approve proposals."""
    min_confidence: float = Field(0.9, description="Minimum confidence threshold")
    reviewer: Optional[str] = Field(None, description="Reviewer name")


# Mock data for testing without live credentials
MOCK_SALESFORCE_SCHEMA = {
    "account": [
        FieldMetadata("Id", "Account ID", "id", "salesforce", "account", False, True, api_name="Id"),
        FieldMetadata("Name", "Account Name", "string", "salesforce", "account", True, False, 255, api_name="Name"),
        FieldMetadata("Phone", "Phone", "phone", "salesforce", "account", False, False, 40, api_name="Phone"),
        FieldMetadata("Website", "Website", "url", "salesforce", "account", False, False, 255, api_name="Website"),
        FieldMetadata("Industry", "Industry", "picklist", "salesforce", "account", False, False, picklist_values=["Technology", "Finance", "Healthcare"], api_name="Industry"),
        FieldMetadata("BillingStreet", "Billing Street", "string", "salesforce", "account", False, False, 255, api_name="BillingStreet"),
        FieldMetadata("BillingCity", "Billing City", "string", "salesforce", "account", False, False, 40, api_name="BillingCity"),
        FieldMetadata("Description", "Description", "textarea", "salesforce", "account", False, False, api_name="Description"),
    ],
    "contact": [
        FieldMetadata("Id", "Contact ID", "id", "salesforce", "contact", False, True, api_name="Id"),
        FieldMetadata("FirstName", "First Name", "string", "salesforce", "contact", False, False, 40, api_name="FirstName"),
        FieldMetadata("LastName", "Last Name", "string", "salesforce", "contact", True, False, 80, api_name="LastName"),
        FieldMetadata("Email", "Email", "email", "salesforce", "contact", False, False, 80, api_name="Email"),
        FieldMetadata("Phone", "Phone", "phone", "salesforce", "contact", False, False, 40, api_name="Phone"),
        FieldMetadata("Title", "Title", "string", "salesforce", "contact", False, False, 128, api_name="Title"),
        FieldMetadata("AccountId", "Account ID", "reference", "salesforce", "contact", False, False, reference_to="Account", api_name="AccountId"),
    ],
    "opportunity": [
        FieldMetadata("Id", "Opportunity ID", "id", "salesforce", "opportunity", False, True, api_name="Id"),
        FieldMetadata("Name", "Opportunity Name", "string", "salesforce", "opportunity", True, False, 120, api_name="Name"),
        FieldMetadata("Amount", "Amount", "currency", "salesforce", "opportunity", False, False, api_name="Amount"),
        FieldMetadata("StageName", "Stage", "picklist", "salesforce", "opportunity", True, False, picklist_values=["Prospecting", "Qualification", "Proposal", "Closed Won", "Closed Lost"], api_name="StageName"),
        FieldMetadata("CloseDate", "Close Date", "date", "salesforce", "opportunity", True, False, api_name="CloseDate"),
        FieldMetadata("Probability", "Probability", "decimal", "salesforce", "opportunity", False, False, api_name="Probability"),
        FieldMetadata("AccountId", "Account ID", "reference", "salesforce", "opportunity", False, False, reference_to="Account", api_name="AccountId"),
    ],
}

MOCK_DYNAMICS_SCHEMA = {
    "account": [
        FieldMetadata("accountid", "Account", "id", "dynamics365", "account", False, True, api_name="accountid"),
        FieldMetadata("name", "Account Name", "string", "dynamics365", "account", True, False, 160, api_name="name"),
        FieldMetadata("telephone1", "Main Phone", "phone", "dynamics365", "account", False, False, 50, api_name="telephone1"),
        FieldMetadata("websiteurl", "Website", "url", "dynamics365", "account", False, False, 200, api_name="websiteurl"),
        FieldMetadata("industrycode", "Industry", "picklist", "dynamics365", "account", False, False, picklist_values=["Technology", "Financial", "Healthcare"], api_name="industrycode"),
        FieldMetadata("address1_line1", "Street 1", "string", "dynamics365", "account", False, False, 250, api_name="address1_line1"),
        FieldMetadata("address1_city", "City", "string", "dynamics365", "account", False, False, 80, api_name="address1_city"),
        FieldMetadata("description", "Description", "textarea", "dynamics365", "account", False, False, api_name="description"),
    ],
    "contact": [
        FieldMetadata("contactid", "Contact", "id", "dynamics365", "contact", False, True, api_name="contactid"),
        FieldMetadata("firstname", "First Name", "string", "dynamics365", "contact", False, False, 50, api_name="firstname"),
        FieldMetadata("lastname", "Last Name", "string", "dynamics365", "contact", True, False, 50, api_name="lastname"),
        FieldMetadata("emailaddress1", "Email", "email", "dynamics365", "contact", False, False, 100, api_name="emailaddress1"),
        FieldMetadata("telephone1", "Business Phone", "phone", "dynamics365", "contact", False, False, 50, api_name="telephone1"),
        FieldMetadata("jobtitle", "Job Title", "string", "dynamics365", "contact", False, False, 100, api_name="jobtitle"),
        FieldMetadata("parentcustomerid", "Company Name", "reference", "dynamics365", "contact", False, False, reference_to="account", api_name="parentcustomerid"),
    ],
    "opportunity": [
        FieldMetadata("opportunityid", "Opportunity", "id", "dynamics365", "opportunity", False, True, api_name="opportunityid"),
        FieldMetadata("name", "Topic", "string", "dynamics365", "opportunity", True, False, 300, api_name="name"),
        FieldMetadata("estimatedvalue", "Est. Revenue", "currency", "dynamics365", "opportunity", False, False, api_name="estimatedvalue"),
        FieldMetadata("stepname", "Pipeline Phase", "string", "dynamics365", "opportunity", False, False, 200, api_name="stepname"),
        FieldMetadata("estimatedclosedate", "Est. Close Date", "date", "dynamics365", "opportunity", False, False, api_name="estimatedclosedate"),
        FieldMetadata("closeprobability", "Probability", "decimal", "dynamics365", "opportunity", False, False, api_name="closeprobability"),
        FieldMetadata("parentaccountid", "Account", "reference", "dynamics365", "opportunity", False, False, reference_to="account", api_name="parentaccountid"),
    ],
}


def _init_mock_schemas():
    """Initialize schema discovery with mock data for demo/testing."""
    from neuai_crm.services.schema_discovery import FieldType

    # Convert string types to FieldType enum
    for platform_schema in [MOCK_SALESFORCE_SCHEMA, MOCK_DYNAMICS_SCHEMA]:
        for entity, fields in platform_schema.items():
            for i, f in enumerate(fields):
                if isinstance(f.field_type, str):
                    platform_schema[entity][i] = FieldMetadata(
                        name=f.name,
                        label=f.label,
                        field_type=FieldType(f.field_type),
                        platform=f.platform,
                        entity=f.entity,
                        required=f.required,
                        unique=f.unique,
                        max_length=f.max_length,
                        picklist_values=f.picklist_values,
                        reference_to=f.reference_to,
                        description=f.description,
                        default_value=f.default_value,
                        is_custom=f.is_custom,
                        is_system=f.is_system,
                        api_name=f.api_name
                    )


@app.get("/discovery/status", tags=["Schema Discovery"])
async def get_discovery_status():
    """Get schema discovery status and statistics."""
    summary = schema_discovery.get_audit_summary()

    schemas_loaded = {
        platform: len(entities) > 0
        for platform, entities in schema_discovery.schemas.items()
    }

    return {
        "status": "online",
        "schemas_discovered": schemas_loaded,
        "field_counts": {
            platform: sum(len(fields) for fields in entities.values())
            for platform, entities in schema_discovery.schemas.items()
        },
        "audit_summary": summary,
        "discovery_runs": len(schema_discovery.discovery_history)
    }


@app.post("/discovery/salesforce", tags=["Schema Discovery"])
async def discover_salesforce_schema(request: DiscoverSalesforceRequest):
    """
    Discover schema from a Salesforce instance.

    Connects to Salesforce using the provided credentials and extracts
    metadata for all standard and custom objects.
    """
    try:
        from simple_salesforce import Salesforce

        sf = Salesforce(
            username=request.username,
            password=request.password,
            security_token=request.security_token,
            domain=request.domain
        )

        result = schema_discovery.discover_salesforce(sf)

        return {
            "status": "success",
            "result": {
                "entities_discovered": result.entities_discovered,
                "fields_discovered": result.fields_discovered,
                "custom_fields": result.custom_fields,
                "duration_seconds": result.duration_seconds,
                "errors": result.errors
            }
        }

    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="simple_salesforce package not installed. Run: pip install simple-salesforce"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Salesforce connection failed: {str(e)}")


@app.post("/discovery/dynamics365", tags=["Schema Discovery"])
async def discover_dynamics365_schema(request: DiscoverDynamicsRequest):
    """
    Discover schema from a Dynamics 365 instance.

    Connects to Dynamics 365 using the provided OAuth token and extracts
    metadata for all standard and custom entities.
    """
    try:
        result = schema_discovery.discover_dynamics365(
            request.access_token,
            request.environment_url
        )

        return {
            "status": "success",
            "result": {
                "entities_discovered": result.entities_discovered,
                "fields_discovered": result.fields_discovered,
                "custom_fields": result.custom_fields,
                "duration_seconds": result.duration_seconds,
                "errors": result.errors
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Dynamics 365 connection failed: {str(e)}")


@app.post("/discovery/mock", tags=["Schema Discovery"])
async def load_mock_schemas():
    """
    Load mock schema data for testing without live CRM connections.

    This is useful for demos and development.
    """
    _init_mock_schemas()

    schema_discovery.schemas["salesforce"] = MOCK_SALESFORCE_SCHEMA
    schema_discovery.schemas["dynamics365"] = MOCK_DYNAMICS_SCHEMA
    schema_discovery._save_state()

    return {
        "status": "success",
        "message": "Mock schemas loaded",
        "salesforce": {
            "entities": list(MOCK_SALESFORCE_SCHEMA.keys()),
            "total_fields": sum(len(f) for f in MOCK_SALESFORCE_SCHEMA.values())
        },
        "dynamics365": {
            "entities": list(MOCK_DYNAMICS_SCHEMA.keys()),
            "total_fields": sum(len(f) for f in MOCK_DYNAMICS_SCHEMA.values())
        }
    }


@app.post("/discovery/propose", tags=["Schema Discovery"])
async def generate_proposals(request: GenerateProposalsRequest):
    """
    Generate mapping proposals between two platforms.

    The AI analyzes field names, types, and patterns to propose intelligent mappings.
    High-confidence proposals may be auto-approved.
    """
    if not schema_discovery.schemas.get(request.source_platform):
        raise HTTPException(
            status_code=400,
            detail=f"No schema discovered for {request.source_platform}. Run discovery first."
        )

    if not schema_discovery.schemas.get(request.target_platform):
        raise HTTPException(
            status_code=400,
            detail=f"No schema discovered for {request.target_platform}. Run discovery first."
        )

    proposals = schema_discovery.generate_mapping_proposals(
        request.source_platform,
        request.target_platform,
        request.auto_approve_threshold
    )

    # Categorize results
    auto_approved = [p for p in proposals if p.status == AuditStatus.AUTO_APPROVED]
    pending = [p for p in proposals if p.status == AuditStatus.PENDING]

    return {
        "status": "success",
        "total_proposals": len(proposals),
        "auto_approved": len(auto_approved),
        "pending_review": len(pending),
        "summary": {
            "high_confidence": len([p for p in pending if p.confidence >= 0.8]),
            "medium_confidence": len([p for p in pending if 0.6 <= p.confidence < 0.8]),
            "low_confidence": len([p for p in pending if p.confidence < 0.6])
        }
    }


@app.get("/discovery/audit-queue", tags=["Schema Discovery"])
async def get_audit_queue(
    status: Optional[str] = Query(None, description="Filter by status"),
    entity: Optional[str] = Query(None, description="Filter by entity"),
    min_confidence: Optional[float] = Query(None, description="Minimum confidence"),
    limit: int = Query(50, description="Maximum results to return"),
    offset: int = Query(0, description="Results offset")
):
    """
    Get proposals pending human audit.

    Returns proposals sorted by confidence (highest first) for efficient review.
    """
    queue = schema_discovery.audit_queue

    # Filter by status
    if status:
        try:
            status_enum = AuditStatus(status)
            queue = [p for p in queue if p.status == status_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    # Filter by entity
    if entity:
        queue = [p for p in queue if p.source_entity == entity or p.target_entity == entity]

    # Filter by confidence
    if min_confidence:
        queue = [p for p in queue if p.confidence >= min_confidence]

    # Sort by confidence (highest first)
    queue = sorted(queue, key=lambda x: x.confidence, reverse=True)

    # Paginate
    total = len(queue)
    queue = queue[offset:offset + limit]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "proposals": [p.to_dict() for p in queue]
    }


@app.get("/discovery/audit-queue/{proposal_id}", tags=["Schema Discovery"])
async def get_proposal(proposal_id: str):
    """Get a specific proposal by ID."""
    for p in schema_discovery.audit_queue:
        if p.id == proposal_id:
            return {"proposal": p.to_dict()}

    # Check approved mappings
    if proposal_id in schema_discovery.approved_mappings:
        return {"proposal": schema_discovery.approved_mappings[proposal_id].to_dict()}

    raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")


@app.post("/discovery/approve/{proposal_id}", tags=["Schema Discovery"])
async def approve_proposal(proposal_id: str, request: ApproveProposalRequest):
    """
    Approve a mapping proposal.

    Moves the proposal from the audit queue to approved mappings.
    """
    result = schema_discovery.approve_proposal(
        proposal_id,
        request.reviewer,
        request.notes
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found in audit queue")

    return {
        "status": "approved",
        "proposal": result.to_dict()
    }


@app.post("/discovery/reject/{proposal_id}", tags=["Schema Discovery"])
async def reject_proposal(proposal_id: str, request: ApproveProposalRequest):
    """
    Reject a mapping proposal.

    Removes the proposal from the audit queue.
    """
    result = schema_discovery.reject_proposal(
        proposal_id,
        request.reviewer,
        request.notes
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found in audit queue")

    return {
        "status": "rejected",
        "proposal": result.to_dict()
    }


@app.post("/discovery/modify/{proposal_id}", tags=["Schema Discovery"])
async def modify_proposal(proposal_id: str, request: ModifyProposalRequest):
    """
    Modify and approve a proposal with a different target field.

    Use this when the AI's proposal was close but needs correction.
    """
    result = schema_discovery.modify_proposal(
        proposal_id,
        request.new_target_field,
        request.reviewer,
        request.notes
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found in audit queue")

    return {
        "status": "modified",
        "proposal": result.to_dict()
    }


@app.post("/discovery/bulk-approve", tags=["Schema Discovery"])
async def bulk_approve_proposals(request: BulkApproveRequest):
    """
    Bulk approve all proposals above a confidence threshold.

    Efficient for approving many high-confidence proposals at once.
    """
    approved_count = schema_discovery.bulk_approve(
        request.min_confidence,
        request.reviewer
    )

    return {
        "status": "success",
        "approved_count": approved_count,
        "threshold": request.min_confidence,
        "remaining_in_queue": len(schema_discovery.audit_queue)
    }


@app.get("/discovery/approved", tags=["Schema Discovery"])
async def get_approved_mappings(
    entity: Optional[str] = Query(None, description="Filter by entity"),
    source_platform: Optional[str] = Query(None, description="Filter by source platform")
):
    """Get all approved mappings."""
    mappings = list(schema_discovery.approved_mappings.values())

    if entity:
        mappings = [m for m in mappings if m.source_entity == entity or m.target_entity == entity]

    if source_platform:
        mappings = [m for m in mappings if m.source_platform == source_platform]

    return {
        "total": len(mappings),
        "mappings": [m.to_dict() for m in mappings]
    }


@app.get("/discovery/export", tags=["Schema Discovery"])
async def export_approved_mappings():
    """
    Export approved mappings in a format usable by the sync engine.

    Returns mappings ready to be used for data translation.
    """
    export = schema_discovery.export_approved_mappings()
    return export


@app.get("/discovery/schemas/{platform}", tags=["Schema Discovery"])
async def get_discovered_schema(platform: str):
    """Get the discovered schema for a platform."""
    if platform not in schema_discovery.schemas:
        raise HTTPException(status_code=404, detail=f"Platform {platform} not found")

    platform_schema = schema_discovery.schemas[platform]

    return {
        "platform": platform,
        "entities": list(platform_schema.keys()),
        "schema": {
            entity: [f.to_dict() for f in fields]
            for entity, fields in platform_schema.items()
        }
    }


@app.get("/discovery/schemas/{platform}/{entity}", tags=["Schema Discovery"])
async def get_entity_fields(platform: str, entity: str):
    """Get discovered fields for a specific entity."""
    if platform not in schema_discovery.schemas:
        raise HTTPException(status_code=404, detail=f"Platform {platform} not found")

    platform_schema = schema_discovery.schemas[platform]

    if entity not in platform_schema:
        raise HTTPException(status_code=404, detail=f"Entity {entity} not found in {platform}")

    fields = platform_schema[entity]

    return {
        "platform": platform,
        "entity": entity,
        "field_count": len(fields),
        "fields": [f.to_dict() for f in fields]
    }


@app.delete("/discovery/reset", tags=["Schema Discovery"])
async def reset_discovery():
    """Reset all discovery data (schemas, proposals, approvals)."""
    schema_discovery.schemas = {"salesforce": {}, "dynamics365": {}, "local": {}}
    schema_discovery.audit_queue = []
    schema_discovery.approved_mappings = {}
    schema_discovery.discovery_history = []
    schema_discovery._save_state()

    return {"status": "reset", "message": "All discovery data cleared"}


@app.get("/discovery/history", tags=["Schema Discovery"])
async def get_discovery_history():
    """Get history of all discovery operations."""
    from dataclasses import asdict

    return {
        "runs": [asdict(r) for r in schema_discovery.discovery_history],
        "total_runs": len(schema_discovery.discovery_history)
    }
