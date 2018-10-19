#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data_loader import DataLoader

settings = DataLoader()

def foto(bot, update, args, job_queue, chat_data):
    os.system('wget -nv --output-document ' + pictures_directory + '/image.jpg ' + settings.cam_url)
    photo_message = bot.send_photo(chat_id=chat_id, photo=open('./'+settings.pictures_directory + '/image.jpg', 'rb'))
    os.system('rm ' + settings.pictures_directory + '/image.jpg')
    job = job_queue.run_once(deleteMessage, 5, context=photo_message.message_id)
    job = job_queue.run_once(deleteMessage, 5, context=update.message.message_id)

if __name__ == "__main__":
    print ("Bienvenido, se va a aser una fotico.")
