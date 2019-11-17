import subprocess
import time, os 
import signal, sys

 
# subprocess.call(["sh", "kill.sh"])

subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/start-comprun.sh", shell=True)
time.sleep(30)