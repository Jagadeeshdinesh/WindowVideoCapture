from flask import Flask, Response
import cv2
import pygetwindow as gw
import mss
import numpy as np
from PIL import Image

app = Flask(__name__)
# video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return "Default Message"


def gen():
    vlc_window_title = "vlc"

    try:
        while True:
            # Get the VLC window
            vlc_window = gw.getWindowsWithTitle(vlc_window_title)[0]

            # Get the position and size of the VLC window
            x, y, width, height = vlc_window.left, vlc_window.top, vlc_window.width, vlc_window.height

            # Create a MSS screenshot object
            with mss.mss() as sct:
                # Set the capture region based on the VLC window position and size
                region = {'left': x, 'top': y, 'width': width, 'height': height}

                screenShot = sct.grab(region)
                img = Image.frombytes(
                    'RGB', 
                    (screenShot.width, screenShot.height), 
                    screenShot.rgb, 
                )
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.resize(frame, (1080, 720))
                cv2.imshow('test', np.array(frame))

                image = frame
                frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                frame_gray = cv2.equalizeHist(frame_gray)

                ret, jpeg = cv2.imencode('.jpg', image)

                frame = jpeg.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                if cv2.waitKey(33) & 0xFF in (ord('q'), 27):
                    break
                
    except IndexError:
        print("VLC window not found.")
    # while True:
    #     # vlc_window_title = "vlc"

    #     # Call the function to capture video from the VLC window
    #     image = capture_vlc_video(vlc_window_title)
    #     # success, image = video.read()
    #     frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     frame_gray = cv2.equalizeHist(frame_gray)
    #     print("name")

    #     # faces = face_cascade.detectMultiScale(frame_gray)

    #     # for (x, y, w, h) in faces:
    #     #     center = (x + w//2, y + h//2)
    #     #     cv2.putText(image, "X: " + str(center[0]) + " Y: " + str(center[1]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    #     #     image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #     #     faceROI = frame_gray[y:y+h, x:x+w]
    #     ret, jpeg = cv2.imencode('.jpg', image)

    #     frame = jpeg.tobytes()
        
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # global video
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
