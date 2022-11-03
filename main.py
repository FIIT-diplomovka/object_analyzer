from dotenv import load_dotenv
import os
if os.path.exists("./.env"):
    load_dotenv()
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer("NEW_ENTRY", bootstrap_servers=os.environ.get("KAFKA_URL"))

for msg in consumer:
    data = json.loads(msg.value.decode("utf-8"))
    print(json.dumps(data, indent=4))