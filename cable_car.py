#!/usr/bin/python3
# so that script can be run from Brickman
# Version 1.0

import sys, os, time
import paho.mqtt.client as mqtt
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

leds = Leds()
ma = LargeMotor(OUTPUT_A)
md = LargeMotor(OUTPUT_D)

IP_MQTT_Broker = "xxxxxxxx"
USERNAME = "xxxxxxxx"
KEY = "xxxxxxxx"

def go():
    leds.set_color("LEFT", "RED")
    leds.set_color("RIGHT", "RED")
    ma.duty_cycle_sp = -50
    md.duty_cycle_sp =  50
    ma.run_direct()
    md.run_direct()

def stop():
    leds.set_color("LEFT", "GREEN")
    leds.set_color("RIGHT", "GREEN")
    ma.stop(stop_action="hold")
    md.stop(stop_action="hold")

def back():
    leds.set_color("LEFT", "ORANGE")
    leds.set_color("RIGHT", "ORANGE")
    ma.duty_cycle_sp =  10
    md.duty_cycle_sp = -10
    ma.run_direct()
    md.run_direct()

def command_reciever():
    global IP_MQTT_Broker, USERNAME, KEY

    # This is the Subscriber
    def on_connect(client, userdata, flags, respons_code):
        print('status {0}'.format(respons_code))
        client.subscribe("xxxxxxxx/xxxxxxxx")

    def on_message(client, userdata, msg):
        PAYLOAD_STR = str(msg.payload,'utf-8')
        print(msg.topic + ': ' + PAYLOAD_STR)
        if PAYLOAD_STR == "GO":
            print("go")
            go()
        elif PAYLOAD_STR == "BACK":
            print("back")
            back()
        else:
            print("stop")
            stop()

    client = mqtt.Client()
    client.username_pw_set(USERNAME, password = KEY)
    client.connect(IP_MQTT_Broker,1883,60)
    print("Connected to the MQTT Broker runnnig on " + IP_MQTT_Broker + " as a publisher.")

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

# Initialization
def init():
    md.reset()
    print('Initialized.')

# Main
if __name__ == "__main__":
    init()
    command_reciever()
