from dotenv import load_dotenv
from utilities.object_storage_connector import ObjectStorage
from utilities.metadata_extractor import MetadataExtractor
from utilities.postgres_connector import Postgres
from utilities.malware_analysis import MalwareAnalysis
import os
import logging
if os.path.exists("./.env"):
    load_dotenv()
from kafka import KafkaConsumer
import json


mc = ObjectStorage()
postgres = Postgres()

if not mc.is_connected():
    exit(1)

consumer = KafkaConsumer("NEW_ENTRY", bootstrap_servers=os.environ.get("KAFKA_URL"))
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
logging.info("Listening for Kafka events...")
for msg in consumer:
    try:
        data = json.loads(msg.value.decode("utf-8"))
        logging.info("Consuming " + data["path"])
        path = mc.save_object(data["bucket"], data["path"])
        extractor = MetadataExtractor()
        metadata = extractor.extract_using_droid(path) if data["method"] == "droid" else extractor.extract_using_tika(path)
        logging.info(metadata)
        metadata["stage"] = "done"
        # check if malware analysis is possible
        if MalwareAnalysis.is_analysis_supported(path):
            logging.info("Malware analysis available, starting...")
            malware = MalwareAnalysis()
            result = malware.is_malware_using_tika(path)
            logging.info("Malware analysis done.")
            if result != None:
                metadata["malware"] = result
            else:
                metadata["malware"] = "unsupported"
        else:
            metadata["malware"] = "unsupported"
        logging.info(postgres.update_metadata(data["bucket"], data["path"], metadata))
        os.remove(path)
        logging.info("Done.")
    except Exception as e:
        logging.error(e)
        continue