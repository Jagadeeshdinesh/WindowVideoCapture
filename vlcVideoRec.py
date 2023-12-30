import cv2
import pygetwindow as gw
import pyautogui
import numpy as np

# Function to capture VLC window
def capture_vlc_window(window_title):
    try:
        # Get the VLC window
        vlc_window = gw.getWindowsWithTitle(window_title)[0]
        
        # Activate the VLC window
        vlc_window.activate()

        # Capture the screen
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to a NumPy array
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame
    except IndexError:
        print("VLC window not found.")
        return None

# VLC window title (change this according to your VLC window title)
vlc_window_title = "VLC media player"

while True:
    # Capture frame from VLC window
    frame = capture_vlc_window(vlc_window_title)

    if frame is not None:
        # Display the captured frame
        cv2.imshow("VLC Screen Capture", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()