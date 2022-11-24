from dotenv import load_dotenv
from utilities.object_storage_connector import ObjectStorage
from utilities.metadata_extractor import MetadataExtractor
import os
import logging
if os.path.exists("./.env"):
    load_dotenv()
from kafka import KafkaConsumer
import json


mc = ObjectStorage()

if not mc.is_connected():
    exit(1)

consumer = KafkaConsumer("NEW_ENTRY", bootstrap_servers=os.environ.get("KAFKA_URL"))
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
# TODO: use the database for updating the flag in the DB. if you dont do this, there is a race condition bug :(
logging.info("Listening for Kafka events...")
for msg in consumer:
    try:
        data = json.loads(msg.value.decode("utf-8"))
        logging.info("Consuming " + data["path"])
        path = mc.save_object(data["bucket"], data["path"])
        extractor = MetadataExtractor()
        metadata = extractor.extract_using_droid(path)
        metadata["stage"] = "done"
        mc.update_object_metadata(data["bucket"], data["path"], metadata)
        logging.info("Done.")
    except Exception as e:
        logging.info(e)
        continue