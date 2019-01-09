#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import logging
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import dateutil.parser as dparser

settings = DataLoader()
card = {
    "card_no":"",
    "subscription_type":"",
    "subscription_age":"",
    "load_date":"",
    "valid_date":"",
    "first_use":"",
    "renovation_date":""}

def card_dates(tipo, numero):
    cod = []
    cod.append(tipo)
    logging.info('Buscando datos de la tarjeta CRTM '+tipo+' '+numero)
    browser = Browser()
    response = browser.open('http://tarjetatransportepublico.crtm.es/CRTM-ABONOS/consultaSaldo.aspx')
    if response.code == 200: # Comprueba que la página responde
        browser.select_form("aspnetForm")         # Selecciona el formulario
        browser["ctl00$cntPh$txtNumTTP"] = numero # Rellena los datos de la tarjeta
        browser["ctl00$cntPh$dpdCodigoTTP"] = cod
        page = browser.submit(name="ctl00$cntPh$btnConsultar")  # "Pulsa" el boton de Continuar

        soup = BeautifulSoup(page.read())
        card_no = soup.findAll('span', attrs={"id" : 'ctl00_cntPh_lblNumeroTarjeta'}) # Busca el número completo de la tarjeta
        results = soup.findAll('div', attrs={"id" : 'ctl00_cntPh_tableResultados'}) # Busca los datos de validez de la tarjeta
        spans = results[0].findAll('span') # Separa los datos

        card["card_no"] = card_no[0].renderContents()
        card["subscription_age"] = spans[1].text
        card["load_date"] = dparser.parse(spans[2].text, fuzzy=True, dayfirst=True)
        card["valid_date"] = dparser.parse(spans[3].text, fuzzy=True, dayfirst=True)
        card["first_use"] = dparser.parse(spans[4].text, fuzzy=True, dayfirst=True)
        card["renovation_date"] = dparser.parse(spans[5].text, fuzzy=True, dayfirst=True)

        return card
    else:
        logging.info("La página del CRTM no está disponible")

if __name__ == "__main__":
    print ("Bienvenido, vamo a ver cuando llega el bus.")
