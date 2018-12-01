
# Image Processing
import cv2
import numpy as np

# Sockets
import socket

# Encryption
from base64 import b64encode
from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad

# Speed Test
from speedTest import SpeedTestResults

test = False
download = 0.5

# Network Speeds
# 0     - 0.05 MB/s    -> DES
# 0.05  - 0.1 MB/s     -> 3DES
# 0.1   - 0.3 MB/s     -> AES-128
# 0.3   - 0.6 MB/s     -> AES-192
# 0.6   - more         -> AES-256

# Resolutions
# 426x240   -> 240p
# 640x360   -> 360p
# 854x480   -> 480p
# 1280x720  -> 720p

if test:
	print("Testing your network...")
	st = SpeedTestResults()
	download, upload, ping = st.get_results()
	print("Your Network Speed Results:")
	print("Download: {0} MB/s, Upload: {1} MB/s, Ping: {2} ms".format(download, upload, ping))

# misc
end = b'END!'

if float(download) <= 0.05:
	ci = 0          # DES
	w, h = 426, 240 # 240p
elif float(download) > 0.05 and float(download) <= 0.1:
	ci = 1          # DES3
	w, h = 640, 360 # 360p
else:
	ci = 2          # AES-128
	w, h = 854, 480 # 480p

# Capture video
cap = cv2.VideoCapture(0)

# Setup socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostbyname("localhost")
host = "192.168.43.28"
port = 9006

serversocket.bind((host, port))
serversocket.listen(5)
print("Listening...")

# Wait for client
clientsocket, addr = serversocket.accept()
print("Got connection from {0}".format(str(addr)))

# Setup the cipher mode
if ci==0:
	clientsocket.sendall(b'0')
	print("Using DES...")  
elif ci==1:
	clientsocket.sendall(b'1')
	print("Using DES3...")
else:
	clientsocket.sendall(b'2')
	print("Using AES...")

# Send frames
while(cap.isOpened()):
	ret, frame = cap.read()
	frame = cv2.resize(frame, (w, h)) 
	frame = cv2.flip(frame, 1)
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	data = cv2.imencode('.jpg', frame)[1].tostring()
	if ret == True:
		# print('Streaming webcam...')
		# print("data:", data[:50])
		
		if ci == 0:
			key = b'12345678' # 8 bytes
			cipher = DES.new(key, DES.MODE_CBC)
			ct_bytes = cipher.encrypt(pad(data, DES.block_size))
			iv = b64encode(cipher.iv)
			ct = b64encode(ct_bytes)
			d = iv+ct+end
			print("DATA sent:", d[:50])
			clientsocket.sendall(d)

		elif ci == 1:
			key = b'123456789101112131415161' # 24 bytes
			cipher = DES3.new(key, DES3.MODE_CBC)
			ct_bytes = cipher.encrypt(pad(data, DES3.block_size))
			iv = b64encode(cipher.iv)
			ct = b64encode(ct_bytes)
			d  = iv+ct+end
			print("DATA sent:", d[:50])
			clientsocket.sendall(d)

		else:
			key = b'2345678910111213' # 16 bytes
			cipher = AES.new(key, AES.MODE_CBC)
			ct_bytes = cipher.encrypt(pad(data, AES.block_size))
			iv = b64encode(cipher.iv)
			ct = b64encode(ct_bytes)
			d  = iv+ct+end
			print("DATA sent:", d[:50])
			clientsocket.sendall(d)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		# time.sleep(1)
	else:
		cap.release()
		clientsocket.close()
		exit(0)








