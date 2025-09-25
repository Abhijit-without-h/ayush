"""
Pydantic models for AyushBridge API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class EquivalenceEnum(str, Enum):
    """FHIR ConceptMap equivalence codes"""
    relatedto = "relatedto"
    equivalent = "equivalent"
    equal = "equal"
    wider = "wider"
    subsumes = "subsumes"
    narrower = "narrower"
    specializes = "specializes"
    inexact = "inexact"
    unmatched = "unmatched"
    disjoint = "disjoint"


class TranslateRequest(BaseModel):
    """Request model for code translation"""
    code: str = Field(..., description="The source code to translate", example="NAM-1001")
    system: str = Field(
        ..., 
        description="Source code system URI", 
        example="http://namaste.gov.in/fhir/CodeSystem/namaste"
    )
    target_system: str = Field(
        ..., 
        description="Target code system URI", 
        example="http://id.who.int/icd11/mms"
    )
    language: Optional[str] = Field(
        None, 
        description="Language code for AI explanation (ISO 639-1)", 
        example="hi",
        max_length=10
    )


class Coding(BaseModel):
    """FHIR Coding data type"""
    system: str = Field(..., description="Code system URI")
    code: str = Field(..., description="Code value")
    display: Optional[str] = Field(None, description="Human readable display text")


class ConceptMapTarget(BaseModel):
    """Target concept in ConceptMap"""
    code: str = Field(..., description="Target code")
    display: Optional[str] = Field(None, description="Target display text")
    equivalence: EquivalenceEnum = Field(..., description="Mapping equivalence")


class ConceptMapElement(BaseModel):
    """Source concept in ConceptMap"""
    code: str = Field(..., description="Source code")
    display: Optional[str] = Field(None, description="Source display text")
    target: List[ConceptMapTarget] = Field(..., description="Target mappings")


class ConceptMapGroup(BaseModel):
    """Group of mappings in ConceptMap"""
    source: str = Field(..., description="Source system URI")
    target: str = Field(..., description="Target system URI")
    element: List[ConceptMapElement] = Field(..., description="Concept mappings")


class ConceptMapResource(BaseModel):
    """FHIR ConceptMap resource"""
    resourceType: str = Field(default="ConceptMap", description="FHIR resource type")
    id: str = Field(..., description="Resource identifier")
    url: str = Field(..., description="Canonical URL")
    name: str = Field(..., description="Computer friendly name")
    title: str = Field(..., description="Human readable title")
    status: str = Field(default="active", description="Resource status")
    description: Optional[str] = Field(None, description="Resource description")
    group: List[ConceptMapGroup] = Field(..., description="Mapping groups")


class ParameterPart(BaseModel):
    """Parameter part for nested parameters"""
    name: str = Field(..., description="Parameter name")
    valueCode: Optional[str] = Field(None, description="Code value")
    valueCoding: Optional[Coding] = Field(None, description="Coding value")


class Parameter(BaseModel):
    """FHIR Parameters parameter"""
    name: str = Field(..., description="Parameter name")
    valueBoolean: Optional[bool] = Field(None, description="Boolean value")
    valueString: Optional[str] = Field(None, description="String value")
    part: Optional[List[ParameterPart]] = Field(None, description="Parameter parts")


class ParametersResource(BaseModel):
    """FHIR Parameters resource"""
    resourceType: str = Field(default="Parameters", description="FHIR resource type")
    parameter: List[Parameter] = Field(..., description="Parameters list")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    code: Optional[str] = Field(None, description="Error code")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
    components: Dict[str, str] = Field(..., description="Component health status")
