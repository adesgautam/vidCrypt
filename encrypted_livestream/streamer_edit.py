import cv2
import threading
import socket
import struct
from io import StringIO
import json
import numpy as np

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

  def run(self):

    self.isRunning = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # s.bind((self.hostname, self.port))
    # print('Socket bind complete')
    s.connect((socket.gethostbyname(self.hostname), self.port))
    #s.settimeout(2)
    print("Connected to, Host:{0} Port:{1}".format(self.hostname, self.port))

    key = b'2345678910111213'
    # data = ""
    # payload_size = struct.calcsize("L")

    # s.listen(10)
    # print('Socket now listening')

    while self.isRunning:

      # conn, addr = s.accept()
      while True:

        data = b''
        while True:
          r = s.recv(900456)
          if len(r)==0:
            exit(0)
          end = r.find(b'END!')
          if end != -1:
            data += r[:end]
            break
          data += r

        if data is not None:
          print("data:", data[:50])
          # iv = data[:24]
          # data = data[24:]
          x = data.find(b'==')
          iv = data[:x+2]
          data = data[x+2:]

          cipher = AES.new(key, AES.MODE_CBC, b64decode(iv))
          data = unpad(cipher.decrypt(b64decode(data)), AES.block_size)

          nparr = np.fromstring(data, np.uint8)
          frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
          ret, jpeg = cv2.imencode('.jpg', frame)
          self.jpeg = jpeg

          self.connected = True

        else:
          conn.close()
          self.connected = False
          break

    self.connected = False

  def stop(self):
    self.isRunning = False

  def client_connected(self):
    return self.connected

  def get_jpeg(self):
    return self.jpeg.tobytes()