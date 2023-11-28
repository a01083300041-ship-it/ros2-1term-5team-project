import os
import sys


os.system("ros2 run gazebo_ros spawn_entity.py -database prius_hybrid  -entity PR001 -x 25.88 -y -17.5  -Y 3.14 ")
os.system("ros2 run gazebo_ros spawn_entity.py -database prius_hybrid2  -entity PR002 -x 29.97 -y -17.5  -Y 3.14")
