#!/usr/bin/env python3

# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
from flask import Flask
from flask import render_template
from flask import redirect
from subprocess import call
app = Flask(__name__)
app.debug = True

from a_star import AStar
from lsm6 import LSM6DS33

a_star = AStar()
a_star.set_defaults()

lsm6 = LSM6DS33()
'''
    

    raw_acc_x = lsmd.read_raw_accel_x()
    raw_acc_y = lsmd.read_raw_accel_y()
    raw_acc_z = lsmd.read_raw_accel_z()
    '''

import json

led0_state = False
led1_state = False
led2_state = False

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/status.json")
def status():
    buttons = a_star.read_buttons()
    analog = read_acc_and_gyro()
    battery_millivolts = a_star.read_battery_millivolts()
    encoders = a_star.read_encoders()
    x_angle, y_angle = read_x_y_angles()
    data = {
        "buttons": buttons,
        "battery_millivolts": battery_millivolts,
        "analog": analog,
        "encoders": encoders,
        "x_angle": x_angle,
        "y_angle": y_angle
    }
    return json.dumps(data)


def read_acc_and_gyro():
    values = [lsm6.read_scaled_g_accel_x(),
              lsm6.read_scaled_g_accel_y(),
              lsm6.read_scaled_g_accel_z(),
              lsm6.read_raw_gyro_x(),
              lsm6.read_raw_gyro_y(),
              lsm6.read_raw_gyro_z()]
    return values


def read_x_y_angles():
    return lsm6.calc_x_y_angles_from_acc()


@app.route("/motors/<left>,<right>")
def motors(left, right):
    a_star.motors(int(left), int(right))
    return ""

@app.route("/leds/<int:led0>,<int:led1>,<int:led2>")
def leds(led0, led1, led2):
    a_star.leds(led0, led1, led2)
    global led0_state
    global led1_state
    global led2_state
    led0_state = led0
    led1_state = led1
    led2_state = led2
    return ""

@app.route("/heartbeat/<int:state>")
def hearbeat(state):
    if state == 0:
      a_star.leds(led0_state, led1_state, led2_state)
    else:
        a_star.leds(not led0_state, not led1_state, not led2_state)
    return ""

@app.route("/play_notes/<notes>")
def play_notes(notes):
    a_star.play_notes(notes)
    return ""

@app.route("/halt")
def halt():
    call(["bash", "-c", "(sleep 2; sudo halt)&"])
    return redirect("/shutting-down")

@app.route("/shutting-down")
def shutting_down():
    return "Shutting down in 2 seconds! You can remove power when the green LED stops flashing."

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
