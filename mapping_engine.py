"""
Core mapping engine for NAMASTE to ICD-11 code translation
"""
import json
import logging
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path
from models import EquivalenceEnum

# Configure logging
logger = logging.getLogger(__name__)


class CodeMapping:
    """Represents a single code mapping between systems"""
    
    def __init__(self, mapping_data: Dict[str, Any]):
        self.namaste_code: str = mapping_data["namaste_code"]
        self.namaste_display: str = mapping_data["namaste_display"]
        self.namaste_system: str = mapping_data["namaste_system"]
        self.icd11_code: str = mapping_data["icd11_code"]
        self.icd11_display: str = mapping_data["icd11_display"]
        self.equivalence: EquivalenceEnum = EquivalenceEnum(mapping_data["equivalence"])
        self.notes: Optional[str] = mapping_data.get("notes")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert mapping to dictionary"""
        return {
            "namaste_code": self.namaste_code,
            "namaste_display": self.namaste_display,
            "namaste_system": self.namaste_system,
            "icd11_code": self.icd11_code,
            "icd11_display": self.icd11_display,
            "equivalence": self.equivalence.value,
            "notes": self.notes
        }


class MappingEngine:
    """Core engine for code mapping operations"""
    
    def __init__(self, mappings_file: Optional[str] = None):
        """Initialize the mapping engine"""
        self.mappings_file = mappings_file or "mappings/namaste_icd11_mappings.json"
        self.mappings: Dict[str, CodeMapping] = {}
        self.reverse_mappings: Dict[str, List[CodeMapping]] = {}
        self.metadata: Dict[str, Any] = {}
        
        self._load_mappings()
        
        logger.info(f"Mapping engine initialized with {len(self.mappings)} mappings")
    
    def _load_mappings(self):
        """Load mappings from JSON file"""
        try:
            mappings_path = Path(self.mappings_file)
            if not mappings_path.exists():
                logger.error(f"Mappings file not found: {self.mappings_file}")
                return
            
            with open(mappings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.metadata = data.get("metadata", {})
            
            # Load forward mappings (NAMASTE -> ICD-11)
            for mapping_data in data.get("mappings", []):
                mapping = CodeMapping(mapping_data)
                self.mappings[mapping.namaste_code] = mapping
                
                # Build reverse mappings (ICD-11 -> NAMASTE)
                if mapping.icd11_code not in self.reverse_mappings:
                    self.reverse_mappings[mapping.icd11_code] = []
                self.reverse_mappings[mapping.icd11_code].append(mapping)
            
            logger.info(f"Loaded {len(self.mappings)} mappings from {self.mappings_file}")
            
        except Exception as e:
            logger.error(f"Error loading mappings: {str(e)}")
            raise
    
    def translate_namaste_to_icd11(
        self, 
        namaste_code: str
    ) -> Tuple[bool, Optional[CodeMapping]]:
        """
        Translate NAMASTE code to ICD-11
        
        Args:
            namaste_code: Source NAMASTE code
            
        Returns:
            Tuple of (success, mapping or None)
        """
        try:
            mapping = self.mappings.get(namaste_code)
            if mapping:
                logger.debug(f"Found mapping: {namaste_code} -> {mapping.icd11_code}")
                return True, mapping
            else:
                logger.debug(f"No mapping found for NAMASTE code: {namaste_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"Error translating {namaste_code}: {str(e)}")
            return False, None
    
    def translate_icd11_to_namaste(
        self, 
        icd11_code: str
    ) -> Tuple[bool, List[CodeMapping]]:
        """
        Translate ICD-11 code to NAMASTE (may have multiple matches)
        
        Args:
            icd11_code: Source ICD-11 code
            
        Returns:
            Tuple of (success, list of mappings)
        """
        try:
            mappings = self.reverse_mappings.get(icd11_code, [])
            if mappings:
                logger.debug(f"Found {len(mappings)} reverse mappings for {icd11_code}")
                return True, mappings
            else:
                logger.debug(f"No reverse mapping found for ICD-11 code: {icd11_code}")
                return False, []
                
        except Exception as e:
            logger.error(f"Error reverse translating {icd11_code}: {str(e)}")
            return False, []
    
    def translate_code(
        self,
        code: str,
        source_system: str,
        target_system: str
    ) -> Tuple[bool, Optional[CodeMapping], List[CodeMapping]]:
        """
        Generic code translation between systems
        
        Args:
            code: Source code to translate
            source_system: Source system URI
            target_system: Target system URI
            
        Returns:
            Tuple of (success, primary_mapping, all_mappings)
        """
        namaste_system = "http://namaste.gov.in/fhir/CodeSystem/namaste"
        icd11_system = "http://id.who.int/icd11/mms"
        
        try:
            # NAMASTE to ICD-11
            if source_system == namaste_system and target_system == icd11_system:
                success, mapping = self.translate_namaste_to_icd11(code)
                return success, mapping, [mapping] if mapping else []
            
            # ICD-11 to NAMASTE  
            elif source_system == icd11_system and target_system == namaste_system:
                success, mappings = self.translate_icd11_to_namaste(code)
                primary = mappings[0] if mappings else None
                return success, primary, mappings
            
            else:
                logger.warning(f"Unsupported translation: {source_system} -> {target_system}")
                return False, None, []
                
        except Exception as e:
            logger.error(f"Error in generic translation: {str(e)}")
            return False, None, []
    
    def get_mapping_by_code(self, namaste_code: str) -> Optional[CodeMapping]:
        """Get mapping by NAMASTE code"""
        return self.mappings.get(namaste_code)
    
    def search_mappings(
        self, 
        query: str, 
        search_fields: List[str] = None
    ) -> List[CodeMapping]:
        """
        Search mappings by text query
        
        Args:
            query: Search query
            search_fields: Fields to search in (defaults to display names)
            
        Returns:
            List of matching mappings
        """
        if search_fields is None:
            search_fields = ["namaste_display", "icd11_display", "notes"]
        
        query_lower = query.lower()
        results = []
        
        for mapping in self.mappings.values():
            for field in search_fields:
                field_value = getattr(mapping, field, "")
                if field_value and query_lower in field_value.lower():
                    results.append(mapping)
                    break
        
        logger.debug(f"Search for '{query}' returned {len(results)} results")
        return results
    
    def get_mappings_for_concept_map(
        self,
        source_system: str,
        target_system: str
    ) -> List[Dict[str, Any]]:
        """
        Get mappings formatted for FHIR ConceptMap resource
        
        Args:
            source_system: Source system URI
            target_system: Target system URI
            
        Returns:
            List of mapping dictionaries for ConceptMap
        """
        namaste_system = "http://namaste.gov.in/fhir/CodeSystem/namaste"
        icd11_system = "http://id.who.int/icd11/mms"
        
        concept_map_mappings = []
        
        if source_system == namaste_system and target_system == icd11_system:
            # NAMASTE -> ICD-11 mappings
            for mapping in self.mappings.values():
                concept_map_mappings.append({
                    "source_code": mapping.namaste_code,
                    "source_display": mapping.namaste_display,
                    "targets": [{
                        "code": mapping.icd11_code,
                        "display": mapping.icd11_display,
                        "equivalence": mapping.equivalence.value
                    }]
                })
        
        elif source_system == icd11_system and target_system == namaste_system:
            # ICD-11 -> NAMASTE mappings (grouped by ICD-11 code)
            processed_icd11_codes = set()
            
            for icd11_code, mappings in self.reverse_mappings.items():
                if icd11_code not in processed_icd11_codes:
                    targets = []
                    for mapping in mappings:
                        targets.append({
                            "code": mapping.namaste_code,
                            "display": mapping.namaste_display,
                            "equivalence": mapping.equivalence.value
                        })
                    
                    concept_map_mappings.append({
                        "source_code": icd11_code,
                        "source_display": mappings[0].icd11_display,
                        "targets": targets
                    })
                    
                    processed_icd11_codes.add(icd11_code)
        
        return concept_map_mappings
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get mapping statistics"""
        system_counts = {}
        equivalence_counts = {}
        
        for mapping in self.mappings.values():
            # Count by traditional medicine system
            system = mapping.namaste_system
            system_counts[system] = system_counts.get(system, 0) + 1
            
            # Count by equivalence type
            equiv = mapping.equivalence.value
            equivalence_counts[equiv] = equivalence_counts.get(equiv, 0) + 1
        
        return {
            "total_mappings": len(self.mappings),
            "by_traditional_system": system_counts,
            "by_equivalence": equivalence_counts,
            "reverse_mappings": len(self.reverse_mappings),
            "metadata": self.metadata
        }
    
    def validate_mapping(self, mapping: CodeMapping) -> List[str]:
        """Validate a mapping for consistency"""
        errors = []
        
        if not mapping.namaste_code:
            errors.append("Missing NAMASTE code")
        
        if not mapping.icd11_code:
            errors.append("Missing ICD-11 code")
        
        if not mapping.namaste_display:
            errors.append("Missing NAMASTE display name")
        
        if not mapping.icd11_display:
            errors.append("Missing ICD-11 display name")
        
        if mapping.namaste_system not in ["Ayurveda", "Siddha", "Unani"]:
            errors.append("Invalid traditional medicine system")
        
        return errors


# Global mapping engine instance
_mapping_engine_instance: Optional[MappingEngine] = None


def get_mapping_engine() -> MappingEngine:
    """Get or create the mapping engine singleton instance"""
    global _mapping_engine_instance
    if _mapping_engine_instance is None:
        _mapping_engine_instance = MappingEngine()
    return _mapping_engine_instance
