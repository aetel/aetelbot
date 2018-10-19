#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import logging

settings = DataLoader()

def foto(bot, update, args, job_queue, chat_data):
    log_message(update)
    logging.debug('Directorio imágenes: '+settings.pictures_directory )

def take_http_screenshot():
    os.system('rm ' + settings.pictures_directory + '/snapshot.jpg')
    os.system('wget --output-document ' + settings.pictures_directory + '/snapshot.jpg ' + settings.cam_url)

if __name__ == "__main__":
    print ("Bienvenido, se va a aser una fotico.")
