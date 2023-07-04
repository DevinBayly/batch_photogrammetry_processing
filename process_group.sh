#!/bin/bash
uid_key=$1
python3 sym_link_group.py $uid_key
# now navigate to that folder and start the processing
python3 odm_group.py $uid_key
