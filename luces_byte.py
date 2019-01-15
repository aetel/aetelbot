#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import logging
import struct
import paho.mqtt.publish as publish

settings = DataLoader()


def color_picker(args): 
    fichero=open("Colores.txt","r")
    linea=fichero.readlines()
    for x in linea:
        if x.startswith(args[0]):
           color=x.split(' ')
           color_rgb=[int(color[1]),int(color[2]),int(color[3]),1]
           return color_rgb
    
    if (args[0] == 'rojo'):
        color_rgb = [255,0,0]
    elif (args[0] == 'naranja'):
        color_rgb = [222, 83, 7]
    elif (args[0] == 'amarillo'):
        color_rgb = [255, 255, 0]
    elif (args[0] == 'verde'):
        color_rgb = [0, 255, 0]
    elif (args[0] == 'azul'):
        color_rgb = [0, 0, 255]
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
    #log_message(update)
    logging.debug("hostname: " + settings.mqtt_hostname + 
                "\n username: " + settings.mqtt_auth["username"] + 
                "\n password: " + settings.mqtt_auth["password"])
    user_says = " ".join(args)
    if user_says != " ":
        logging.info('Cambiando el color de la luz a '+ user_says)
    else:
        logging.info('Cambiando el color de la luz')
    inicio=0
    final=633
    if(len(args)==5):
        inicio=int(args[3])
        final=int(args[4])
    color_rgb = color_picker(args)
    if(len(color_rgb)==4):
        if(len(args)==3):
            inicio=int(args[1])
            final=int(args[2])
    # Ejemplo verde [0, 181, 26]
    # '\x00\x00\x00\x00\x00\x00\x00\xb5\x00\x00\x00\x1a'
    color_rgb[0]=chr(color_rgb[0])
    color_rgb[1]=chr(color_rgb[1])
    color_rgb[2]=chr(color_rgb[2]) # Tiene que estar en char o bin. char da menos problemas. Int no vale  
    # La colocacion de los bytes la hace la siguiente funcion
    color_bytes = struct.pack('ccccccc', color_rgb[0], color_rgb[1], color_rgb[2], chr(inicio&0xFF), chr((inicio >> 8) & 0xFF), chr(final&0xFF), chr((final >> 8) & 0xFF))
    # El color debe ser codificado de la siguiente manera: byte_rojo, byte_verde, byte_azul, byte_partealta_inicio, byte_partebaja_inicio, byte_partealta_final, byte_partebaja_final
    publish.single("Fuente","1", hostname=settings.mqtt_hostname,auth=settings.mqtt_auth);
    publish.single("SetColor", color_bytes, hostname = settings.mqtt_hostname, auth = settings.mqtt_auth)


def apagar():
    publish.single("Fuente","0", hostname=settings.mqtt_hostname, auth=settings.mqtt_auth);


def animacion(args):
    logging.debug("hostname: " + settings.mqtt_hostname + 
                "\n username: " + settings.mqtt_auth["username"] + 
                "\n password: " + settings.mqtt_auth["password"])
    user_says = " ".join(args)
    if user_says != " ":
        logging.info('Cambiando animacion a '+ user_says)
    else:
        logging.info('Cambiando animacion')
    mensaje=struct.pack('c',chr(int(args[0]))) #Esto en ensamblador no pasaba, eh...
    publish.single("animacion", mensaje, hostname=settings.mqtt_hostname, auth=settings.mqtt_auth)

    
if __name__ == "__main__":
    print ("Bienvenido, se van a encender las luces.")
