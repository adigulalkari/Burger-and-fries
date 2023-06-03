import numpy as np
import cv2
import imutils

def detect_weapon():
    cascade = cv2.CascadeClassifier('models/weapon_cascade.xml')

    bank_camera = cv2.VideoCapture(0)

    firstFrame = None
    wframe_count = 0
    weapon_count = 0

    while True:
        (grabbed, frame) = bank_camera.read()

        if not grabbed:
            break
        wframe_count += 1
        frame = imutils.resize(frame, width=700)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gun = cascade.detectMultiScale(gray, 1.3, 50)

        weapon_detected = False  # Flag to track if a weapon is detected

        for (x, y, w, h) in gun:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            weapon_detected = True  # Set the flag to True if a weapon is detected

        if weapon_detected:
            weapon_count += 1

        if firstFrame is None:
            firstFrame = gray
            continue

        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            cv2.destroyAllWindows()
            break

    bank_camera.release()
    cv2.destroyAllWindows()

    if weapon_count / wframe_count > 0.2:
        print("Definitely dangerous!")
        return 10
        
    else:
        print("Not suspicious.")
        return 0
    