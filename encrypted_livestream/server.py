import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import io
import json

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

cap = cv2.VideoCapture(0)
# clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# clientsocket.connect(('localhost',8089))

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("localhost")
# host = "192.168.43.28"
port = 9002

serversocket.bind((host, port))
serversocket.listen(5)
print("Listening...")

clientsocket, addr = serversocket.accept()
print("Got connection from {0}".format(str(addr)))

key = b'2345678910111213'
end = b'END!'

while(cap.isOpened()):
	ret, frame = cap.read()
	frame = cv2.resize(frame, (600, 350)) 
	frame = cv2.flip(frame, 1)
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	data = cv2.imencode('.jpg', frame)[1].tostring()
	if ret == True:
		# print('Streaming webcam...')
		# print("data:", data[:50])
	
		cipher = AES.new(key, AES.MODE_CBC)
		ct_bytes = cipher.encrypt(pad(data, AES.block_size))
		iv = b64encode(cipher.iv)
		ct = b64encode(ct_bytes)
		
		d = iv+ct+end
		print("DATA sent:", d[:50])
		clientsocket.sendall(d)
		# clientsocket.sendall(data+b'END!')

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		# time.sleep(1)
	else:
		cap.release()
		clientsocket.close()
		exit(0)








