#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
from logger import get_logger
import paho.mqtt.publish as publish

settings = DataLoader()
logger = get_logger("luces")
logger.setLevel(0)


def color_picker(args):
    if (args[0] == 'rojo'):
        color_rgb = [255,0,0]
    elif (args[0] == 'naranja'):
        color_rgb = [222, 83, 7]
    elif (args[0] == 'amarillo'):
        color_rgb = [255, 255, 0]
    elif (args[0] == 'verde'):
        color_rgb = [0, 181, 26]
    elif (args[0] == 'azul'):
        color_rgb = [0, 20, 255]
    elif (args[0] == 'indigo'):
        color_rgb = [0, 28, 200]
    elif (args[0] == 'violeta'):
        color_rgb = [118, 104, 154]
    elif (args[0] == 'cian'):
        color_rgb = [0, 191, 255]
    elif (args[0] == 'magenta'):
        color_rgb = [188, 64, 119]
    elif (args[0] == 'blanco'):
        color_rgb = [255,255,255]
    else: #RGB mode
        color_rgb = [int(args[0]),int(args[1]),int(args[2])]
    return color_rgb 


def encender(args):
    #log_message(update)
    #logger.debug("hostname: " + settings.mqtt["hostname"] + 
    #            "\n username: " + settings.mqtt["username"] + 
    #            "\n password: " + settings.mqtt["password"])
    color_rgb = color_picker(args)

    color_bytes = (bin(color_rgb[0])[2:].rjust(8, "0")+' ')
    color_bytes += (bin(color_rgb[1])[2:].rjust(8, "0")+' ')
    color_bytes += bin(color_rgb[2])[2:].rjust(8, "0")

    publish.single("setcolor", color_bytes, hostname=settings.mqtt_hostname, auth = settings.mqtt_auth)


def apagar():
    #log_message(update)
    #logger.debug("hostname: " + settings.mqtt["hostname"] + 
    #            "\n username: " + settings.mqtt["username"] + 
    #            "\n password: " + settings.mqtt["password"])
    color_rgb = [0,0,0]

    color_bytes = (bin(color_rgb[0])[2:].rjust(8, "0")+' ')
    color_bytes += (bin(color_rgb[1])[2:].rjust(8, "0")+' ')
    color_bytes += bin(color_rgb[2])[2:].rjust(8, "0")

    publish.single("setcolor", color_bytes, hostname=settings.mqtt_hostname, auth = settings.mqtt_auth)


if __name__ == "__main__":
    print ("Bienvenido, se van a encender las luces.")
