import cv2
import pygetwindow as gw
import mss
import numpy as np
from PIL import Image

def capture_vlc_video(window_title):
    try:
        # Get the VLC window
        vlc_window = gw.getWindowsWithTitle(window_title)[0]

        # Get the position and size of the VLC window
        x, y, width, height = vlc_window.left, vlc_window.top, vlc_window.width, vlc_window.height
        print(vlc_window.height)

        # Create a MSS screenshot object
        with mss.mss() as sct:
            # Set the capture region based on the VLC window position and size
            region = {'left': x, 'top': y, 'width': width, 'height': height}

            print(region)

            while True:
                screenShot = sct.grab(region)
                img = Image.frombytes(
                    'RGB', 
                    (screenShot.width, screenShot.height), 
                    screenShot.rgb, 
                )
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow('test', np.array(frame))
                if cv2.waitKey(33) & 0xFF in ( 
                    ord('q'), 
                    27, 
                ):
                    break

    except IndexError:
        print("VLC window not found.")

# VLC window title (change this according to your VLC window title)
# vlc_window_title = "VLC media player"
vlc_window_title = "Wireless Display"

# Call the function to capture video from the VLC window
capture_vlc_video(vlc_window_title)

# Release resources
cv2.destroyAllWindows()
