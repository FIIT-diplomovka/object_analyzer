import os
import json
from .metadata_utilities import Droid

class MetadataExtractor:
    EMPTY_DCM = "./static/empty_dublin_core.json"

    def extract_sample(self, file_path):
        with open(MetadataExtractor.EMPTY_DCM) as f:
            dcm = json.load(f)
        return dcm

    def extract_using_droid(self, file_path):
        droid = Droid()
        dcm = droid.extract_metadata(file_path)
        return dcm