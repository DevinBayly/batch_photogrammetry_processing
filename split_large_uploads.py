import uuid
from datetime import datetime
import subprocess as sp
from pathlib import Path
import yaml


status= yaml.safe_load(sorted(Path().glob("status*.yaml"))[-1].read_text())["flight_status"]
pairings = {}
for f_key,f_data in status.items():
  image_count = f_data.get("number_images",-1)
  ## check to see if there's contents in the folder named split_up
  if image_count != -1 and image_count >1000:
    ## get the images and chunk into 500s` 
    jpgs = sorted(Path(f"../tmp/{f_key}/images/").glob("*JPG"))
    chunks = len(jpgs)//500
    for i in range(chunks):
      # maek a new tmp uid folder
      key = uuid.uuid4()
      dest_fldr = Path(f"../tmp/split_{key}/images")
      print("making folder",dest_fldr)
      dest_fldr.mkdir(exist_ok=True,parents=True)
      # get a newline delimited set of the images
      end = (i+1)*500
      if end > len(jpgs):
        jpgs_subset =jpgs[i*500:]
      else:
        jpgs_subset = jpgs[i*500:end]
      pths = "\n".join([str(jpg.name) for jpg in jpgs_subset])
      Path("rsync_file_list").write_text(pths)
      
      cmd = f"rsync -azP --files-from=rsync_file_list {jpgs[0].parent} {dest_fldr}"
      print(cmd)
      sp.run(cmd,shell=True)

    
