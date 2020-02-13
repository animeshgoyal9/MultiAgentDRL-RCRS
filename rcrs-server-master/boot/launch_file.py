import subprocess
import time, os 
import signal, sys

# subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/start-comprun.sh -m ../maps/gml/berlin/map -c ../maps/gml/berlin/config", shell=True)
subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-server-master/boot/start-comprun.sh", shell=True)
time.sleep(10)
subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-adf-sample/launch.sh '-all'", shell=True)
time.sleep(5000000)	
