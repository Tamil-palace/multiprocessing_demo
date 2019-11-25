from multiprocessing import Process, Queue
from time import time
import face_recognition
import cv2


def run_detector(input_queue: Queue, output_queue: Queue):
    frame = input_queue.get()
    while frame is not None:
        face_locations = face_recognition.face_locations(frame)
        face_locations = [(right, top, left, bottom) for top, right, bottom, left in face_locations]
        output_queue.put((frame, face_locations))
        frame = input_queue.get()
    output_queue.put((None, None))


def get_video_frames(input_queue: Queue, video_path: str):
    cap = cv2.VideoCapture(video_path)

    grabbed, frame = cap.read()
    while grabbed:
        input_queue.put(cv2.resize(frame, (416, 416)))
        grabbed, frame = cap.read()

    input_queue.put(None)


def display_output(output_queue: Queue):
    t0 = time()
    fps = "FPS: 0"
    n = 10  # calc fps every n frames
    i = 1  # frame count

    frame, face_locations = output_queue.get()
    while frame is not None:
        for xmin, ymin, xmax, ymax in face_locations:
            frame = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 255), 1)

        if i % n == 0:
            t1 = time()
            fps = f"FPS {round(n / (t1 - t0), 1)}"
            t0 = t1

        i += 1
        frame = cv2.putText(frame, fps, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        cv2.imshow("Friends", frame)
        cv2.waitKey(1)

        frame, face_locations = output_queue.get()


if __name__ == '__main__':
    in_q = Queue(maxsize=10)
    out_q = Queue(maxsize=10)

    video_path = "friends.mp4"

    frames_getter = Process(target=get_video_frames, args=(in_q, video_path))
    detector1 = Process(target=run_detector, args=(in_q, out_q))
    detector2 = Process(target=run_detector, args=(in_q, out_q))
    display = Process(target=display_output, args=(out_q,))

    frames_getter.start()
    detector1.start()
    detector2.start()
    display.start()

    frames_getter.join()
    detector1.join()
    detector2.join()
    display.join()

    print("Finished...")
