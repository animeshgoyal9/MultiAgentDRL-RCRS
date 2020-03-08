#!/usr/bin/env python

import subprocess
import time, os 
import signal, sys
import socket

path_for_start_file = os.path.join(sys.path[0], "start-comprun.sh -bp 4007 -rp 5010")
# path_for_start_file = os.path.join(sys.path[0], "start-comprun.sh -m ../maps/gml/berlin/map -c ../maps/gml/berlin/config")
path_for_launch_file = os.path.join(sys.path[0], "../../rcrs-adf-sample/launch.sh '-all'")

subprocess.Popen(path_for_start_file, shell=True)
time.sleep(10)
subprocess.Popen(path_for_launch_file, shell=True)
time.sleep(5000000)	
