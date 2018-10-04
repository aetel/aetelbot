#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to send timed Telegram messages.
# This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler
import os
from random import randint
import time
import logging



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Este bot envía una foto del local de AETEL en este mismo instante. Solo funciona en el grupo de AETEL y la foto solo existe durante 1 minuto')
    print(update.message.chat_id)

def deleteCameraImage(bot, job):
    """Deleting image."""
    bot.delete_message(chat_id_AETEL, message_id=job.context)


def sendCameraImage(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    if chat_id == chat_id_AETEL:
        bala = randint(0, 3)
        if bala == 0:
            print("\n\n BANG! \n\n")
            #update.message.reply_text('BANG!')
            unban_time = time.time() + 35
            print("Time now: "+str(time.time())+"\n")
            print("Time unban: "+str(unban_time)+"\n")
            user_id = update.message.from_user.id
            caption = 'Todo lo que tiene un principio tiene un final, '+update.message.from_user.first_name
            #update.message.reply_text(caption)
            #photo_message = bot.send_photo(chat_id=chat_id, photo=open('./smith.jpeg', 'rb'), caption=caption)
            update.message.reply_photo(photo=open('./smith.jpeg', 'rb'), caption=caption)
            bot.kickChatMember(chat_id=chat_id_AETEL, user_id=user_id, until_date=unban_time)
        else:
            #bot.send_photo(chat_id=chat_id, photo='http://192.168.0.27/axis-cgi/jpg/image.cgi') #photo='https://telegram.org/img/t_logo.png')
            #os.system("wget --output-document image.jpg http://root:liderberbell@169.254.184.176/axis-cgi/jpg/image.cgi")
            os.system('ffmpeg -f avfoundation -video_size 1280x720 -framerate 30 -i "0" -vframes 1 out.jpg')
            photo_message = bot.send_photo(chat_id=chat_id, photo=open('./out.jpg', 'rb'))
            os.system('rm ./out.jpg')
            message_id = photo_message.message_id
            job = job_queue.run_once(deleteCameraImage, 3, context=message_id)
            chat_data['job'] = job
    else:
        bot.sendMessage(chat_id=chat_id, text="Este comando solo se puede usar en el grupo de AETEL")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

token_file = open('./token.txt', 'r')
token = token_file.readline()
token_file.close()

#camera = camera_file.readline()
#camera_file.close()
#chat_id_AETEL = -1001121436177
chat_id_AETEL = -1001121436177

def main():
    """Run bot."""
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ayuda", start))
    dp.add_handler(CommandHandler("camara", sendCameraImage,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
