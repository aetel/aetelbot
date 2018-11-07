#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import logging
import untangle

settings = DataLoader()

def busE(bot, update, args, job_queue, chat_data):
    if args == None:
        parada_numero = update.data
        bus_nombre = 'E'
    else:
        parada_numero = args[1]
        bus_nombre = args[0]
    parada_link = (settings.url_emt_inicio+parada_numero+settings.url_emt_final)
    logging.info('Contacting the EMT API... Bus: '+bus_nombre+' Parada: '+parada_numero)
    logging.debug(emt(bus_nombre,parada_link))

    if args == None:
        bot.edit_message_text(text=emt(bus_nombre,parada_link),
                          chat_id=update.message.chat_id,
                          message_id=update.message.message_id)
    else:
        bot.send_message(update.message.chat_id,emt(bus_nombre,parada_link))

#Esta función es de Carlos Cansino

runner_emoji = u'\U0001F3C3'
sad_emoji = u'\U0001F625'
bus_emoji = u'\U0001F68C'

def emt(bus,url):#Funcion que comprueba el tiempo restante del ultimo bus, pasando como parametros el numero de linea y la parada

    parsed_data = untangle.parse(url)

    #Comprobamos que haya algun bus disponble en la parada
    lista1 = parsed_data.Arrives
    if lista1 =="":
        logging.info('No hay ningún bus disponible.')
        return (bus_emoji + " Línea " + bus + " no disponible.")

    lista = parsed_data.Arrives.Arrive

    #Array con los numeros de linea ordenados
    lines = [str(Arrive.idLine.cdata) for Arrive in lista]

    #Array con los tiempo de llegada ordenados
    time = [int(Arrive.TimeLeftBus.cdata)for Arrive in lista]

    #Array con la distacia a la parada ordenados
    distance =[str(Arrive.DistanceBus.cdata)for Arrive in lista]

    #Array con los destinos de los buses ordenados
    destination =[str(Arrive.Destination.cdata)for Arrive in lista]


    #Buscamos la posicion del bus "bus" en la lista
    #Si el bus está en la lista lo indicamos
    if (bus in lines):
        min = int (time[lines.index(bus)]/60)
        #Segun el tiempo restante cambia el texto de salida
        if min==1:
            return bus_emoji + " Línea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " queda menos de 1 minuto. " + runner_emoji + runner_emoji
        elif min==0:
            return bus_emoji +" Línea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " está en la parada. " + sad_emoji + sad_emoji
        else:
            return bus_emoji +" Línea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " quedan " + str(min) + " minutos."
    #Si no esta sacamos un error de no disponible
    else:
        return (bus_emoji + " Línea " + bus + " no disponible.")


if __name__ == "__main__":
    print ("Bienvenido, vamo a ver cuando llega el bus.")
