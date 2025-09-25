"""
AyushBridge: FHIR R4-compliant microservice for NAMASTE to ICD-11 code mapping
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv


load_dotenv()

# Import our modules
from models import (
    TranslateRequest, ParametersResource, ConceptMapResource, 
    ErrorResponse, HealthResponse
)
from mapping_engine import get_mapping_engine, MappingEngine
from ai_service import get_ai_service, GeminiAIService, validate_language_code
from fhir_resources import FHIRResourceBuilder, PREDEFINED_CONCEPT_MAPS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
mapping_engine: Optional[MappingEngine] = None
ai_service: Optional[GeminiAIService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global mapping_engine, ai_service
    
    # Startup
    logger.info("Starting AyushBridge service...")
    
    try:
        # Initialize mapping engine
        mapping_engine = get_mapping_engine()
        logger.info("Mapping engine initialized")
        
        # Initialize AI service
        ai_service = get_ai_service()
        logger.info("AI service initialized")
        
        # Test AI service connection
        if ai_service.test_connection():
            logger.info("AI service connection test successful")
        else:
            logger.warning("AI service connection test failed")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    # Shutdown
    logger.info("Shutting down AyushBridge service...")


# Create FastAPI app with comprehensive OpenAPI documentation
app = FastAPI(
    title="AyushBridge FHIR Terminology Service",
    description="""
🌉 **AyushBridge** is a FHIR R4-compliant microservice that bridges India's traditional AYUSH medicine with the global healthcare ecosystem.

## Features

- **FHIR R4 Compliant**: Standardized API following HL7 FHIR R4 specification
- **Bidirectional Mapping**: Translate between NAMASTE codes (Ayurveda, Siddha, Unani) and ICD-11
- **AI-Powered Explanations**: Intelligent multilingual explanations powered by advanced AI
- **15 Traditional Medicine Systems**: Support for Ayurveda, Siddha, and Unani medicine codes
- **100+ Languages**: AI explanations available in Hindi, Tamil, Bengali, and many more

## Code Systems

- **NAMASTE**: `http://namaste.gov.in/fhir/CodeSystem/namaste`
- **ICD-11**: `http://id.who.int/icd11/mms`

## Authentication

Currently no authentication required for demonstration purposes. In production, implement OAuth 2.0 or API keys.

---

*Powered by advanced AI technology for multilingual medical explanations*
    """,
    version="1.0.0",
    terms_of_service="https://ayushbridge.org/terms",
    contact={
        "name": "AyushBridge Support",
        "url": "https://ayushbridge.org/contact",
        "email": "support@ayushbridge.org"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.ayushbridge.org",
            "description": "Production server"
        }
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health Check",
    description="Check the health status of the AyushBridge service and its components."
)
async def health_check():
    """Health check endpoint"""
    try:
        # Test mapping engine
        mapping_stats = mapping_engine.get_statistics() if mapping_engine else {}
        mapping_status = "healthy" if mapping_engine else "error"
        
        # Test AI service
        ai_status = "healthy" if ai_service and ai_service.test_connection() else "error"
        
        return HealthResponse(
            status="healthy",
            version="1.0.0", 
            timestamp=datetime.utcnow().isoformat() + "Z",
            components={
                "mapping_engine": mapping_status,
                "ai_service": ai_status,
                "total_mappings": str(mapping_stats.get("total_mappings", 0))
            }
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.post(
    "/translate",
    response_model=ParametersResource,
    tags=["Terminology Operations"],
    summary="Translate Code",
    description="""
Translate a medical code from one terminology system to another.

**Supported translations:**
- NAMASTE → ICD-11
- ICD-11 → NAMASTE

**AI Explanations:**
When the `language` parameter is provided, the service generates a multilingual explanation of the medical mapping using advanced AI technology.

**Supported Languages:**
- `hi` - Hindi
- `ta` - Tamil  
- `bn` - Bengali
- `en` - English
- And 100+ more languages...

