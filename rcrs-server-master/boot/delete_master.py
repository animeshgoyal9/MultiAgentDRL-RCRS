import subprocess
import time, os 
import signal, sys


# subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete.py"])

# while True:
# 	pp = subprocess.Popen("bash 'start-comprun.sh'", shell=True)

# 	time.sleep(10)

# 	qq = subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-adf-sample/launch.sh '-all'", shell=True)
# 	# subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete.py"])
# 	time.sleep(20)


subprocess.Popen("bash 'start-comprun.sh'", shell=True)
time.sleep(10)
subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-adf-sample/launch.sh '-all'", shell=True)
time.sleep(300)	
# subprocess.call(['python3', '/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete.py'])

# time.sleep(20)

# subprocess.call(['python3', '/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete1.py'])

# time.sleep(10)

# subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete.py"])