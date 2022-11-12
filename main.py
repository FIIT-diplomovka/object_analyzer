from dotenv import load_dotenv
from utilities.object_storage_connector import ObjectStorage
from utilities.metadata_extractor import MetadataExtractor
import os
import hashlib
if os.path.exists("./.env"):
    load_dotenv()
from kafka import KafkaConsumer
import json


mc = ObjectStorage()

if not mc.is_connected():
    exit(1)

consumer = KafkaConsumer("NEW_ENTRY", bootstrap_servers=os.environ.get("KAFKA_URL"))


print("Listening for Kafka events...")
for msg in consumer:
    data = json.loads(msg.value.decode("utf-8"))
    print("Consuming " + data["path"])
    path = mc.save_object(data["bucket"], data["path"])
    extractor = MetadataExtractor()
    metadata = extractor.extract_using_droid(path)
    metadata["stage"] = "done"
    mc.update_object_metadata(data["bucket"], data["path"], metadata)
    print("Done.")