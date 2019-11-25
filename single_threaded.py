import face_recognition
import cv2
from time import time

video_path = "friends.mp4"
times = []
cap = cv2.VideoCapture(video_path)
t0 = time()
fps = "FPS: 0"
n = 10

for i in range(10**20):
    grabbed, frame = cap.read()
    if not grabbed:
        break

    # face detections
    frame = cv2.resize(frame, (416, 416))
    face_locations = face_recognition.face_locations(frame)
    for top, right, bottom, left in face_locations:
        # cv2.rectangle(image, start_point, end_point, color, thickness)
        frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 1)

    # fps calc
    if i % n == 0:
        t1 = time()
        fps = f"FPS {round(n/(t1-t0), 1)}"
        t0 = t1
    # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    frame = cv2.putText(frame, fps, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    cv2.imshow("Friends", frame)

    if 255 & cv2.waitKey(1) == ord('q'):
        break


