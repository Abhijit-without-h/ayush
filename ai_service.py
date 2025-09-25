"""
AI service for multilingual explanations using Google Gemini 2.5 Flash
"""
import os
import logging
from typing import Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logger = logging.getLogger(__name__)


class GeminiAIService:
    """Service for generating multilingual medical explanations using Gemini 2.5 Flash"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini AI service"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model - using Gemini 2.5 Flash
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",  # Latest Gemini 2.5 Flash model
            generation_config={
                "temperature": 0.3,  # Lower temperature for more consistent medical explanations
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 500,  # Reasonable limit for explanations
                "response_mime_type": "text/plain",
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        logger.info("Gemini AI service initialized successfully")
    
    async def generate_mapping_explanation(
        self,
        source_code: str,
        source_display: str,
        target_code: str,
        target_display: str,
        language: str = "en",
        source_system: str = "NAMASTE",
        target_system: str = "ICD-11"
    ) -> Optional[str]:
        """
        Generate a multilingual explanation for a code mapping
        
        Args:
            source_code: Source code (e.g., NAM-1001)
            source_display: Source code display name (e.g., "Pandu")
            target_code: Target code (e.g., "DB64.0") 
            target_display: Target code display name (e.g., "Iron deficiency anaemia")
            language: Target language code (ISO 639-1/639-3)
            source_system: Source terminology system name
            target_system: Target terminology system name
            
        Returns:
            Generated explanation or None if generation fails
        """
        try:
            # Build the prompt for medical mapping explanation
            prompt = self._build_explanation_prompt(
                source_code, source_display, target_code, target_display,
                language, source_system, target_system
            )
            
            logger.debug(f"Generating explanation for {source_code} -> {target_code} in language: {language}")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                explanation = response.text.strip()
                logger.info(f"Successfully generated explanation in {language}")
                return explanation
            else:
                logger.warning("Empty response from Gemini API")
                return None
                
        except Exception as e:
            logger.error(f"Error generating AI explanation: {str(e)}")
            return None
    
    def _build_explanation_prompt(
        self,
        source_code: str,
        source_display: str,
        target_code: str,
        target_display: str,
        language: str,
        source_system: str,
        target_system: str
    ) -> str:
        """Build the prompt for generating mapping explanations"""
        
        # Language name mapping for better context
        language_names = {
            "hi": "Hindi",
            "ta": "Tamil", 
            "te": "Telugu",
            "bn": "Bengali",
            "gu": "Gujarati",
            "kn": "Kannada",
            "ml": "Malayalam",
            "mr": "Marathi",
            "pa": "Punjabi",
            "or": "Odia",
            "as": "Assamese",
            "sa": "Sanskrit",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ar": "Arabic"
        }
        
        lang_name = language_names.get(language, language)
        
        prompt = f"""
You are a medical terminology expert specializing in traditional medicine and modern healthcare coding systems.

Task: Explain the medical relationship between a {source_system} code and its corresponding {target_system} code in {lang_name}.

Source Code: {source_code} - "{source_display}"
Target Code: {target_code} - "{target_display}"

Guidelines:
1. Write a clear, concise explanation (2-3 sentences maximum)
2. Focus on the medical/clinical connection between the concepts
3. Use terminology appropriate for healthcare professionals
4. If traditional medicine terms are involved, briefly explain the concept
5. Maintain medical accuracy and cultural sensitivity
6. Write entirely in {lang_name}

Example format:
"[Source concept] is a traditional medicine term that corresponds to [target concept] because [brief medical explanation]."

Generate the explanation now:
"""
        
        return prompt.strip()
    
    def test_connection(self) -> bool:
        """Test if the AI service is working properly"""
        try:
            test_response = self.model.generate_content("Test connection. Respond with 'OK'.")
            return test_response and "OK" in test_response.text
        except Exception as e:
            logger.error(f"AI service connection test failed: {str(e)}")
            return False


# Language code validation
SUPPORTED_LANGUAGES = {
    "en", "hi", "ta", "te", "bn", "gu", "kn", "ml", "mr", "pa", 
    "or", "as", "sa", "es", "fr", "de", "zh", "ja", "ar", "ru",
    "pt", "it", "nl", "sv", "no", "da", "fi", "pl", "tr", "he"
}


def validate_language_code(language: str) -> bool:
    """Validate if the language code is supported"""
    return language.lower() in SUPPORTED_LANGUAGES


# Singleton instance
_ai_service_instance: Optional[GeminiAIService] = None


def get_ai_service() -> GeminiAIService:
    """Get or create the AI service singleton instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = GeminiAIService()
    return _ai_service_instance
