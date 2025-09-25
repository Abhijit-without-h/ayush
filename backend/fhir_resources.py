"""
FHIR resource builders for AyushBridge
"""
from typing import List, Optional, Dict, Any
from models import (
    ParametersResource, Parameter, ParameterPart, Coding,
    ConceptMapResource, ConceptMapGroup, ConceptMapElement, 
    ConceptMapTarget, EquivalenceEnum
)


class FHIRResourceBuilder:
    """Builder class for FHIR resources"""
    
    @staticmethod
    def build_translate_response(
        result: bool,
        source_code: str,
        target_code: Optional[str] = None,
        target_display: Optional[str] = None,
        target_system: Optional[str] = None,
        equivalence: EquivalenceEnum = EquivalenceEnum.equivalent,
        ai_explanation: Optional[str] = None
    ) -> ParametersResource:
        """
        Build FHIR Parameters resource for translate operation response
        """
        parameters = [
            Parameter(name="result", valueBoolean=result)
        ]
        
        if result and target_code and target_system:
            # Add match parameter with nested parts
            match_parts = [
                ParameterPart(name="equivalence", valueCode=equivalence.value),
                ParameterPart(
                    name="concept", 
                    valueCoding=Coding(
                        system=target_system,
                        code=target_code,
                        display=target_display
                    )
                )
            ]
            
            parameters.append(
                Parameter(name="match", part=match_parts)
            )
        
        # Add AI explanation if provided
        if ai_explanation:
            parameters.append(
                Parameter(name="ai_explanation", valueString=ai_explanation)
            )
        
        return ParametersResource(parameter=parameters)
    
    @staticmethod
    def build_concept_map(
        map_id: str,
        name: str,
        title: str,
        source_system: str,
        target_system: str,
        mappings: List[Dict[str, Any]],
        description: Optional[str] = None
    ) -> ConceptMapResource:
        """
        Build FHIR ConceptMap resource
        """
        elements = []
        
        for mapping in mappings:
            targets = []
            for target in mapping.get("targets", []):
                targets.append(ConceptMapTarget(
                    code=target["code"],
                    display=target.get("display"),
                    equivalence=EquivalenceEnum(target.get("equivalence", "equivalent"))
                ))
            
            elements.append(ConceptMapElement(
                code=mapping["source_code"],
                display=mapping.get("source_display"),
                target=targets
            ))
        
        group = ConceptMapGroup(
            source=source_system,
            target=target_system,
            element=elements
        )
        
        return ConceptMapResource(
            id=map_id,
            url=f"http://ayushbridge.org/fhir/ConceptMap/{map_id}",
            name=name,
            title=title,
            description=description,
            group=[group]
        )
    
    @staticmethod
    def build_error_parameters(
        error_message: str,
        error_code: Optional[str] = None
    ) -> ParametersResource:
        """
        Build FHIR Parameters resource for error response
        """
        parameters = [
            Parameter(name="result", valueBoolean=False),
            Parameter(name="error", valueString=error_message)
        ]
        
        if error_code:
            parameters.append(
                Parameter(name="error_code", valueString=error_code)
            )
        
        return ParametersResource(parameter=parameters)
    
    @staticmethod
    def build_operation_outcome(
        severity: str,
        code: str,
        details: str
    ) -> Dict[str, Any]:
        """
        Build FHIR OperationOutcome resource for detailed error information
        """
        return {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": severity,
                    "code": code,
                    "details": {
                        "text": details
                    }
                }
            ]
        }


# Pre-defined ConceptMap configurations
PREDEFINED_CONCEPT_MAPS = {
    "namaste-to-icd11": {
        "name": "NAMASTEtoICD11",
        "title": "Mapping from NAMASTE to ICD-11",
        "description": "Official mapping between NAMASTE codes for traditional Indian medicine and ICD-11 codes",
        "source_system": "http://namaste.gov.in/fhir/CodeSystem/namaste",
        "target_system": "http://id.who.int/icd11/mms"
    },
    "icd11-to-namaste": {
        "name": "ICD11toNAMASTE", 
        "title": "Mapping from ICD-11 to NAMASTE",
        "description": "Reverse mapping between ICD-11 codes and NAMASTE codes for traditional Indian medicine",
        "source_system": "http://id.who.int/icd11/mms",
        "target_system": "http://namaste.gov.in/fhir/CodeSystem/namaste"
    }
}
