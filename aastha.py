import socket, pickle, json, subprocess, ast
from subprocess import *
import numpy as np
import threading 

#portName = ['Score','Agent','Building']
port = [2025, 2211] 
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
		data = bytes(rcvdData).decode("utf-8")
		print(data)
		c.close()

if __name__ == "__main__":
	for p in port:
		ss.append(createSocket(p));
	
	for s in ss:
		t = threading.Thread(target=readMessage, args=(s,))
		t.start()