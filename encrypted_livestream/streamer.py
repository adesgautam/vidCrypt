import cv2
import threading
import socket
import numpy as np

from base64 import b64decode
from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import unpad

class Streamer(threading.Thread):
	def __init__(self, hostname, port):
		threading.Thread.__init__(self)

		self.hostname = hostname
		self.port = port
		self.connected = False
		self.jpeg = None
		self.key = None
		self.i = 0
		self.buff = 2048

	def run(self):
		self.isRunning = True

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.connect((socket.gethostbyname(self.hostname), self.port))
		# s.connect((self.hostname, self.port))
		#s.settimeout(2)
		print("Connected to, Host:{0} Port:{1}".format(self.hostname, self.port))

		# Setup the cipher mode
		ci = s.recv(1024)
		if len(ci)==0:
			print("No Cipher mode detected!")
			exit(0)

		if ci == b'0':
			self.key = b'12345678' # 8 bytes
			print("Using DES...")
		elif ci == b'1':
			self.key = b'123456789101112131415161' # 24 bytes
			print("Using DES3...")
		else:
			self.key = b'2345678910111213' # 16 bytes
			print("Using AES...")

		while self.isRunning:

			t = b''
			while True:
				data = b''

				while True:
					r = s.recv(self.buff)
					if len(r)==0:
						exit(0)
					end = r.find(b'END!')
					if end != -1:
						data = t + data + r[:end]
						t = r[end+4:]
						break
					data += r

				if data is not None:
					print("data:", data[:50])
					# iv = data[:24]
					# data = data[24:]
					if ci == b'0':
						x = data.find(b'=')
						iv = data[:x+1]
						data = data[x+1:]

						cipher = DES.new(self.key, DES.MODE_CBC, b64decode(iv))
						data = unpad(cipher.decrypt(b64decode(data)), DES.block_size)
					elif ci == b'1':
						x = data.find(b'=')
						iv = data[:x+1]
						data = data[x+1:]

						cipher = DES3.new(self.key, DES3.MODE_CBC, b64decode(iv))
						data = unpad(cipher.decrypt(b64decode(data)), DES3.block_size)
					else:						
						x = data.find(b'==')
						iv = data[:x+2]
						data = data[x+2:]

						cipher = AES.new(self.key, AES.MODE_CBC, b64decode(iv))
						data = unpad(cipher.decrypt(b64decode(data)), AES.block_size)

					nparr = np.fromstring(data, np.uint8)
					frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
					ret, jpeg = cv2.imencode('.jpg', frame)

					self.jpeg = jpeg
					self.connected = True
				else:
					# conn.close()
					self.connected = False
					break
		self.connected = False

	def stop(self):
		self.isRunning = False

	def client_connected(self):
		return self.connected

	def get_jpeg(self):
		return self.jpeg.tobytes()























