#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import struct
import paho.mqtt.publish as publish

settings = DataLoader()


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
    elif (args[0] == 'off'):
        color_rgb = [0,0,0]
    else: #RGB mode
        color_rgb = [int(args[0]),int(args[1]),int(args[2])]
    return color_rgb 


def cambiar(args):
    color_rgb = color_picker(args)

    # Ejemplo verde [0, 181, 26]
    # '\x00\x00\x00\x00\x00\x00\x00\xb5\x00\x00\x00\x1a'
    color_bytes = struct.pack('>iii', color_rgb[0], color_rgb[1], color_rgb[2])
    publish.single("setcolor", color_bytes, hostname = settings.mqtt_hostname, auth = settings.mqtt_auth)


if __name__ == "__main__":
    print ("Bienvenido, se van a encender las luces.")
