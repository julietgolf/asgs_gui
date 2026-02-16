from pathlib import Path
import json


#config_dir = Path.home() / ".config" / "asgs"
#config_file = config_dir / "asgs_settings.json"
#
#if not config_file.exists():
#    config_dir.mkdir(parents=True, exist_ok=True)
#    ASGS_SETTINGS={}
#    
#else:
#    with open(config_file) as file:
#        ASGS_SETTINGS=json.load(file)
#
#if "ASGS_HOME" not in ASGS_SETTINGS:
#    ASGS_SETTINGS["ASGS_HOME"]=input("Enter ASGS_HOME: ")
#
#    with open(config_file,"w") as file:
#        json.dump(ASGS_SETTINGS,file,indent=4) 