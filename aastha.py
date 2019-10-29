import socket, pickle, json, subprocess, ast
from subprocess import *
import numpy as np
import threading 

#portName = ['Score','Agent','Building']
port = [2211, 2025, 4011] 
ss = []

def createSocket(port): 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('localhost', port))
	s.listen(5)
	return s

def readMessage(s):
	while True:
		c, addr = s.accept()
		print ("Socket Up and running with a connection from ",addr)
		rcvdData = c.recv(1024)
		final = bytes(rcvdData).decode("utf-8")
		print(final)

		# if len(final) < 50:
		# 	print("************************This is the Rewards************************")
		# 	print(float(final))
		# else:
		# 	final_3 = list(final.split("|"))
		# 	state = final_3[0]
			
		# 	state = state.replace('[','')
		# 	state = state.replace(',','')
		# 	state = state.replace(']','')
		# 	state = list(state.split(" "))
		# 	state = state[:-1]
		# 	state_list = [int(i) for i in state]

		# 	action = final_3[1]
		# 	action = action.replace('[','')
		# 	action = action.replace(',','')
		# 	action = action.replace(']','')
		# 	action = list(action.split(" "))
		# 	action = action[1:]
		# 	action_list = [int(i) for i in action]
		# 	print("************************This is the State space************************")
		# 	print(state_list)
		# 	print("************************This is the Action space***********************")
		# 	print(action_list)
		c.close()

if __name__ == "__main__":
	for p in port:
		ss.append(createSocket(p));
	
	for s in ss:
		t = threading.Thread(target=readMessage, args=(s,))
		t.start()