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
