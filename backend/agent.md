# 🌉 AyushBridge: FHIR Terminology Microservice

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![FHIR R4](https://img.shields.io/badge/FHIR_R4-004B87?style=for-the-badge&logo=hl7)](https://www.hl7.org/fhir/)
[![AI Powered](https://img.shields.io/badge/AI_Powered-4285F4?style=for-the-badge&logo=artificial-intelligence)](https://ai.google.dev/gemini-api)

**AyushBridge** is a FHIR R4-compliant microservice that bridges India's traditional AYUSH medicine with the global healthcare ecosystem. It provides real-time, bidirectional mapping between **NAMASTE codes** (Ayurveda, Siddha, Unani) and **ICD-11**, powered by AI for multilingual explanations and clinician support.

> "The 2025 ICD-11 update significantly advances the global integration of traditional medicine, including Ayurveda, Siddha, and Unani" .

---

## 🌟 Features

- **FHIR R4 `ConceptMap` & `Translate` Endpoints**: Standardized, interoperable API for EMR integration.
- **Bidirectional Mapping**: Translate NAMASTE ↔ ICD-11 codes in real-time.
- **AI-Powered Explanations**: Uses advanced AI technology to generate multilingual, clinician-friendly explanations of mappings.
- **Multilingual Support**: Get responses in Hindi, Tamil, Bengali, and 100+ languages.
- **Auto-Generated OpenAPI/Swagger Docs**: Interactive, testable documentation out-of-the-box .
- **Immutable Audit Logs**: Every translation is stored as a FHIR `Provenance` resource for compliance.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A [Google AI Studio API Key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/ayushbridge.git
cd ayushbridge

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`.

- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI) 
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

---

## 📚 API Endpoints

### 1. Translate a Code (`POST /translate`)

Translate a code from one system to another.

**Request Body (JSON)**
```json
{
  "code": "NAM-1001",
  "system": "http://namaste.gov.in/fhir/CodeSystem/namaste",
  "target_system": "http://id.who.int/icd11/mms",
  "language": "hi" // Optional: for AI explanation language
}
```

**Success Response (200)**
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": true
    },
    {
      "name": "match",
      "part": [
        {
          "name": "equivalence",
          "valueCode": "equivalent"
        },
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
      "valueString": "पाण्डु रोग आयुर्वेद में रक्त की कमी की स्थिति है, जो आयरन की कमी से होती है।"
    }
  ]
}
```

### 2. Get ConceptMap (`GET /ConceptMap/{id}`)

Retrieve a pre-defined FHIR `ConceptMap` resource for bulk operations .

**Response**
```json
{
  "resourceType": "ConceptMap",
  "id": "namaste-to-icd11",
  "url": "http://ayushbridge.org/fhir/ConceptMap/namaste-to-icd11",
  "name": "NAMASTEtoICD11",
  "title": "Mapping from NAMASTE to ICD-11",
  "status": "active",
  "group": [
    {
      "source": "http://namaste.gov.in/fhir/CodeSystem/namaste",
      "target": "http://id.who.int/icd11/mms",
      "element": [
        {
          "code": "NAM-1001",
          "display": "Pandu",
          "target": [
            {
              "code": "DB64.0",
              "display": "Iron deficiency anaemia",
              "equivalence": "equivalent"
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 🧠 How It Works

### The Mapping Engine
The core is a rule-based mapper using a local JSON file (`mappings/namaste_icd11_mappings.json`) that contains the official mappings from the **2025 ICD-11 update** [[26], [31]].

### AI-Powered Explanations
When a `language` parameter is provided, the service calls an advanced AI service to generate a clear, multilingual explanation of the mapping.

```python
# AI service integration for multilingual explanations
prompt = f"Explain the medical link between '{source_display}' and '{target_display}' in {language}."
response = ai_service.generate_content(prompt)
```

This leverages advanced AI technology to generate text from simple prompts in multiple languages.

### FHIR Compliance
All responses are valid FHIR R4 resources (`Parameters`, `ConceptMap`), ensuring seamless integration with any FHIR-compliant EMR or the ABDM network .

---

## 📂 Project Structure

```
ayushbridge/
├── main.py                 # FastAPI app entry point
├── models.py               # Pydantic models for request/response
├── fhir_resources.py       # FHIR resource builders (ConceptMap, Parameters)
├── mapping_engine.py       # Core logic for code translation
├── ai_service.py           # AI service integration for multilingual support
├── mappings/
│   └── namaste_icd11_mappings.json  # Official code mappings
├── requirements.txt
└── .env.example
```

---

## 🤝 Contributing

We welcome contributions! This project aims to operationalize the historic inclusion of AYUSH systems in ICD-11 . Please open an issue or PR to help expand the mapping database or improve the AI explanations.

---

## 📜 License

MIT License

---

## 🙏 Acknowledgements

- **Ministry of AYUSH, Government of India**: For the NAMASTE portal and standardized terminologies .
- **World Health Organization (WHO)**: For the landmark 2025 ICD-11 update .
- **HL7 International**: For the FHIR standard that makes interoperability possible.