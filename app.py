import face_recognition
import cv2
from mouth_helper_functions import is_mouth_open
import pyautogui
import sys

"""
    Press key on keyboard!
"""
def press(keypress):
    pyautogui.press(keypress)
    print('Press!')

"""
    Start the application invoking our while loop.
"""
def start(keypress):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    mouth_open = False
    while True:
        print('Running...')
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Find all the faces and face enqcodings in the frame of video
        face_landmarks_list = face_recognition.face_landmarks(frame)
        if (len(face_landmarks_list) == 0): continue

        m_open = is_mouth_open(face_landmarks_list[0])

        if (m_open and not mouth_open):
            mouth_open = m_open
            press(keypress)
            continue

        mouth_open = m_open

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


start(sys.argv[1])