#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import telegram
import camara
import puerta
import luces_byte as luces
import bus
import datetime
import time
import os
import logging
from data_loader import DataLoader
import sys
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, CallbackQueryHandler
from random import normalvariate
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import paho.mqtt.publish as publish

reload(sys)
sys.setdefaultencoding('utf8')


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        logger.exception("remove update.message.chat_id from conversation list")
    except BadRequest:
        logger.exception("handle malformed requests - read more below!")
    except TimedOut:
        logger.exception("handle slow connection problems")
    except NetworkError:
        logger.exception("handle other connection problems")
    except ChatMigrated as e:
        logger.exception("the chat_id of a group has changed, use " + e.new_chat_id + " instead")
    except TelegramError:
        logger.exception("There is some error with Telegram")


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
    log_message(update)
    bot.sendMessage(update.message.chat_id, settings.help_string, parse_mode=telegram.ParseMode.MARKDOWN)


def log_message(update):
    logger.info("He recibido: \"" + update.message.text + "\" de " + update.message.from_user.username + " [ID: " + str(
        update.message.chat_id) + "]")


def abrir(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        puerta.abrir()
        job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
        chat_data['job'] = job
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Puerta forge attemp')
        print('Puerta forge attemp')


def reload_data(bot, update):
    log_message(update)
    if update.message.from_user.id == settings.president_chatid:
        load_settings()
        bot.send_message(chat_id=update.message.chat_id, text="Datos cargados")


def berbell(bot, update):
    if is_call_available("berbell", update.message.chat.id, 10):
        bot.sendSticker(update.message.chat_id, u'CAADAgADogMAAiCxJgABuNx3vGNQs7EC')


def cambiar_luz(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        luces.cambiar(args)
        job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
        chat_data['job'] = job
        user_says = " ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Luces forge attemp')
        print('Luces forge attemp')

def nuevo_bus(bot, update, args, job_queue, chat_data):
    log_message(update)
    if not args:
        keyboard = [[InlineKeyboardButton("1027", callback_data='1027'),
                     InlineKeyboardButton("2603", callback_data='2603')],
                    [InlineKeyboardButton("4702", callback_data='4702'),
                     InlineKeyboardButton("4281", callback_data='4281')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot_message = bot.send_message(chat_id=update.message.chat_id, text="Selecciona la parada:", reply_markup=reply_markup)
    else:
        bus.busE(bot, update, args, job_queue, chat_data)
        bot_message = bot.send_message(chat_id=update.message.chat_id, text="Buscando próximo bus...")
        job = job_queue.run_once(deleteMessage, 2, context=bot_message.message_id)
    job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
    chat_data['job'] = job

def button(bot, update, job_queue, chat_data):
    query = update.callback_query
    text =query.data
    if text == '1027':
    	logger.info("Comprobando parada 1027")
        bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '2603':
    	logger.info("Comprobando parada 2603")
        bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '4702':
    	logger.info("Comprobando parada 4702")
        bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '4281':
    	logger.info("Comprobando parada 4281")
        bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    else:
    	logger.info("Botón equivocado")
        print ("error")


if __name__ == "__main__":

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename='aetelbot.log',
                        level=logging.INFO,
                        format='%(asctime)s %(message)s', 
                        filemode='w')
    logging.getLogger().addHandler(logging.StreamHandler())

    logger = logging.getLogger(__name__)
    logger.info("Current PID:"+str(os.getpid()))
    logger.info("aetelbot arrancando...")
    load_settings()

    try:
        logger.info("Conectando con la API de Telegram.")
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
        dispatcher.add_handler(CommandHandler('reload', reload_data))
        dispatcher.add_handler(CommandHandler('luz', cambiar_luz,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        updater.dispatcher.add_handler(CommandHandler("bus", nuevo_bus,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        updater.dispatcher.add_handler(CallbackQueryHandler(button,
        									  pass_job_queue=True,
                                              pass_chat_data=True))
        # Inside joke
        berbell_filter = BerbellFilter()
        dispatcher.add_handler(MessageHandler(berbell_filter, berbell))
        dispatcher.add_error_handler(error_callback)
    except Exception as ex:
        logger.exception("Error al conectar con la API de Telegram.")
        quit()

    try:
        jobs = updater.job_queue
        logger.info("Iniciando jobs")
    except Exception as ex:
        logger.exception("Error al cargar la job list. Ignorando jobs...")

    updater.start_polling()
    logger.info("aetelbot a la escucha...")
    updater.idle()
