import cv2
from cv2_enumerate_cameras import enumerate_cameras  # Add this import
import time
from modules.face_swapper import process_frame

from modules.face_analyser import (
    get_one_face,
)

def fit_image_to_size(image, width: int, height: int):
    if width is None and height is None:
        return image
    h, w, _ = image.shape
    ratio_h = 0.0
    ratio_w = 0.0
    if width > height:
        ratio_h = height / h
    else:
        ratio_w = width / w
    ratio = max(ratio_w, ratio_h)
    new_size = (int(ratio * w), int(ratio * h))
    return cv2.resize(image, dsize=new_size)

def get_available_cameras():
    """Returns a list of available camera names and indices."""
    camera_indices = []
    camera_names = []

    for camera in enumerate_cameras():
        cap = cv2.VideoCapture(camera.index)
        if cap.isOpened():
            camera_indices.append(camera.index)
            camera_names.append(camera.name)
            cap.release()
    return (camera_indices, camera_names)


def start():

    # camera = cv2.VideoCapture("1.mp4")
    # camera.set(cv2.CAP_PROP_FPS, 60)

    source_image = None
    # prev_time = time.time()
    # fps_update_interval = 0.5  # Update FPS every 0.5 seconds
    # frame_count = 0
    # fps = 0

    frame = cv2.imread("target.jpeg")
    temp_frame = frame.copy()
    if source_image is None:
        source_image = get_one_face(cv2.imread("face.jpg"))
    temp_frame = process_frame(source_image, temp_frame)
    cv2.imwrite("result.jpg", temp_frame)
    # while camera:
    #     ret, frame = camera.read()
    #     if not ret:
    #         break

    #     temp_frame = frame.copy()

    #     if source_image is None:
    #         source_image = get_one_face(cv2.imread("face.jpg"))
    #     temp_frame = process_frame(source_image, temp_frame)
    #     # Calculate and display FPS
    #     # current_time = time.time()
    #     # frame_count += 1
    #     # if current_time - prev_time >= fps_update_interval:
    #     #     fps = frame_count / (current_time - prev_time)
    #     #     frame_count = 0
    #     #     prev_time = current_time
    #     # print(fps)

    #     cv2.imshow("Face Swap Video", temp_frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # camera.release()