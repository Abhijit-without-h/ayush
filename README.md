# 🌉 AyushBridge: FHIR Terminology Microservice

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![FHIR R4](https://img.shields.io/badge/FHIR_R4-004B87?style=for-the-badge&logo=hl7)](https://www.hl7.org/fhir/)
[![AI Powered](https://img.shields.io/badge/AI_Powered-4285F4?style=for-the-badge&logo=artificial-intelligence)](https://ai.google.dev/gemini-api)

**AyushBridge** is a FHIR R4-compliant microservice that bridges India's traditional AYUSH medicine with the global healthcare ecosystem. It provides real-time, bidirectional mapping between **NAMASTE codes** (Ayurveda, Siddha, Unani) and **ICD-11**, powered by AI for multilingual explanations and clinician support.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- An AI service API key for multilingual explanations

### Installation

```bash
# Clone and setup
git clone <your-repo-url>
cd ayushbridge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your AI service API key:
```env
GEMINI_API_KEY=your_ai_service_api_key_here
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📚 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/translate` | POST | Translate codes between NAMASTE and ICD-11 |
| `/ConceptMap/{id}` | GET | Retrieve FHIR ConceptMap resources |
| `/search` | GET | Search through available mappings |
| `/statistics` | GET | Get mapping statistics |
| `/health` | GET | Health check and system status |

### Example Usage

**Translate a NAMASTE code to ICD-11:**
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "NAM-1001",
    "system": "http://namaste.gov.in/fhir/CodeSystem/namaste",
    "target_system": "http://id.who.int/icd11/mms",
    "language": "hi"
  }'
```

**Get a ConceptMap:**
```bash
curl "http://localhost:8000/ConceptMap/namaste-to-icd11"
```

**Search mappings:**
```bash
curl "http://localhost:8000/search?q=diabetes&limit=5"
```

---

## 🧠 AI-Powered Explanations

AyushBridge uses advanced AI technology to generate multilingual medical explanations:

- **100+ Languages**: Hindi, Tamil, Bengali, English, and more
- **Medical Context**: Clinician-friendly explanations
- **Cultural Sensitivity**: Respectful handling of traditional medicine concepts

---

## 🏗️ Project Structure

```
ayushbridge/
├── main.py                 # FastAPI application
├── models.py               # Pydantic models for validation
├── fhir_resources.py       # FHIR resource builders
├── mapping_engine.py       # Core mapping logic
├── ai_service.py           # AI service integration
├── mappings/
│   └── namaste_icd11_mappings.json  # Code mappings data
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Development

### Code Quality
```bash
# Install development dependencies
pip install black isort flake8

# Format code
black .
isort .

# Lint code
flake8 .
```

### Testing
```bash
# Run tests (when implemented)
pytest

# Test specific endpoint
pytest tests/test_translate.py
```

---

## 📊 Sample Mappings

The service includes 15 sample mappings across traditional medicine systems:

| NAMASTE Code | Traditional System | ICD-11 Code | Condition |
|--------------|-------------------|-------------|-----------|
| NAM-1001 | Ayurveda | DB64.0 | Iron deficiency anaemia |
| NAM-2002 | Siddha | GA32.0 | Type 2 diabetes |
| NAM-3002 | Unani | GA31.0 | Type 1 diabetes |

---

## 🌍 FHIR Compliance

AyushBridge follows **FHIR R4** specifications:

- **ConceptMap**: For bulk mapping operations
- **Parameters**: For translate operation responses
- **Coding**: Standard code representation
- **OperationOutcome**: Error handling

---


---

## 🙏 Acknowledgements

- **Ministry of AYUSH, Government of India**: For NAMASTE standardization
- **World Health Organization**: For ICD-11 traditional medicine integration
- **HL7 International**: For FHIR standards
- **AI Technology Partners**: For advanced multilingual AI capabilities
