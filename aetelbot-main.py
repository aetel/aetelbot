#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import telegram
import network_scan as scan
import camara
import puerta
import luces_byte as luces
import bus
import datetime
import time
import os
from data_loader import DataLoader
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, RegexHandler, ConversationHandler
from random import normalvariate
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import paho.mqtt.publish as publish

reload(sys)
sys.setdefaultencoding('utf8')

BUS, PHOTO, LOCATION, BIO = range(4)


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
    except BadRequest:
    except TimedOut:
    except NetworkError:
    except ChatMigrated as e:
    except TelegramError:


class BerbellFilter(BaseFilter):
    def filter(self, message):
        lower_message = str(message.text).lower()
        if ('berbel' in lower_message) or ('berbell' in lower_message):
            return True
        else:
            return False


def load_settings():
    global settings
    global last_function_calls
    settings = DataLoader()
    last_function_calls = {}


def is_member(bot, user_id):
    try:
        return bot.get_chat_member(chat_id=settings.admin_chatid,
                                   user_id=user_id).status in ['creator', 'administrator', 'member']
    except BadRequest:
        return False


def is_call_available(name, chat_id, cooldown):
    global last_function_calls
    now = datetime.datetime.now()
    cooldown_time = datetime.datetime.now() - datetime.timedelta(minutes=cooldown)
    if name in last_function_calls.keys():
        if chat_id in last_function_calls[name].keys():
            if last_function_calls[name][chat_id] > cooldown_time:
                last_function_calls[name][chat_id] = now
                return False
            else:
                last_function_calls[name][chat_id] = now
                return True
        else:
            last_function_calls[name] = {chat_id: now}
            return True
    else:
        last_function_calls[name] = {chat_id: now}
        return True


def deleteMessage(bot, job):
    bot.delete_message(settings.admin_chatid, message_id=job.context)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=settings.start_message)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, settings.help_string, parse_mode=telegram.ParseMode.MARKDOWN)




def alguien(bot, update):
    if is_call_available("alguien", update.message.chat_id, 15):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        bot.sendMessage(update.message.chat_id,
                        scan.who_is_there()[
                            0] + "\n`No podrás hacer otro /alguien hasta dentro de 15 minutos`.",
                        parse_mode="Markdown")
    else:
        bot.deleteMessage(update.message.message_id)


def abrir(bot, update, args, job_queue, chat_data):
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        puerta.abrir()
        job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
        chat_data['job'] = job
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        print('Puerta forge attemp')


def reload_data(bot, update):
    if update.message.from_user.id == settings.president_chatid:
        load_settings()
        bot.send_message(chat_id=update.message.chat_id, text="Datos cargados")


def berbell(bot, update):
    if is_call_available("berbell", update.message.chat.id, 10):
        bot.sendSticker(update.message.chat_id, u'CAADAgADogMAAiCxJgABuNx3vGNQs7EC')


def name_changer(bot, job):
    try:
        if scan.is_someone_there():
            bot.setChatTitle(settings.public_chatid, u"AETEL: \U00002705 Abierto")
        else:
            bot.setChatTitle(settings.public_chatid, u"AETEL: \U0000274C Cerrado")
    except:


def cambiar_luz(bot, update, args, job_queue, chat_data):
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        luces.cambiar(args)
        job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
        chat_data['job'] = job
        user_says = " ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        print('Luces forge attemp')

def nuevo_bus(bot, update, args, job_queue, chat_data):
    reply_keyboard = [['1027', '2603'], ['4702', '4281']]
    reply_markup = telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    bot_message = bot.send_message(chat_id=update.message.chat_id, 
                     text="Selecciona la parada", 
                     reply_markup=reply_markup)
    job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
    job = job_queue.run_once(deleteMessage, 2, context=bot_message.message_id)
    chat_data['job'] = job
    return BUS

if __name__ == "__main__":

    load_settings()

    try:
        updater = Updater(settings.telegram_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('foto', camara.foto,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('puerta', abrir,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('alguien', alguien))
        dispatcher.add_handler(CommandHandler('reload', reload_data))
        dispatcher.add_handler(CommandHandler('luz', cambiar_luz,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))

        # Add conversation handler with the states BUS, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('bus', nuevo_bus,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True)],
     
            states={
                BUS: [RegexHandler('^(1027|2603|4702|4281)$', bus.busE,
                                              pass_job_queue=True,
                                              pass_chat_data=True)],
            },
     
            fallbacks=[CommandHandler('bus', nuevo_bus,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True)]
        )
     
        dispatcher.add_handler(conv_handler)
        # Inside joke
        berbell_filter = BerbellFilter()
        dispatcher.add_handler(MessageHandler(berbell_filter, berbell))
        dispatcher.add_error_handler(error_callback)
    except Exception as ex:
        quit()

    try:
        jobs = updater.job_queue
        job_name_changer = jobs.run_repeating(name_changer, 15 * 60, 300)
    except Exception as ex:

    updater.start_polling()
    updater.idle()
