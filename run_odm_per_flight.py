from pathlib import Path
import subprocess as sp
import uuid

# first convert these all to be named images instead
imagefolders = sorted(Path("../").glob("*/images"))+sorted(Path("../").glob("*/*/images"))+sorted(Path("../").glob("*/*/*/images"))
#for fldr in outputfolders:
#  if "odm" in fldr.name:
#    continue
#  new_name = Path(f"{fldr.parent}/images")
#  fldr.rename(new_name)
#  imagefolders.append(new_name)
#
#print(imagefolders)


## here we fix the fact that there might be spaces in the names of the files
def remove_spaces_within_parents(pth):
  # split on the / and start with the first one and then gradually update the path so that we have the option to rename later parts
  parts = str(pth).split("/")
  new_pth= Path(parts[0])
  print("full path is",pth)
  for p in parts[1:]:
    print(new_pth,"starting out",p)
    if " " in p:
      new_name = p.replace(" ","_")
      og_pth= Path(f"{new_pth}/{p}")
      print("path that probably contains spce",og_pth)
      if og_pth.exists():
        og_pth.rename(f"{new_pth}/{new_name}")
        new_pth = Path(f"{new_pth}/{new_name}")
        print("new path after renaming",new_pth)
      else:
        break
    else:
      new_pth=Path(f"{new_pth}/{p}")
  

# check for spaces
for imfolder in imagefolders:
  if " " in str(imfolder):
    remove_spaces_within_parents(imfolder)


imagefolders = sorted(Path("../tmp").glob("*/images"))+sorted(Path("../tmp").glob("*/*/images"))+sorted(Path("../tmp").glob("*/*/*/images"))
print("fixed spaces",imagefolders)


for imagefldr in imagefolders[5:]:
  try:
    if "odm" in str(imagefldr.parent):
      continue
    if len(sorted(imagefldr.iterdir())) >10:
#      Path(f"{imagefldr.parent}/results").mkdir(exist_ok=True)
      cmd = f'sbatch -A cdh -p standard -t 24:00:00 -N 1 -n 16  odm_submit.sh "{imagefldr}" {imagefldr.parent.stem} "{imagefldr.absolute()}"'
      print(cmd)
      sp.run(cmd,shell=True)
  except:
    print("didn't start",imagefldr)
