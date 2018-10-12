import cv2
import threading
import socket
import struct
from io import StringIO
import json
import numpy as np
import time

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Streamer (threading.Thread):
  def __init__(self, hostname, port):
    threading.Thread.__init__(self)

    self.hostname = hostname
    self.port = port
    self.connected = False
    self.jpeg = None
    self.video = None
    self.key = b'2345678910111213'
    self.i = 0
    self.i1 = 0
    self.isVideoPlayed = False

  def run(self):
    self.isRunning = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.connect((socket.gethostbyname(self.hostname), self.port))
    #s.settimeout(2)
    print("Connected to, Host:{0} Port:{1}".format(self.hostname, self.port))

    while self.isRunning:
      # conn, addr = s.accept()
      t = b''
      while True:
        data = b''

        while True:
          r = s.recv(2048)
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

  def set_video(self, data):
    self.video = data

  def stop(self):
    self.isRunning = False

  def client_connected(self):
    return self.connected

  def get_jpeg(self):
    return self.jpeg.tobytes()























