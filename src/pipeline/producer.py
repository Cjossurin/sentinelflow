import pandas as pd
import json
import time
import random
from kafka import KafkaProducer
import os

# Configuration
KAFKA_TOPIC = "network-traffic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:19092"  # External port for Redpanda
DATA_FILE = "../../data/MachineLearningCSV/MachineLearningCVE/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

# 1. Initialize the Producer
print(f"🔌 Connecting to Redpanda at {KAFKA_BOOTSTRAP_SERVERS}...")
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')  # Turn data into JSON bytes
    )
    print("✅ Connected to Redpanda!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# 2. Load the Dataset (Friday - DDoS)
print(f"\n📂 Loading data from {DATA_FILE}...")
# Get absolute path to handle running from different directories
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, DATA_FILE)

try:
    df = pd.read_csv(file_path)
    # Clean column names immediately
    df.columns = df.columns.str.strip()
    print(f"📊 Loaded {len(df):,} records.")
except FileNotFoundError:
    print("❌ File not found! Check your path.")
    exit()

# 3. Simulate Streaming
print("\n🚀 Starting stream... (Press Ctrl+C to stop)")

try:
    # Shuffle data to mix normal traffic with attacks
    df_shuffled = df.sample(frac=1).reset_index(drop=True)
    
    for index, row in df_shuffled.iterrows():
        # Convert row to dictionary
        record = row.to_dict()
        
        # Send to Redpanda
        producer.send(KAFKA_TOPIC, value=record)
        
        # Print progress every 1000 records
        if index % 1000 == 0:
            label = record.get('Label', 'Unknown')
            print(f"   Sent record #{index} | Type: {label}")
            
        # Simulate real-time delay (fast)
        # Remove this sleep if you want to blast data as fast as possible
        time.sleep(0.01) 

except KeyboardInterrupt:
    print("\n🛑 Stream stopped by user.")
finally:
    producer.close()