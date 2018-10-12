from flask import Flask, render_template, Response, stream_with_context
from streamer import Streamer
import cv2, time

app = Flask(__name__)

def gen_img():
  streamer = Streamer('localhost', 9002)
  streamer.start()

  while True:
    if streamer.client_connected():
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_jpeg() + b'\r\n\r\n')

def gen_video():
  streamer = Streamer('localhost', 9002)
  streamer.start()
  minutes = 0

  while True:
    if streamer.client_connected():
      time.sleep(minutes)

      path = 'output/file' + str(streamer.i) + '.mp4'
      f = open(path, 'rb')
      data = f.read()
      print("file ", streamer.i, " READ")
      f.close()
      # streamer.video = data

      # vid = cv2.VideoCapture(path)
      # fps = vid.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
      # frameCount = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
      # duration = frameCount/fps
      # minutes = int(duration/60)
      minutes = 7
      streamer.i += 1
      # yield streamer.get_video()
      yield data

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/video_feed')
def video_feed():
  # return Response(gen_img(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(stream_with_context(gen_video()), mimetype="video/mp4", direct_passthrough=True)

if __name__ == '__main__':
  app.run(host='localhost', threaded=True)
















