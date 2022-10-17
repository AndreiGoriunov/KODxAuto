from lib.kodxauto import KODxAuto
import json

def run(file_path):
    kodxauto = KODxAuto(file_path)
    print(json.dumps(kodxauto._steps))
    kodxauto.start()
