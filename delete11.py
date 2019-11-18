import os
import subprocess
import signal

# print(os.getpid())

# os.killpg(os.getpgid(subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/start-comprun.sh", shell=True).pid), signal.SIGINT)

subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete_master.py"])