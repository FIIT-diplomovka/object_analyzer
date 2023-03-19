import os
import json
import logging
from .metadata_utilities import Droid, Tika

class MetadataExtractor:
    EMPTY_DCM = "./static/empty_dublin_core.json"

    def extract_sample(self, file_path):
        with open(MetadataExtractor.EMPTY_DCM) as f:
            dcm = json.load(f)
        return dcm

    def extract_using_droid(self, file_path):
        logging.info("Starting DROID extraction...")
        droid = Droid()
        dcm = droid.extract_metadata_dc(file_path)
        return dcm
    
    def extract_using_tika(self, file_path):
        logging.info("Starting TIKA extraction...")
        tika = Tika()
        dcm = tika.extract_metadata_dc(file_path)
        return dcm