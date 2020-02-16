import subprocess
import time, os 
import signal, sys
import socket

path_for_start_file = os.path.join(sys.path[0], "start-comprun.sh")
path_for_launch_file = os.path.join(sys.path[0], "../../rcrs-adf-sample/launch.sh '-all'")

subprocess.Popen(path_for_start_file, shell=True)
time.sleep(10)
subprocess.Popen(path_for_launch_file, shell=True)
time.sleep(5000000)	
