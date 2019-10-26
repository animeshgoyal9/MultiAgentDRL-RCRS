#!/usr/bin/python


# import socket, pickle

# HOST = 'localhost'
# PORT = 5119
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(5)
# while True:
# 	conn, addr = s.accept()
# 	print ('Connected by', addr)
# 	arr = ([1,2,3,4,5,6],[1,2,3,4,5,6])
# 	data_string = pickle.dumps(arr)
# 	# myList = "123"
# 	conn.send(data_string)
# # conn.close()

# ********************************************8

# #!/usr/bin/python           # This is server.py file

# import socket               # Import socket module

# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# port = 12325                # Reserve a port for your service.
# s.bind((host, port))        # Bind to the           ort

# s.listen(5)                 # Now wait for client connection.
# while True:
#    c, addr = s.accept()     # Establish connection with client.
#    print ('Got connection from', addr)
#    c.send(b'Thank you for connecting')
#    c.close()          

# ****************************************************

import socket, pickle, json, subprocess, ast
from subprocess import *
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 2025 
s.bind(('localhost', port))
s.listen(5)
while True:
	c, addr = s.accept()
	print ("Socket Up and running with a connection from",addr)
	rcvdData = c.recv(1024)
	final = bytes(rcvdData).decode("utf-8")
	print(final)
	# print(type(final))
	final_3 = list(final.split("|"))
	final_2 = list(final.split(", "))
	final_5 = final_3[0]
	final_4 = final_3[1]

	final_5 = final_5.replace('[','')
	final_5 = final_5.replace(',','')
	final_5 = final_5.replace(']','')
	final_5 = list(final_5.split(" "))
	final_5 = final_5[:-1]
	state_list = [int(i) for i in final_5]

	final_4 = final_4.replace('[','')
	final_4 = final_4.replace(',','')
	final_4 = final_4.replace(']','')
	final_4 = list(final_4.split(" "))
	final_4 = final_4[1:]
	
	action_list = [int(i) for i in final_4]
	# # test_list_1 = [int(i) for i in final_5]
	print("************************This is the State space************************")
	print(state_list)
	print("************************This is the Action space***********************")
	print(action_list)
	# # # final_1 = ast.literal_eval(final)
	# # # print(final_1)
	# # print(type(final_1))
	# final_1 = pickle.dumps(final)
	# final_1 = pickle.loads(final_1)
	# print(final_1)
	# c.send(bytes([936, 259], encoding= "utf-8"))
	c.send(bytes([936, 259]).encode("utf-8"))
	print("------------------------------------------------------------------------")
	c.close()


# *******************************************************

# import socket

# HOST = "localhost"
# PORT = 9999
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('Socket created')

# try:
#     s.bind((HOST, PORT))
# except socket.error as err:
#     print('Bind failed. Error Code : ' .format(err))
# s.listen(10)
# print("Socket Listening")
# conn, addr = s.accept()
# while(True):
#     conn.send(bytes("Message"+"\r\n",'UTF-8'))
#     print("Message sent")
#     # data = conn.recv(1024)
#     # print(data.decode(encoding='UTF-8'))
#     break
# conn.close()