**Example Request:**
```json
{
  "code": "NAM-1001",
  "system": "http://namaste.gov.in/fhir/CodeSystem/namaste",
  "target_system": "http://id.who.int/icd11/mms",
  "language": "hi"
}
```
    """,
    responses={
        200: {
            "description": "Translation successful",
            "content": {
                "application/json": {
                    "example": {
                        "resourceType": "Parameters",
                        "parameter": [
                            {"name": "result", "valueBoolean": True},
                            {
                                "name": "match",
                                "part": [
                                    {"name": "equivalence", "valueCode": "equivalent"},
                                    {
                                        "name": "concept",
                                        "valueCoding": {
                                            "system": "http://id.who.int/icd11/mms",
                                            "code": "DB64.0",
                                            "display": "Iron deficiency anaemia"
                                        }
                                    }
                                ]
                            },
                            {
                                "name": "ai_explanation",
                                "valueString": "पाण्डु रोग आयुर्वेद में रक्त की कमी की स्थिति है।"
                            }
                        ]
                    }
                }
            }
        },
        404: {"description": "Code not found"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"}
    }
)
async def translate_code(request: TranslateRequest):
    """Translate a code from one system to another"""
    try:
        logger.info(f"Translation request: {request.code} from {request.system} to {request.target_system}")
        
        # Validate language code if provided
        if request.language and not validate_language_code(request.language):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported language code: {request.language}"
            )
        
        # Perform translation
        success, primary_mapping, all_mappings = mapping_engine.translate_code(
            request.code, request.system, request.target_system
        )
        
        if not success:
            return FHIRResourceBuilder.build_translate_response(
                result=False,
                source_code=request.code
            )
        
        # Get AI explanation if language is specified
        ai_explanation = None
        if request.language and primary_mapping and ai_service:
            try:
                # Determine source and target based on translation direction
                if request.system == "http://namaste.gov.in/fhir/CodeSystem/namaste":
                    source_display = primary_mapping.namaste_display
                    target_display = primary_mapping.icd11_display
                    target_code = primary_mapping.icd11_code
                else:
                    source_display = primary_mapping.icd11_display
                    target_display = primary_mapping.namaste_display
                    target_code = primary_mapping.namaste_code
                
                ai_explanation = await ai_service.generate_mapping_explanation(
                    source_code=request.code,
                    source_display=source_display,
                    target_code=target_code,
                    target_display=target_display,
                    language=request.language
                )
            except Exception as e:
                logger.warning(f"AI explanation generation failed: {str(e)}")
        
        # Build response
        if request.system == "http://namaste.gov.in/fhir/CodeSystem/namaste":
            return FHIRResourceBuilder.build_translate_response(
                result=True,
                source_code=request.code,
                target_code=primary_mapping.icd11_code,
                target_display=primary_mapping.icd11_display,
                target_system=request.target_system,
                equivalence=primary_mapping.equivalence,
                ai_explanation=ai_explanation
            )
        else:
            return FHIRResourceBuilder.build_translate_response(
                result=True,
                source_code=request.code,
                target_code=primary_mapping.namaste_code,
                target_display=primary_mapping.namaste_display,
                target_system=request.target_system,
                equivalence=primary_mapping.equivalence,
                ai_explanation=ai_explanation
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@app.get(
    "/ConceptMap/{concept_map_id}",
    response_model=ConceptMapResource,
    tags=["Terminology Resources"],
    summary="Get ConceptMap",
    description="""
Retrieve a FHIR ConceptMap resource containing predefined mappings.

**Available ConceptMaps:**
- `namaste-to-icd11` - Mappings from NAMASTE codes to ICD-11
- `icd11-to-namaste` - Reverse mappings from ICD-11 to NAMASTE codes

ConceptMap resources are useful for bulk operations and EMR integration.
    """,
    responses={
        200: {"description": "ConceptMap retrieved successfully"},
        404: {"description": "ConceptMap not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_concept_map(
    concept_map_id: str = Path(
        ...,
        description="ConceptMap identifier",
        examples=["namaste-to-icd11"]
    )
):
    """Get a FHIR ConceptMap resource by ID"""
    try:
        logger.info(f"ConceptMap request: {concept_map_id}")
        
        # Check if it's a predefined ConceptMap
        if concept_map_id not in PREDEFINED_CONCEPT_MAPS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ConceptMap '{concept_map_id}' not found"
            )
        
        config = PREDEFINED_CONCEPT_MAPS[concept_map_id]
        
        # Get mappings for the ConceptMap
        mappings = mapping_engine.get_mappings_for_concept_map(
            config["source_system"],
            config["target_system"]
        )
        
        # Build ConceptMap resource
        concept_map = FHIRResourceBuilder.build_concept_map(
            map_id=concept_map_id,
            name=config["name"],
            title=config["title"],
            source_system=config["source_system"],
            target_system=config["target_system"],
            mappings=mappings,
            description=config.get("description")
        )
        
        return concept_map
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ConceptMap retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve ConceptMap: {str(e)}"
        )


@app.get(
    "/search",
    tags=["Search Operations"],
    summary="Search Mappings", 
    description="""
