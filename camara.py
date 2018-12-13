#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader
import os

settings = DataLoader()

def foto(bot, chat_id):
    MYDIR = os.path.dirname(os.path.abspath(__file__))
    pic_dir = os.path.join(MYDIR, settings.pictures_directory)
    os.system('wget -nv --output-document ' + pic_dir + '/image.jpg ' + settings.cam_url)
    mensaje_foto = bot.send_photo(chat_id=chat_id, photo=open(pic_dir+ '/image.jpg', 'rb'))
    os.system('rm '+ pic_dir + '/image.jpg')
    return mensaje_foto

if __name__ == "__main__":
    print ("Bienvenido, se va a aser una fotico.")
