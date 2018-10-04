#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import telegram
import network_scan as scan
import datetime
import time
import os
from logger import get_logger
from data_loader import DataLoader
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
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
        if ('Berbell' in lower_message) or ('berbell' in lower_message):
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


def take_http_screenshot():
    os.system('rm ' + settings.pictures_directory + '/snapshot.jpg')
    os.system('wget --output-document ' + settings.pictures_directory + '/snapshot.jpg ' + settings.cam_url)


def log_message(update):
    logger.info("He recibido: \"" + update.message.text + "\" de " + update.message.from_user.username + " [ID: " + str(
        update.message.chat_id) + "]")


def foto(bot, update, args, job_queue, chat_data):
    log_message(update)

    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        bot.send_chat_action(chat_id=update.message.chat_id, action='upload_photo')
        take_http_screenshot()
        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open(settings.pictures_directory + '/snapshot.jpg', 'rb'), reply_markup=reply_markup)
        job = job_queue.run_once(deleteMessage, 5, context=photo_message.message_id)
        job = job_queue.run_once(deleteMessage, 5, context=update.message.message_id)
        chat_data['job'] = job
        logger.debug(settings.pictures_directory + '/snapshot.jpg')


def alguien(bot, update):
    if is_call_available("alguien", update.message.chat_id, 15):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        bot.sendMessage(update.message.chat_id,
                        scan.who_is_there()[
                            0] + "\n`No podrás hacer otro /alguien hasta dentro de 15 minutos`.",
                        parse_mode="Markdown")
    else:
        bot.deleteMessage(update.message.message_id)


def puerta(bot, update, args, job_queue, chat_data):
    log_message(update)

    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        bot.sendMessage(update.message.chat_id, text="Abriendo...")
        publish.single("OPEN", "0", hostname=settings.node.puerta.hostname, auth = {'username':settings.node.puerta.username, 'password':settings.node.puerta.password})
        job = job_queue.run_once(deleteMessage, 2, context=update.message.message_id)
        chat_data['job'] = job
        print('hostname ' + settings.node.puerta.hostname + ' username: ' + settings.node.puerta.username + ' password: ' + settings.node.puerta.password)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Photo forge attemp')


def reload_data(bot, update):
    if update.message.from_user.id == settings.president_chatid:
        load_settings()
        bot.send_message(chat_id=update.message.chat_id, text="Datos cargados")


def berbell(bot, update):
    if is_call_available("berbell", update.message.chat.id, 10):
        bot.send_message(chat_id=update.message.chat_id, text="¡Berbell Imperio!")
        bot.sendSticker(update.message.chat_id, u'CAADBAADyAADD2LqAAEgnSqFgod7ggI')


def name_changer(bot, job):
    logger.info("Starting scheduled network scan.")
    try:
        if scan.is_someone_there():
            bot.setChatTitle(settings.public_chatid, u"AETEL: \U00002705 Abierto")
            logger.info("Hay alguien.")
        else:
            bot.setChatTitle(settings.public_chatid, u"AETEL: \U0000274C Cerrado")
            logger.info("No hay nadie.")
    except:
        logger.exception("Error al actualizar el nombre del grupo AETEL.")


if __name__ == "__main__":
    print("AETEL Bot: Starting...")

    logger = get_logger("bot_starter", True)
    load_settings()

    try:
        logger.info("Conectando con la API de Telegram.")
        updater = Updater(settings.telegram_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('foto', foto,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('puerta', puerta,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('alguien', alguien))
        dispatcher.add_handler(CommandHandler('reload', reload_data))
        # Inside joke
        berbell_filter = BerbellFilter()
        dispatcher.add_handler(MessageHandler(berbell_filter, berbell))
        dispatcher.add_error_handler(error_callback)
    except Exception as ex:
        logger.exception("Error al conectar con la API de Telegram.")
        quit()

    try:
        jobs = updater.job_queue
        job_name_changer = jobs.run_repeating(name_changer, 15 * 60, 300)
        logger.info("Iniciando jobs")
    except Exception as ex:
        logger.exception("Error al cargar la job list. Ignorando jobs...")

    updater.start_polling()
    logger.info("AETEL Bot: Estoy escuchando.")
    updater.idle()
