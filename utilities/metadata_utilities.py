import os
import csv
import json
import logging
import hashlib
import subprocess

class Droid():
    DC_TO_DROID_MAP = "static/dublin_core_to_droid_map.json"
    DROID_RUNNABLE = "droid.bat" if os.name == "nt" else "droid.sh"
    OS_DELIMITER = "\\" if os.name == "nt" else "/"
    DROID_DIR = "analysis" + OS_DELIMITER + "droid"
    TEMP_DIR = "analysis" + OS_DELIMITER + "temp"

    # returns "raw" output from droid formatted as a dictionary
    def get_json_analysis(self, file_path):
        file_path = file_path.replace("/", Droid.OS_DELIMITER)
        file_name= file_path.split(Droid.OS_DELIMITER)[-1]
        temp_profile = Droid.TEMP_DIR + Droid.OS_DELIMITER + "profile-" + file_name + ".droid"
        initial_csv = Droid.TEMP_DIR + Droid.OS_DELIMITER + "intialcsv-" + file_name + ".csv"
        droid_run = Droid.DROID_DIR + Droid.OS_DELIMITER + Droid.DROID_RUNNABLE
        droid = subprocess.run([droid_run, "-a", file_path, "-p", temp_profile], capture_output=True, text=True)
        logging.info("Initial profile done..")
        if not droid.returncode == 0:
            logging.error("Error during the initial profiling:")
            logging.error(droid.stderr)
            return None
        droid = subprocess.run([droid_run, "-e", initial_csv, "-p", temp_profile], capture_output=True, text=True)
        logging.info("CSV creation done")
        if not droid.returncode == 0:
            logging.error("Error during CSV generation:")
            logging.error(droid.stderr)
            return None
        with open(initial_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            temp_list = list(reader)
            metadata = temp_list[0]
        os.remove(initial_csv)
        os.remove(temp_profile)
        return metadata

    def extract_metadata_dc(self, file_path):
        metadata = self.get_json_analysis(file_path)
        dc_map = json.load(open(Droid.DC_TO_DROID_MAP))
        dc = {}
        for key in dc_map:
            if dc_map[key] != "" and dc_map[key] in metadata and metadata[dc_map[key]] != "":
                dc[key] = metadata[dc_map[key]]
            else:
                dc[key] = ""
        # get SHA-256
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            dc["sha_256"] = sha256_hash.hexdigest()
        return dc
        


class Tika():
    DC_TO_TIKA_MAP = "static/dublin_core_to_tika_map.json"
    OS_DELIMITER = "\\" if os.name == "nt" else "/" 
    TIKA_JAR = "analysis" + OS_DELIMITER + "tika" + OS_DELIMITER + "tika-app-2.5.0.jar"


    def get_json_analysis(self, file_path):
        tika = subprocess.run(["java", "-jar", Tika.TIKA_JAR,
                      "--json", file_path], capture_output=True, text=True)
        if not tika.returncode == 0:
            return None
        metadata = json.loads(tika.stdout)
        return metadata

    def extract_metadata_dc(self, file_path):
        metadata = self.get_json_analysis(file_path)
        if metadata is None:
            return None
        dc_map = json.load(open(Tika.DC_TO_TIKA_MAP))
        dc = {}
        for key in dc_map:
            for tika_key in dc_map[key]:
                if tika_key != "" and tika_key in metadata:
                    dc[key] = metadata[tika_key]
                    break
            if key not in dc:
                dc[key] = ""
        # get SHA-256
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            dc["sha_256"] = sha256_hash.hexdigest()
        
        return dc
        