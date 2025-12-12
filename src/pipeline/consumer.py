import json
import requests
from kafka import KafkaConsumer
import colorama
from colorama import Fore, Style

# Initialize colors for terminal output
colorama.init()

# Configuration
KAFKA_TOPIC = "network-traffic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:19092"
API_URL = "http://localhost:8005/predict"  # Your Dockerized API

print(f"{Fore.CYAN}🎧 Connecting to Redpanda topic: {KAFKA_TOPIC}...{Style.RESET_ALL}")

try:
    # 1. Connect to the stream
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',       # Start reading from NOW (ignore old messages)
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print(f"{Fore.GREEN}✅ Connected! Waiting for traffic...{Style.RESET_ALL}\n")

    # 2. Process messages in real-time
    for message in consumer:
        packet = message.value
        
        # Prepare data for API (it expects a list of features)
        # We need to extract the values from the dictionary in the correct order
        # (This relies on the dictionary maintaining insertion order, which works in Python 3.7+)
        features = list(packet.values())
        
        # Remove the 'Label' if it exists (the API doesn't want the answer, just the data)
        # The dataset has 79 columns, API expects 78 features
        if len(features) > 78:
            features = features[:-1] 

        payload = {"features": features}

        try:
            # 3. Send to AI Brain (API)
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                confidence = result['confidence']
                
                # 4. Visualization
                if prediction == "BENIGN":
                    # Print normal traffic quietly
                    print(f"{Fore.GREEN}✓ Normal Traffic {Style.DIM}({confidence}){Style.RESET_ALL}", end='\r')
                else:
                    # SCREAM if it's an attack
                    print(f"\n{Fore.RED}🚨 ALERT: {prediction} DETECTED! [Confidence: {confidence}]{Style.RESET_ALL}")
                    print(f"   Payload Sample: {features[:5]}...")
            
            else:
                print(f"{Fore.YELLOW}⚠️ API Error: {response.status_code}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ API Connection Failed: {e}{Style.RESET_ALL}")

except KeyboardInterrupt:
    print(f"\n{Fore.YELLOW}🛑 Monitoring stopped.{Style.RESET_ALL}")