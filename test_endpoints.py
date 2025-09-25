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
    """Test the search endpoint"""
    print("\n🔍 Testing search endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/search?q=diabetes&limit=3")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful")
            print(f"   Query: {data['query']}")
            print(f"   Total results: {data['total_results']}")
            print(f"   Results returned: {data['returned_results']}")
            for result in data['results']:
                print(f"   - {result['namaste_code']}: {result['namaste_display']} -> {result['icd11_display']}")
        else:
            print(f"❌ Search failed: {response.text}")
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")

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
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main()
