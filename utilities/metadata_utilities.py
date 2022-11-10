import os
import csv
import json
import subprocess

class Droid():
    DC_TO_DROID_MAP = "static/dublin_core_to_droid_map.json"
    DROID_RUNNABLE = "droid.bat" if os.name == "nt" else "droid.sh"
    OS_DELIMITER = "\\" if os.name == "nt" else "/"
    DROID_DIR = "analysis" + OS_DELIMITER + "droid"
    TEMP_DIR = "analysis" + OS_DELIMITER + "temp"

    def extract_metadata(self, file_path):
        file_path = file_path.replace("/", Droid.OS_DELIMITER)
        file_name= file_path.split(Droid.OS_DELIMITER)[-1]
        temp_profile = Droid.TEMP_DIR + Droid.OS_DELIMITER + "profile-" + file_name + ".droid"
        initial_csv = Droid.TEMP_DIR + Droid.OS_DELIMITER + "intialcsv-" + file_name + ".csv"
        droid_run = Droid.DROID_DIR + Droid.OS_DELIMITER + Droid.DROID_RUNNABLE
        droid = subprocess.run([droid_run, "-a", file_path, "-p", temp_profile], capture_output=True, text=True)
        print("Initial profile done..")
        if not droid.returncode == 0:
            print("Error during the initial profiling:")
            print(droid.stderr)
            return
        droid = subprocess.run([droid_run, "-e", initial_csv, "-p", temp_profile], capture_output=True, text=True)
        print("CSV creation done")
        if not droid.returncode == 0:
            print("Error during CSV generation:")
            print(droid.stderr)
            return
        with open(initial_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            temp_list = list(reader)
            metadata = temp_list[0]
        dc_map = json.load(open(Droid.DC_TO_DROID_MAP))
        dc = {}
        for key in dc_map:
            if dc_map[key] != "" and dc_map[key] in metadata and metadata[dc_map[key]] != "":
                dc[key] = metadata[dc_map[key]]
            else:
                dc[key] = ""
        os.remove(initial_csv)
        os.remove(temp_profile)
        os.remove(file_path)
        
        
        return dc
        
        