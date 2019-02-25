#!/usr/bin/env python3

# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
from flask import Flask
from flask import render_template
from flask import redirect
from subprocess import call
from a_star import AStar
from lsm6 import LSM6DS33
import json

app = Flask(__name__)
app.debug = True
a_star = AStar()
a_star.set_defaults()

lsm6 = LSM6DS33()
'''
    raw_acc_x = lsmd.read_raw_accel_x()
    raw_acc_y = lsmd.read_raw_accel_y()
    raw_acc_z = lsmd.read_raw_accel_z()
    '''

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
    current_x_angle, current_y_angle, current_z_angle = read_current_angles()

    data = {
        "buttons": buttons,
        "battery_millivolts": battery_millivolts,
        "analog": analog,
        "encoders": encoders,
        "x_angle": x_angle,
        "y_angle": y_angle,
        "current_x": current_x_angle,
        "current_y": current_y_angle,
        "current_z": current_z_angle
    }
    return json.dumps(data)


def read_acc_and_gyro():
    values = [lsm6.read_scaled_g_accel_x(),
              lsm6.read_scaled_g_accel_y(),
              lsm6.read_scaled_g_accel_z(),
              lsm6.read_scaled_dps_gyro_x(),
              lsm6.read_scaled_dps_gyro_y(),
              lsm6.read_scaled_dps_gyro_z()]
    return values


def read_x_y_angles():
    return lsm6.calc_x_y_angles_from_acc_degrees()


def read_current_angles():
    x = lsm6.read_current_gyro_degrees_x()
    y = lsm6.read_current_gyro_degrees_y()
    z = lsm6.read_current_gyro_degrees_z()
    print("x: {}, y: {} z: {}".format(x, y, z))

    return x, y, z


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
def heartbeat(state):
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


# def calc_tilt_angle():


'''
/********************************************************************
* Complimentary Filter
********************************************************************/
float filterAngle;
float dt=0.02;

float comp_filter(float newAngle, float newRate) {

float filterTerm0;
float filterTerm1;
float filterTerm2;
float timeConstant;

timeConstant=0.5; // default 1.0

filterTerm0 = (newAngle - filterAngle) * timeConstant * timeConstant;
filterTerm2 += filterTerm0 * dt;
filterTerm1 = filterTerm2 + ((newAngle - filterAngle) * 2 * timeConstant) + newRate;
filterAngle = (filterTerm1 * dt) + filterAngle;

return previousAngle; // This is actually the current angle, but is stored for the next iteration
}
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0")
