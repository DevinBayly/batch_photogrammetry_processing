#!/usr/bin/python3
import sys
from pathlib import Path
from datetime import datetime
import yaml
import uuid
import json

high_level_status ={}

## first get all the outputs
all_gps_tagged_uploads = []
for pattern_mult in range(0,5):
    all_gps_tagged_uploads+=[str(f.parent) for f in Path("/xdisk/bryancarter/elliottc1").glob("*/"*pattern_mult +"OUTPUT")]



high_level_status["uploaded_gps_folders"]=all_gps_tagged_uploads.copy()
totals={}
high_level_status["totals"]=totals
totals["total_gps_folders"]=len(all_gps_tagged_uploads)
## calculate the number of images in the entire collection of output folders
totals["total_images_total"] = sum([len(sorted(Path(f"{fldr}/OUTPUT/").glob("*JPG"))) for fldr in all_gps_tagged_uploads])
print(all_gps_tagged_uploads)
## then get folder names from tmp
tmp_folders = [f.stem for f in Path("../tmp").iterdir()]
print(tmp_folders)
## then go through all the pairings files
pairings_files = sorted(Path().glob("pairings*"))
## remove all the keys that are folders in tmp
print(len(tmp_folders),"before removing a number of folder entries")

flight_level_status={}

for pairing_file in pairings_files:
  pairings = json.loads(open(pairing_file).read())
  for key in pairings:
    print(key)
    try:
      ind = tmp_folders.index(key)

      images = sorted(Path(f"../tmp/{key}/images").glob("*JPG"))
      flight_level_status[tmp_folders.pop(ind)] ={
        "copied":"complete",
        "original_folder":pairings[key],
        "number_images":len(images)
    }
      
    except Exception as e:
      print(e)
      flight_level_status[key] ={
        "error":"random uuid without tmp folder to match",
      }


print(len(tmp_folders),"after removing pairings that have already been established")
print("remaining folders are",tmp_folders)
print(flight_level_status)
## then for each of the remaining folders in tmp
## go through the first image in each and compare to the first image in the remaining folders from the outputs


# a map that helps us match an image name to the upload folder it belongs to
image_to_upload_map = {}
new_pairings ={}
for upload in all_gps_tagged_uploads:
    images = sorted(Path(f"{upload}/OUTPUT").glob("*JPG"))
    if len(images) == 0:
        print("upload has no images",upload)
    else:
        for im in images:
            image_to_upload_map[im.stem] = upload
    
added_some = False
for tmp in tmp_folders:
    images = sorted(Path(f"{tmp}/images").glob("*JPG"))
    image_count = len(images)
    if len(images) >0:
        first = images[0]
        found = image_to_upload_map.get(first.stem,-1)
        if found !=-1:
            flight_level_status[tmp] ={
            "copied":"incomplete",
            "error":"no images found for folder",
            }
        else:
            print("matched ",tmp,found)
            flight_level_status[tmp] ={
            "copied":"complete",
            "number_images":image_count,
            "original_folder":found,
            "error":""
            }
            added_some=True


print("new pairings look like ",new_pairings)
if added_some:
  Path(f"pairings_{uuid.uuid4()}.json").write_text(json.dumps(new_pairings))
  print("""
FOUND TMP FOLDER CONTENT NOT PREVIOUSLY PAIRED TO FOLDER NAMES

RECOMMEND RE_REUNNING THIS SCRIPT

""")





## TODO show the number of folders yet to process at the bottom
for remaining_folder in all_gps_tagged_uploads:
  exists = flight_level_status.get(remaining_folder,-1) 
  if exists== -1:
    flight_level_status[remaining_folder] = {
    "error":"folder hasn't been processed"
  }

# this function will accept a folder name, and a file to look for, and a key to update in the dictionary if those two things exist
def status_updater_helper(parent_folder,fldr_name,file_name,dct,workflow_stage):
  fldr_path= Path(f"../tmp/{parent_folder}/{fldr_name}")
  if fldr_path.exists():
    file_name_path = Path(f"{fldr_path}/{file_name}")
    if file_name_path.exists():
      dct[workflow_stage] = "complete"
      return 1
  dct[workflow_stage]="incomplete"
  return 0


      

  
  

## here's where we are really going to get into fleshing out some more of the stats
image_total = 0
copied_count = 0
ortho_count =0
geo_count =0
texture_count =0
for fldr_key,fldr_data in flight_level_status.items():
## explore just the folders that have the flight_level_status copied, 
  print(fldr_key,fldr_data)
  copied_status = fldr_data.get("copied",-1)
  if copied_status =="complete":
    copied_count +=1
  ## add image number of timages to the total
    image_total += fldr_data["number_images"]
    ### all of the helper functions return 1 or 0 so that we can increment counts also
## find out if they have orthos
    ortho_count+=status_updater_helper(fldr_key,"odm_orthophoto","odm_orthophoto.tif",fldr_data,"ortho")
## find out if they have laz point cloud
    geo_count +=status_updater_helper(fldr_key,"odm_georeferencing","odm_georeferenced_model.laz",fldr_data,"georeferencing")
## find out if they have textured model or not.
    texture_count +=status_updater_helper(fldr_key,"odm_texturing","odm_textured_model_geo.obj",fldr_data,"texturing")


totals["total_images_copied"]=image_total
totals["total_flights_copied"] = copied_count
totals["total_flights_ortho"]=ortho_count
totals["total_flights_georeferenced"]=geo_count
totals["total_flights_textured_models"]=texture_count
high_level_status["flight_status"]=flight_level_status

## might be helpful to now go through and pick out the ones that were copied but haven't been 
## convert to yaml for visibility
yaml_text = yaml.dump(high_level_status)
print(yaml_text)
 
# get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
status_path = f"status_{current_datetime}.yaml"
Path(status_path).write_text(yaml_text)

## add in here some indication of the amount we have yet to cover still

## output to a file the following
## 

print(f"""
Feel free to check in the document
 {status_path}
it should contain a representation of folders that have flight_level_status "folder hasn't been processed"
These can be added to the staged_flights.txt
""")

input("press a key to close")

