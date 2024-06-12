#!/bin/bash
ssh team1@192.168.55.1
ifconfig

ssh team1@10.31.141.191
source ~/realsense/bin/activate
python ~/Desktop/realsense_code/stream_out_60.py --ip 10.31.141.191

conda activate pytorch
python ~/Desktop/mobile_robot/stream_in.py

# Optional
pkill realsense
sudo shutdown -h now
