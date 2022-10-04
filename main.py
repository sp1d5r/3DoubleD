"""
Camera Initialisation
Get the camera set up and show what the camera sees
"""

import numpy as np
import cv2
import random
import requests
import mediapipe as mp

WIDTH = 640
HEIGHT = 480


cap = cv2.VideoCapture(0)
# cap1 = cv2.VideoCapture(1)
cap.set(3, WIDTH)  # set Width
cap.set(4, HEIGHT)  # set Height
# cap1.set(3, WIDTH)
# cap1.set(4, HEIGHT)

TOP_LEFT = (int(WIDTH / 2) - 5, int(HEIGHT / 2) - 5)
BOTTOM_RIGHT = (int(WIDTH / 2) + 5, int(HEIGHT / 2) + 5)

BOTTOM_LEFT = (int(WIDTH / 2) - 5, int(HEIGHT / 2) + 5)
TOP_RIGHT = (int(WIDTH / 2) + 5, int(HEIGHT / 2) - 5)


def draw_line_to_point(img_frame, point_coords, center=(int(WIDTH/2), int(HEIGHT/2))):
    cv2.line(img_frame, center, point_coords, (0, 0, 255), 2)
    distance_x, distance_y = point_coords[0] - center[0], point_coords[1] - center[1]
    text_position = (center[0] + int(distance_x / 2), center[1] + int(distance_y / 2))
    cv2.putText(
        img_frame,
        f"({abs(distance_x)}, {abs(distance_y)})",
        text_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0,0,255),
        1,
        cv2.LINE_AA
    )

loop = 0
random_point = (352, 123)

# Getting the IRIS
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
)

# IRIS Frames
LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


def draw_axis(frame):
    # Draw the y-Axis
    cv2.line(frame, (int(WIDTH / 2), 0), (int(WIDTH / 2), HEIGHT), (255, 0, 0), 1)

    # Draw the x-Axis
    cv2.line(frame, (0, int(HEIGHT / 2)), (WIDTH, int(HEIGHT / 2)), (255, 0, 0), 1)

    # Get center X
    cv2.line(frame, TOP_LEFT, BOTTOM_RIGHT, (0, 0, 0), 3)
    cv2.line(frame, BOTTOM_LEFT, TOP_RIGHT, (0, 0, 0), 3)


def get_face_atributes(frame):
    # Process IRIS from face model.
    results = face_mesh.process(frame)
    if results.multi_face_landmarks:
        mesh_points = np.array(
            [np.multiply([p.x, p.y], [WIDTH, HEIGHT]).astype(int) for p in results.multi_face_landmarks[0].landmark])

        cv2.polylines(frame, [mesh_points[LEFT_IRIS]], True, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(frame, [mesh_points[RIGHT_IRIS]], True, (0, 255, 0), 1, cv2.LINE_AA)

        left_iris_center = (int(sum([i[0] for i in mesh_points[LEFT_IRIS]]) / len(LEFT_IRIS)),
                            int(sum([i[1] for i in mesh_points[LEFT_IRIS]]) / len(LEFT_IRIS)))

        right_iris_center = (int(sum([i[0] for i in mesh_points[RIGHT_IRIS]]) / len(RIGHT_IRIS)),
                             int(sum([i[1] for i in mesh_points[RIGHT_IRIS]]) / len(RIGHT_IRIS)))

        update_positions(left_iris_center, right_iris_center)

        draw_line_to_point(frame, left_iris_center)
        draw_line_to_point(frame, right_iris_center)
    else:
        # No eyes found
        cv2.putText(
            frame,
            "no eyes found!",
            (30, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA
        )

x_position = 0
y_position = 0


def update_positions(left_iris_center, right_iris_center):
    global x_position, y_position
    iris_center_x, iris_center_y = (left_iris_center[0] + right_iris_center[0])/2, (left_iris_center[1] + right_iris_center[1])/2
    if iris_center_x != x_position:
        x_position = iris_center_x
        requests.get(f"http://127.0.0.1:5000/set_x?x_pos={iris_center_x}")

    if iris_center_y != y_position:
        y_position = iris_center_y
        requests.get(f"http://127.0.0.1:5000/set_y?y_pos={iris_center_y}")


while (True):
    ret, frame = cap.read()
    # ret1, frame1 = cap1.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)

    get_face_atributes(frame)
    # get_face_atributes(frame1)

    # If your camera orientation changes you can flip it
    # frame = cv2.flip(frame, -1)

    draw_axis(frame)
    # draw_axis(frame1)

    frame = cv2.flip(frame, 1)
    # frame1 = cv2.flip(frame1, 1)

    # Flip the image vertically so it matches the real world
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Builtin Cam', frame)
    # cv2.imshow('Webcam', frame1)
    # cv2.imshow('gray', gray)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
# cap1.release()
cv2.destroyAllWindows()