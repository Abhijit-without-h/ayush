"""
Test script for AyushBridge API endpoints
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful")
            print(f"   Version: {data['version']}")
            print(f"   Status: {data['status']}")
            print(f"   Components: {data['components']}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_statistics_endpoint():
    """Test the statistics endpoint"""
    print("\n📊 Testing statistics endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics retrieved successfully")
            print(f"   Total mappings: {data['total_mappings']}")
            print(f"   Traditional systems: {data['by_traditional_system']}")
            print(f"   Equivalence types: {data['by_equivalence']}")
        else:
            print(f"❌ Statistics failed: {response.text}")
    except Exception as e:
        print(f"❌ Statistics endpoint error: {e}")

def test_search_endpoint():
    """Test the search endpoint with expanded diseases"""
    print("\n🔍 Testing search endpoint...")
    
    # Test multiple search queries
    search_queries = ["diabetes", "fever", "headache", "skin", "arthritis", "cough"]
    
    for query in search_queries:
        try:
            response = requests.get(f"{BASE_URL}/search?q={query}&limit=5")
            print(f"Search '{query}' - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Found {data['total_results']} results")
                for result in data['results'][:2]:  # Show first 2 results
                    print(f"     - {result['namaste_code']}: {result['namaste_display']} ({result['namaste_system']}) -> {result['icd11_display']}")
            else:
                print(f"   ❌ Search failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Search endpoint error: {e}")
        print()  # Blank line between searches

def test_translate_endpoint():
    """Test the translate endpoint"""
    print("\n🌐 Testing translate endpoint...")
    try:
        # Test NAMASTE to ICD-11 translation
        test_data = {
            "code": "NAM-1001",
            "system": "http://namaste.gov.in/fhir/CodeSystem/namaste",
            "target_system": "http://id.who.int/icd11/mms"
        }
        
        response = requests.post(
            f"{BASE_URL}/translate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Translation successful")
            print(f"   Resource Type: {data['resourceType']}")
            
            # Find result parameter
            result_param = next((p for p in data['parameter'] if p['name'] == 'result'), None)
            if result_param:
                print(f"   Translation Result: {result_param['valueBoolean']}")
            
            # Find match parameter
            match_param = next((p for p in data['parameter'] if p['name'] == 'match'), None)
            if match_param and match_param.get('part'):
                for part in match_param['part']:
                    if part['name'] == 'concept' and 'valueCoding' in part:
                        coding = part['valueCoding']
                        print(f"   Translated to: {coding['code']} - {coding['display']}")
        else:
            print(f"❌ Translation failed: {response.text}")
    except Exception as e:
        print(f"❌ Translation endpoint error: {e}")

def test_concept_map_endpoint():
    """Test the ConceptMap endpoint"""
    print("\n🗺️  Testing ConceptMap endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/ConceptMap/namaste-to-icd11")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ConceptMap retrieved successfully")
            print(f"   Resource Type: {data['resourceType']}")
            print(f"   Name: {data['name']}")
            print(f"   Title: {data['title']}")
            print(f"   Groups: {len(data['group'])}")
            if data['group']:
                elements = data['group'][0].get('element', [])
                print(f"   Mappings: {len(elements)}")
        else:
            print(f"❌ ConceptMap failed: {response.text}")
    except Exception as e:
        print(f"❌ ConceptMap endpoint error: {e}")

def test_disease_analysis_endpoint():
    """Test the disease analysis endpoint"""
    print("\n🧠 Testing Disease Analysis endpoint...")
    
    # Test conditions with different traditional systems and enhanced multilingual support
    test_cases = [
        {"condition": "diabetes", "system": "Ayurveda", "language": "hi", "desc": "Hindi (हिन्दी)"},
        {"condition": "fever", "system": "Siddha", "language": "ta", "desc": "Tamil (தமிழ்)"},
        {"condition": "headache", "system": "Unani", "language": "ur", "desc": "Urdu (اردو)"},
        {"condition": "arthritis", "system": "Ayurveda", "language": "en", "desc": "English"},
        {"condition": "asthma", "system": "Siddha", "language": "bn", "desc": "Bengali (বাংলা)"}
    ]
    
    for test_case in test_cases:
        try:
            params = {
                "condition": test_case["condition"],
                "traditional_system": test_case["system"],
                "language": test_case["language"],
                "include_medications": True
            }
            
            response = requests.post(f"{BASE_URL}/analyze", params=params)
            print(f"Analysis '{test_case['condition']}' ({test_case['system']}) in {test_case['desc']} - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Analysis generated successfully")
                print(f"   Condition: {data['condition']}")
                print(f"   System: {data['traditional_system']}")
                print(f"   Has AI Analysis: {data['has_ai_analysis']}")
                print(f"   Related mappings: {data['total_related_codes']}")
                
                if data.get('ai_analysis') and len(data['ai_analysis']) > 100:
                    # Show first 200 characters of analysis
                    preview = data['ai_analysis'][:200] + "..." if len(data['ai_analysis']) > 200 else data['ai_analysis']
                    print(f"   Analysis preview: {preview}")
                
                # Show related mappings
                if data.get('related_mappings'):
                    print(f"   Related codes found:")
                    for mapping in data['related_mappings'][:2]:
                        print(f"     - {mapping['namaste_code']}: {mapping['namaste_display']}")
                        
            else:
                print(f"   ❌ Analysis failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Disease analysis error: {e}")
        print()  # Blank line between tests

def main():
    """Run all endpoint tests"""
    print("🚀 Starting AyushBridge API Tests")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    test_health_endpoint()
    test_statistics_endpoint()
    test_search_endpoint()
    test_translate_endpoint()
    test_concept_map_endpoint()
    test_disease_analysis_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main()
