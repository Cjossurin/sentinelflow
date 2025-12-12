import requests
import json
import random

# The address of your local API
url = "http://127.0.0.1:8005/predict"

# Generate a fake network packet (78 random numbers)
# In the real world, this would come from a network sensor reading Wireshark data
fake_packet = [random.random() * 100 for _ in range(78)]

payload = {
    "features": fake_packet
}

print(f"📡 Sending mock network traffic to {url}...")

try:
    # Send the POST request
    response = requests.post(url, json=payload)
    
    # Check if it worked
    if response.status_code == 200:
        print("✅ Success! The API responded:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Failed with status code: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("Make sure your uvicorn server is still running in the other terminal!")