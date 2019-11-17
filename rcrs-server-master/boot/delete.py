import subprocess
import time, os 
import signal, sys
import threading


pp = subprocess.Popen("bash 'start-comprun.sh'", shell=True)

time.sleep(10)

qq = subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-adf-sample/launch.sh '-all'", shell=True)

# time.sleep(13)

# os.killpg(os.getpgid(pp.pid), signal.SIGINT)

# subprocess.run('bash start-comprun.sh')

# subprocess.call(["bash", "start-comprun.sh"])

# # q = subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-adf-sample/launch.sh '-all'", shell=True)
# # subprocess.call(["/u/animesh9/Documents/RoboCup-gRPC/rcrs-adf-sample/launch.sh", "-all"]) 

# time.sleep(10)

# import os
# import sys
# import psutil
# import logging

# def restart_program():
#     """Restarts the current program, with file objects and descriptors
#        cleanup
#     """

#     try:
#         p = psutil.Process(os.getpid(qq.getpid))
#         for handler in p.open_files() + p.connections():
#             os.close(handler.fd)
#     except Exception as e:
#         logging.error(e)

#     python = sys.executable
#     os.execl(python, python, *sys.argv)


# restart_program()