#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
from logger import get_logger
import untangle

settings = DataLoader()
logger = get_logger("bus")
logger.setLevel(0)


runner_emoji = u'\U0001F3C3'
sad_emoji = u'\U0001F625'
working = u'\U000026A0'
bus_emoji = u'\U0001F68C'

def busE(bot, update):
    parada_numero = update.message.text
    parada_link = (settings.url_emt_inicio+parada_numero+settings.url_emt_final)
    parada_nombre = ('E')
    #print (parada_link)
    print (emt(parada_nombre,parada_link))
    bot.send_message(update.message.chat_id,emt(parada_nombre,parada_link))

#Esta función es de Carlos Cansino
def emt(bus,url):#Funcion que comprueba el tiempo restante del ultimo bus, pasando como parametros el numero de linea y la parada

    parsed_data = untangle.parse(url)

    #Comprobamos que haya algun bus disponble en la parada
    lista1 = parsed_data.Arrives
    if lista1 =="":
        return (bus_emoji + " Linea " + bus + " no disponible.")

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
            return bus_emoji + " Linea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " Queda menos de 1 minuto. Se encuentra a " + distance[lines.index(bus)] + " metros. " + runner_emoji + runner_emoji
        elif min==0:
            return bus_emoji +" Linea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " Está en la parada " + sad_emoji + sad_emoji
        else:
            return bus_emoji +" Linea " + lines [lines.index(bus)] + " destino " + destination[lines.index(bus)] + " Quedan " + str(min) + " minutos. Se encuentra a " + distance[lines.index(bus)] + " metros."
    #Si no esta sacamos un error de no disponible
    else:
        return (bus_emoji + " Linea " + bus + " no disponible.")


if __name__ == "__main__":
    print ("Bienvenido, vamo a ver cuando llega el bus.")
