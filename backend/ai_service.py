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
            model_name="gemini-2.5-flash",  # Latest Gemini 2.5 Flash model
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
    
    async def generate_disease_analysis(
        self,
        condition_name: str,
        traditional_system: str = "Ayurveda",
        language: str = "en",
        include_medications: bool = True
    ) -> Optional[str]:
        """
        Generate comprehensive analysis for diseases and conditions
        
        Args:
            condition_name: Disease or condition name
            traditional_system: Traditional medicine system (Ayurveda, Siddha, Unani)
            language: Target language code
            include_medications: Whether to include medication information
            
        Returns:
            Comprehensive analysis or None if generation fails
        """
        try:
            prompt = self._build_disease_analysis_prompt(
                condition_name, traditional_system, language, include_medications
            )
            
            logger.debug(f"Generating disease analysis for '{condition_name}' in {traditional_system}")
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                analysis = response.text.strip()
                logger.info(f"Successfully generated disease analysis for {condition_name}")
                return analysis
            else:
                logger.warning("Empty response from AI service for disease analysis")
                return None
                
        except Exception as e:
            logger.error(f"Error generating disease analysis: {str(e)}")
            return None
    
    def _build_disease_analysis_prompt(
        self,
        condition_name: str,
        traditional_system: str,
        language: str,
        include_medications: bool
    ) -> str:
        """Build prompt for comprehensive multilingual disease analysis"""
        
        # Enhanced language mapping with native names and better coverage
        language_names = {
            "hi": "Hindi (हिन्दी)", "ta": "Tamil (தமிழ்)", "te": "Telugu (తెలుగు)", 
            "bn": "Bengali (বাংলা)", "gu": "Gujarati (ગુજરાતી)", "kn": "Kannada (ಕನ್ನಡ)", 
            "ml": "Malayalam (മലയാളം)", "mr": "Marathi (मराठी)", "pa": "Punjabi (ਪੰਜਾਬੀ)", 
            "or": "Odia (ଓଡ଼ିଆ)", "as": "Assamese (অসমীয়া)", "sa": "Sanskrit (संस्कृत)",
            "ur": "Urdu (اردو)", "ne": "Nepali (नेपाली)", "si": "Sinhala (සිංහල)",
            "en": "English", "es": "Spanish (Español)", "fr": "French (Français)", 
            "de": "German (Deutsch)", "zh": "Chinese (中文)", "ja": "Japanese (日本語)", 
            "ar": "Arabic (العربية)", "ru": "Russian (Русский)", "pt": "Portuguese (Português)", 
            "it": "Italian (Italiano)", "nl": "Dutch (Nederlands)", "tr": "Turkish (Türkçe)", 
            "ko": "Korean (한국어)", "th": "Thai (ไทย)", "vi": "Vietnamese (Tiếng Việt)",
            "my": "Myanmar (မြန်မာ)", "km": "Khmer (ខ្មែរ)", "lo": "Lao (ລາວ)"
        }
        
        lang_name = language_names.get(language, f"{language.upper()} language")
        
        # Traditional system names in various languages
        traditional_names = {
            "Ayurveda": {
                "hi": "आयुर्वेद", "sa": "आयुर्वेद", "bn": "আয়ুর্বেদ", 
                "te": "ఆయుర్వేదం", "ta": "ஆயுர்வேதம்", "kn": "ಆಯುರ್ವೇದ",
                "ml": "ആയുര്‍വേദം", "mr": "आयुर्वेद", "gu": "આયુર્વેદ",
                "or": "ଆୟୁର୍ବେଦ", "pa": "ਆਯੁਰਵੇਦ", "ne": "आयुर्वेद",
                "default": "Ayurveda"
            },
            "Siddha": {
                "ta": "சித்த மருத்துவம்", "te": "సిద్ధ వైద్య", "ml": "സിദ്ധ വൈദ്യം",
                "hi": "सिद्ध चिकित्सा", "kn": "ಸಿದ್ಧ ವೈದ್ಯ", "bn": "সিদ্ধ চিকিৎসা",
                "default": "Siddha Medicine"
            },
            "Unani": {
                "ur": "یونانی طب", "ar": "الطب اليوناني", "hi": "यूनानी चिकित्सा",
                "bn": "ইউনানি চিকিৎসা", "te": "యునాని వైద్యం", "ta": "யூனானி மருத்துவம்",
                "fa": "طب یونانی", "default": "Unani Medicine"
            }
        }
        
        traditional_name = traditional_names.get(traditional_system, {}).get(
            language, traditional_names.get(traditional_system, {}).get("default", traditional_system)
        )
        
        # Language-specific section headers
        section_headers = {
            "hi": {
                "understanding": f"{traditional_name} की समझ",
                "modern": "आधुनिक चिकित्सा दृष्टिकोण", 
                "pathology": "रोग की प्रक्रिया",
                "symptoms": "लक्षण और संकेत",
                "treatments": f"{traditional_name} में उपचार",
                "diet": "आहार संबंधी सुझाव",
                "lifestyle": "जीवनशैली में बदलाव",
                "prognosis": "पूर्वानुमान और प्रबंधन"
            },
            "ta": {
                "understanding": f"{traditional_name} புரிதல்",
                "modern": "நவீன மருத்துவ கண்ணோட்டம்",
                "pathology": "நோய் செயல்முறை", 
                "symptoms": "அறிகுறிகள் மற்றும் குறியீடுகள்",
                "treatments": f"{traditional_name} சிகிச்சை",
                "diet": "உணவு பரிந்துரைகள்",
                "lifestyle": "வாழ்க்கை முறை மாற்றங்கள்",
                "prognosis": "முன்னறிவிப்பு மற்றும் மேலாண்மை"
            },
            "bn": {
                "understanding": f"{traditional_name} বোঝাপড়া",
                "modern": "আধুনিক চিকিৎসা দৃষ্টিভঙ্গি",
                "pathology": "রোগের প্রক্রিয়া",
                "symptoms": "লক্ষণ ও চিহ্ন", 
                "treatments": f"{traditional_name} চিকিৎসা",
                "diet": "খাদ্য সুপারিশ",
                "lifestyle": "জীবনযাত্রার পরিবর্তন",
                "prognosis": "পূর্বাভাস ও ব্যবস্থাপনা"
            },
            "default": {
                "understanding": f"{traditional_system} Understanding",
                "modern": "Modern Medical Perspective",
                "pathology": "Pathophysiology",
                "symptoms": "Symptoms & Signs",
                "treatments": f"{traditional_system} Treatments",
                "diet": "Dietary Recommendations", 
                "lifestyle": "Lifestyle Modifications",
                "prognosis": "Prognosis & Management"
            }
        }
        
        headers = section_headers.get(language, section_headers["default"])
        
        medication_section = ""
        if include_medications:
            medication_section = f"""
5. **{headers['treatments']}**: Traditional medicines, herbs, and therapeutic approaches
6. **{headers['diet']}**: Dietary guidelines according to {traditional_system}
7. **{headers['lifestyle']}**: Lifestyle changes recommended in {traditional_system}"""
        
        # Enhanced multilingual prompt with strong language enforcement
        prompt = f"""
You are a highly skilled medical practitioner with expertise in {traditional_system} ({traditional_name}) medicine and modern healthcare systems. You are fluent in {lang_name} and specialize in medical communication.

🔴 CRITICAL LANGUAGE REQUIREMENT: 
- Respond ENTIRELY in {lang_name} 
- Do NOT mix languages or use English unless specifically requested
- Use appropriate medical terminology in {lang_name}
- All section headers, explanations, and content must be in {lang_name}

Task: Provide comprehensive medical analysis of "{condition_name}" integrating {traditional_system} and modern medical knowledge.

Structure your response in {lang_name} with these sections:

1. **{headers['understanding']}**: Traditional perspective on this condition
2. **{headers['modern']}**: Current medical understanding and classification  
3. **{headers['pathology']}**: Disease mechanisms from both viewpoints
4. **{headers['symptoms']}**: Clinical manifestations and diagnostic signs{medication_section}
8. **{headers['prognosis']}**: Treatment outcomes and long-term management

Response Requirements:
✓ Write completely in {lang_name}
✓ Use medical terminology appropriate for {lang_name}
✓ Maintain professional healthcare tone in {lang_name}
✓ Include cultural context for traditional medicine concepts
✓ Provide evidence-based information
✓ 700-1000 words in {lang_name}
✓ Be comprehensive yet accessible

Condition: "{condition_name}"
Medical System: {traditional_system} ({traditional_name})
Language: {lang_name}

Begin detailed analysis in {lang_name}:
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


# Enhanced language code validation - Supporting 50+ languages
SUPPORTED_LANGUAGES = {
    # Indian Languages
    "hi", "ta", "te", "bn", "gu", "kn", "ml", "mr", "pa", "or", "as", "sa", "ur", "ne", "si",
    # International Languages  
    "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ar", "ko", "tr", "nl", "sv", "no", 
    "da", "fi", "pl", "cs", "hu", "ro", "bg", "hr", "sk", "sl", "et", "lv", "lt", "he", "th",
    "vi", "id", "ms", "tl", "my", "km", "lo", "ka", "am", "sw", "zu", "af", "is", "mt", "cy"
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
