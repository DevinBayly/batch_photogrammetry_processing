from pathlib import Path
import argparse
import json
parser = argparse.ArgumentParser()
parser.add_argument("uid_key")
args = parser.parse_args()
groups = json.loads(Path("../split_groups_missing.json").read_text())
if groups.get(args.uid_key,-1) !=-1:
  images = groups[args.uid_key]["images"]

  # each element in the images list has several parts
  # first is the full path
  # second is just the name
  # third is the parent 

  # we are going to iterate over them and link them to the images folder in a newly created processing directory
  output = Path(f"../tmp_group_split/{args.uid_key}/images")
  output.mkdir(exist_ok=True,parents=True)
  status = Path(f"{output.parent}/status.json")
  if not status.exists():
    # In [4]: Path('link-to-textfile.txt').symlink_to(Path('textfile.txt'))
    for im in images:
      # get the name
      
      name = im[1]
      abs_path = Path(im[0])
      dest_path = Path(f"{output}/{name}.JPG")
      ## check if image exists, if so continue
      if dest_path.exists():
        print("already linked",dest_path)
        continue
      dest_path.symlink_to(abs_path)
      print("linked",abs_path,"tp",dest_path)
      
    # add to the status at the end 
    status.write_text(json.dumps({"symlink":"complete"}))