Search through available code mappings using text queries.

**Searchable fields:**
- NAMASTE code display names
- ICD-11 code display names  
- Mapping notes

**Example:** Search for "diabetes" to find all diabetes-related mappings.
    """,
    response_model=Dict[str, Any]
)
async def search_mappings(
    q: str = Query(
        ...,
        description="Search query",
        examples=["diabetes"],
        min_length=2
    ),
    limit: int = Query(
        default=10,
        description="Maximum number of results",
        ge=1,
        le=100
    )
):
    """Search mappings by text query"""
    try:
        logger.info(f"Search request: '{q}' (limit: {limit})")
        
        # Perform search
        results = mapping_engine.search_mappings(q)
        
        # Limit results
        limited_results = results[:limit]
        
        # Format response
        return {
            "query": q,
            "total_results": len(results),
            "returned_results": len(limited_results),
            "results": [mapping.to_dict() for mapping in limited_results]
        }
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@app.get(
    "/statistics",
    tags=["System"],
    summary="Mapping Statistics",
    description="Get statistics about the available code mappings and system health.",
    response_model=Dict[str, Any]
)
async def get_statistics():
    """Get mapping statistics"""
    try:
        stats = mapping_engine.get_statistics()
        return {
            "service": "AyushBridge",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **stats
        }
        
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


@app.post(
    "/analyze",
    tags=["AI Analysis"],
    summary="Disease Analysis",
    description="""
Generate comprehensive medical analysis for diseases and conditions using advanced AI.

**Features:**
- Traditional medicine perspective (Ayurveda, Siddha, Unani)
- Modern medical understanding
- Pathophysiology and mechanisms
- Treatment recommendations and medications
- Dietary and lifestyle guidance

**Example Request:**
```json
{
  "condition": "diabetes",
  "traditional_system": "Ayurveda", 
  "language": "hi",
  "include_medications": true
}
```

**Supported Systems:** Ayurveda, Siddha, Unani
**Languages:** 50+ languages including Hindi (हिन्दी), Tamil (தமிழ்), Bengali (বাংলা), Telugu (తెలుగు), Arabic (العربية), and English
    """,
    response_model=Dict[str, Any]
)
async def analyze_disease(
    condition: str = Query(
        ...,
        description="Disease or condition name to analyze",
        examples=["diabetes", "hypertension", "arthritis", "asthma"]
    ),
    traditional_system: str = Query(
        default="Ayurveda",
        description="Traditional medicine system",
        examples=["Ayurveda", "Siddha", "Unani"]
    ),
    language: str = Query(
        default="en", 
        description="Language for analysis (ISO 639-1)",
        examples=["en", "hi", "ta", "bn"]
    ),
    include_medications: bool = Query(
        default=True,
        description="Include medication and treatment information"
    )
):
    """Generate comprehensive disease analysis using AI"""
    try:
        logger.info(f"Disease analysis request: {condition} in {traditional_system} ({language})")
        
        # Validate inputs
        if traditional_system not in ["Ayurveda", "Siddha", "Unani"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Traditional system must be one of: Ayurveda, Siddha, Unani"
            )
        
        if language and not validate_language_code(language):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported language code: {language}"
            )
        
        # Generate AI analysis if AI service is available
        analysis = None
        if ai_service:
            analysis = await ai_service.generate_disease_analysis(
                condition_name=condition,
                traditional_system=traditional_system,
                language=language,
                include_medications=include_medications
            )
        
        # Search for related mappings
        related_mappings = mapping_engine.search_mappings(condition)
        
        return {
            "condition": condition,
            "traditional_system": traditional_system,
            "language": language,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ai_analysis": analysis,
            "related_mappings": [mapping.to_dict() for mapping in related_mappings[:5]],
            "has_ai_analysis": analysis is not None,
            "total_related_codes": len(related_mappings)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Disease analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
