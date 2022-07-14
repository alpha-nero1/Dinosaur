import face_recognition
import cv2
from mouth_helper_functions import get_lip_height, get_mouth_height, is_mouth_open
from datetime import datetime
import pyautogui
import sys

def jump(frame):
    pyautogui.press('space')
    cv2.putText(frame, "JUMP", (115, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2, 2)

def start(name_arg):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object to save video to local
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # codec
    # cv2.VideoWriter( filename, fourcc, fps, frameSize )
    out = cv2.VideoWriter('output.avi', fourcc, 7, (640, 480))

    # Load a sample picture and learn how to recognize it.
    person_image = face_recognition.load_image_file(f'./images/{name_arg}.jpg') # replace peter.jpg with your own image !!
    person_face_image = face_recognition.face_encodings(person_image)[0]

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(frame)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding, face_landmarks in zip(face_locations, face_encodings, face_landmarks_list):

            #  See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([person_face_image], face_encoding)

            name = "Unknown"
            if match[0]:
                name = name_arg

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)

            # Display text for mouth open / close
            ret_mouth_open = is_mouth_open(face_landmarks)

            if ret_mouth_open:
                jump(frame)


        # Display the resulting image
        cv2.imshow('Video', frame)
        out.write(frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


start(sys.argv[2])