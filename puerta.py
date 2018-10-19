#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import logging
import paho.mqtt.publish as publish

settings = DataLoader()

def abrir():
    logging.debug("hostname: " + settings.mqtt_hostname + 
                "\n username: " + settings.mqtt_auth["username"] + 
                "\n password: " + settings.mqtt_auth["password"])
    logging.info('Abriendo puerta...')
    publish.single("cmnd/PUERTA/POWER", "1", hostname = settings.mqtt_hostname, auth = settings.mqtt_auth)

if __name__ == "__main__":
    print ("Bienvenido, se va a abrir la porta.")
