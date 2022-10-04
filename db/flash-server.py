from flask import Flask
from flask import request

app = Flask(__name__)

x_position = "0"
y_position = "0"


@app.route("/set_x")
def set_x_pos():
    global x_position
    x_pos = request.args.get('x_pos')
    x_position = x_pos
    return x_pos


@app.route("/set_y")
def set_y_pos():
    global y_position
    y_pos = request.args.get('y_pos')
    y_position = y_pos
    return y_pos


@app.route("/get_x")
def get_x():
    global x_position
    return x_position


@app.route("/get_y")
def get_y():
    global y_position
    return y_position