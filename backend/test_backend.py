"""
Test script to verify backend functionality
Run: python test_backend.py
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_chat_flow():
    print("\nTesting chat flow...")
    
    # Create chat job
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={"message": "What is artificial intelligence?"}
    )
    assert response.status_code == 200
    data = response.json()
    job_id = data["job_id"]
    print(f"✓ Job created: {job_id}")
    
    # Stream response
    print("✓ Streaming response...")
    url = f"{BASE_URL}/api/chat/stream/{job_id}"
    response = requests.get(url, stream=True)
    
    event_count = 0
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                event = json.loads(line[6:])
                event_count += 1
                print(f"  Event {event_count}: {event['type']}")
                if event['type'] == 'done':
                    break
    
    print(f"✓ Received {event_count} events")

def test_pdf_list():
    print("\nTesting PDF list...")
    response = requests.get(f"{BASE_URL}/api/pdf")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Found {len(data['documents'])} PDFs")
    for doc in data['documents']:
        print(f"  - {doc}")

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Test Suite")
    print("=" * 50)
    
    try:
        test_health()
        test_chat_flow()
        test_pdf_list()
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        print("\nMake sure backend is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
