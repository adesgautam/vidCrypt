# vidCrypt
This project aims to securely livestream webcam using AES-128 over network and also steam videos on demand over network.

Currently the livestream is working but the video on demand needs work.

![Running the client and server on the local machine](https://drive.google.com/open?id=1dEfF_6cpf_-7jTcPyKdn5WRKLvEtsnQM)

![Actual encrypted data transfer of the stream.](https://drive.google.com/open?id=145Zu_LapIj6DFEOEhiyei_ASFUrNIf4v)

![Live Streaming of the Webcam on a local machine. The live video stream and the video resolution is encrypted according to the network speed.](https://drive.google.com/open?id=1Xol_5yKqo-pETdkYpgtD7zKHIEfVX2oU)

## For running the project:
Dependencies:
1. [OpenCV](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)
2. [Numpy](http://www.numpy.org/)
3. [Pycryptodome](https://pycryptodome.readthedocs.io/)
4. [Flask](http://flask.pocoo.org/)
5. [ffmpeg](https://www.ffmpeg.org/)
Install the dependencies using pip.

### Running the Webcam livstream:
1. Run ```python server.py``` on terminal
2. Run ```python client.py``` on another terminal
3. Now open ```http://127.0.0.1:5000/``` in browser to watch the webcam livestream

### Running the video on demand:
1. Create a folder ```outputs``` and run 

   ```ffmpeg -i input_video_to stream.mp4 -c copy -map 0 -segment_time 8 -f segment -reset_timestamps 1 outputs/output%03d.mp4```

This will split the original video into chunks in the ```outputs``` folder. These chunks will be streamed over the network.

2. Now, run ```python server.py``` on terminal. to start the server.

3. Run ```python client.py``` on another terminal to start the client.

4. Now open ```http://127.0.0.1:5000/``` in browser to watch the stream.

## Edit the Webcam livestream parameters
For switching the network speed, change the "download" variable in the ```server.py``` file on line 20. And, for making it perform automatically change the "test" variable's value as True.

This streaming is now working correctly. Only the first chunk gets played. 

Please help to make it working. Raise issues and make pull requests.

For queries contact me at adeshg7@gmail.com
 
