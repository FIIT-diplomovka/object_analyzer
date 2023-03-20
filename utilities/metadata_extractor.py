import os
import json
import logging
import openai
from .metadata_utilities import Droid, Tika



class MetadataExtractor:
    EMPTY_DCM = "./static/empty_dublin_core.json"

    def extract_sample(self, file_path):
        with open(MetadataExtractor.EMPTY_DCM) as f:
            dcm = json.load(f)
        return dcm
        

    def extract_using_droid(self, file_path, use_gpt3=False):
        logging.info("Starting DROID extraction...")
        droid = Droid()
        if use_gpt3:
            metadata = droid.get_json_analysis(file_path)
            return self._extract_using_gpt3(metadata)
        dcm = droid.extract_metadata_dc(file_path)
        return dcm
    
    def extract_using_tika(self, file_path, use_gpt3=False):
        logging.info("Starting TIKA extraction...")
        tika = Tika()
        if use_gpt3:
            metadata = tika.get_json_analysis(file_path)
            return self._extract_using_gpt3(metadata)
        dcm = tika.extract_metadata_dc(file_path)
        return dcm


    def _extract_using_gpt3(self, metadata):
        openai.organization = os.environ.get("ORGANIZATION_ID")
        openai.api_key = os.environ.get("API_KEY")
        logging.warning("USING GPT3 FOR METADATA EXTRACTION")
        gpt3_dc_output = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", timeout=20,
                messages=[
                    {"role": "system", "content": 'Every message user sends will contains file metadata in JSON format. You will then try to use this metadata to fill dublin core elements as best as you can. If you cannot assign a value to a dublin core element, simply leave it empty. Never output anything else than Dublin core in JSON format. Example output:  {     "DCM_contributor": "Dominik Horvath",     "DCM_coverage": "",     "DCM_creator": "Jana Strbova",     "DCM_date": "",     "DCM_description": "Sample description of a file",     "DCM_format": "",     "DCM_identifier": "",     "DCM_language": "english",     "DCM_publisher": "",     "DCM_relation": "",     "DCM_rights": "",     "DCM_source": "",     "DCM_subject": "",     "DCM_title": "Document title",     "DCM_type": "" }'},
                    {"role": "user", "content": json.dumps(metadata, ensure_ascii=False)}
                ]
        )
        return json.loads(gpt3_dc_output['choices'][0]['message']['content'])