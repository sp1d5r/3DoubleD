from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import requests
import math

app = Ursina()
room = Entity(model="./models/room.obj", texture="brick", scale=0.7, x=0, y=-7)
cube = Entity(model="cube", color=color.azure, texture="brick", scale=1)
camera.z = -10
camera_position_text = Text(text="Camera Pos = (x,y)", scale=1, x=0.1, y=0)
face_position_text = Text(text="face Pos = (x,y)", scale=1, x=0.1, y=-0.1)
cube_position_text = Text(text="Cube Position Pos = (x,y)", scale=1, x=0.1, y=-0.2)
camera_rotation_text = Text(text="camera rotation = (x,y)", scale=1, x=0.1, y=-0.3)


def update_position_text():
    x_pos = requests.get("http://127.0.0.1:5000/get_x")
    y_pos = requests.get("http://127.0.0.1:5000/get_y")

    if (x_pos.status_code == 200 and y_pos.status_code == 200):
        x_pos, y_pos = x_pos.text, y_pos.text
        x_pos, y_pos = float(x_pos), float(y_pos)

        scaled_x = 3 * (x_pos - (640 / 2)) / 640
        scaled_y = 3 * (y_pos - (480 / 2)) / 480

        face_position_text.text = f"Face position = ({scaled_x}, {scaled_y})"
        move_camera_x_y(-scaled_x, -scaled_y)


def move_camera_x_y(x, y):
    camera.x = x
    camera.y = y


def move_camera():
    camera.x += held_keys['d'] * 0.1
    camera.x -= held_keys['a'] * 0.1

    camera.y += held_keys['w'] * 0.1
    camera.y -= held_keys['s'] * 0.1

    camera_position_text.text = f"Camera Pos = ({round(camera.x, 4)}, {round(camera.y,4)}, {round(camera.z, 4)})"


def rotate_camera():
    x, y, z = camera.x, camera.y, 40
    # Calculate the rotation of the camera along the x and y to get to the origin (0,0,0)
    if x == 0 or y == 0:
        return

    rotate_x = (math.atan(x/z) * (180/3.14159265))
    rotate_y = (math.atan(y/z) * (180/3.14159265))

    # Rotate the camera accordingly
    camera.rotation_x = rotate_x
    camera.rotation_x = rotate_y

    camera_rotation_text.text = f"({rotate_x} , {rotate_y})"
    # what i need is the angle between (0,0,1) and the (x,y,1)



def update():
    # handle the update
    move_camera()
    update_position_text()
    cube_position_text.text = f"Cube Pos = ({cube.x},{cube.y}, {cube.z})"
    rotate_camera()

app.run()


