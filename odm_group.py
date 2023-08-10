from pathlib import Path
import subprocess as sp
import argparse
import json
parser = argparse.ArgumentParser()
parser.add_argument("uid_key")
args = parser.parse_args()

output = Path(f"../tmp_group_split/{args.uid_key}/images")
status = Path(f"{output.parent}/status.json")
prev_status = json.loads(status.read_text())
print("running anyways regardless of status")
#if prev_status.get("odm_processed",-1) ==-1:
sp.run(f"./kickoff_odm.sh {args.uid_key}",shell=True)
# if we reach this point we should update the status of the group
prev_status["odm_processed"]="complete"
status.write_text(json.dumps(prev_status))
