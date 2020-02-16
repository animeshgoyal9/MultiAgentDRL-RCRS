import subprocess
import os
import socket
import sys

# Directory 
directory = socket.gethostname()
  
# Parent Directory path 
parent_dir = sys.path[0]
  
# Path 
path = os.path.join(parent_dir, directory) 
  
# os.mkdir(path) 
print("Directory '% s' created" % directory) 
print(os.path.join(parent_dir, "../../rcrs-adf-sample/launch.sh '-all'"))
