#!/bin/bash
cd /home/ubuntu
source .profile

cd deepracer-for-cloud
aws s3 cp s3://markpett-training/env_files/ . --recursive
aws s3 cp s3://markpett-training/startup_files/is_bucket_changing.py is_bucket_changing.py
aws s3 cp s3://markpett-training/startup_files/can_overwrite_folder.py can_overwrite_folder.py

sleep 5
dr-update

# python script checks if safe to overwrite folder
CAN_OVERWRITE=$(python3 can_overwrite_folder.py)
if [ "$CAN_OVERWRITE" = "overwrite" ] ; then
    dr-start-training -w -q
else
    dr-increment-training -f
    # dr-increment-training -f -p MarkP-10gTurnRadius-1
    dr-start-training -q
    aws s3 cp run.env s3://markpett-training/env_files/
fi

# python script keeps checking if bucket is being updated
# and reboots if there is nothing changing
python3 is_bucket_changing.py 600
