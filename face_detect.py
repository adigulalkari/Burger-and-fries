import numpy as np
import cv2
import imutils

def detect_faces():
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('models/haarcascade_smile.xml')

    cap = cv2.VideoCapture(0)
    face_count = 0  # Initialize face count variable
    frame_count = 0  # Initialize frame count variable

    while True:
        ret, frame = cap.read()
        if ret == False:
            continue
        frame_count += 1  # Increment frame count

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)

        if len(faces) > 1:
            print("Multiple faces detected in the same frame")

        if len(faces) != 0:
            face_count += 1  # Increment face count

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                mouths = mouth_cascade.detectMultiScale(roi_gray)
                eyes = sorted(eyes, key=lambda x: x[2] * x[3], reverse=True)
                mouths = sorted(mouths, key=lambda x: x[2] * x[3], reverse=True)
                if len(mouths) > 0:
                    mx, my, mw, mh = mouths[0]
                    cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                for ix in range(len(eyes)):
                    if ix > 1:
                        continue
                    ex, ey, ew, eh = eyes[ix]
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow("Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    print("Total faces detected:", face_count)
    print("Total frames used:", frame_count)

    if face_count/frame_count<0.7:
        return 5
    else:
        return 0

