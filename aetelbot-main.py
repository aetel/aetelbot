#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram
import camara
import puerta
import luces_byte as luces
import bus
import crtm_card
import datetime
import os
import logging
from data_loader import DataLoader
from update import update_bot
import sys
import locale
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackQueryHandler
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


def new_member(bot, update, job_queue, chat_data):
    for member in update.message.new_chat_members:
        MYDIR = os.path.dirname(os.path.abspath(__file__))
        pic_dir = os.path.join(MYDIR, settings.pictures_directory)
        update.message.reply_photo(photo=open(pic_dir + '/welcome.jpg', 'rb'))
        job = job_queue.run_once(deleteMessage, 14400, context=update.message)
        chat_data['job'] = job


def load_settings():
    global settings
    global last_function_calls
    settings = DataLoader()
    last_function_calls = {}


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
    logging.info("Borrando mensaje con ID: "+str(job.context.message_id)+" en grupo con ID: "+str(job.context.chat_id))
    bot.delete_message(job.context.chat_id, message_id=job.context.message_id)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=settings.start_message)


def help(bot, update):
    log_message(update)
    bot.sendMessage(update.message.chat_id, settings.help_string, parse_mode=telegram.ParseMode.MARKDOWN)


def log_message(update):
    try:
         username = update.message.from_user.username
    except:
        username = update.message.from_user.id
    try:
        text = update.message.text
    except:
        text = "algo"
    logger.info("He recibido: \"" + text + "\" de " + username + " [ID: " + str(
    update.message.chat_id) + "]"+" en un "+update.message.chat.type)


def abrir(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid or update.message.chat_id == settings.public_chatid:
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job'] = job
        puerta.abrir()
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
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job'] = job
        user_says = " ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Luces forge attemp')
        print('Luces forge attemp')


def apagar_luz(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        luces.apagar()
        job=job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job']=job
        user_says=" ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Luces forge attemp')
        print('Luces forge attemp')


def animation(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        luces.animacion(args)
        job=job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job']=job
        user_says=" ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Luces animation forge attemp')
        print('Luces animation forge attemp')


def stop_animation(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        luces.animacion(0)
        job=job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job']=job
        user_says=" ".join(args)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL")
        logger.debug('Luces stop animation forge attemp')
        print('Luces stop animation forge attemp')


def hacer_foto(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        logging.info('Enviando foto...')
        logging.debug('Directorio imágenes: ' + settings.pictures_directory + '/image.jpg')
        mensaje_foto = camara.foto(bot, update.message.chat_id)

        if update.message.chat.type in ('group','supergroup'):
            job = job_queue.run_once(deleteMessage, 2, context=update.message)
            job = job_queue.run_once(deleteMessage, 120, context=mensaje_foto)
            chat_data['job'] = job
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de la Junta Directiva de AETEL")
        logger.debug('Camera forge attemp')
        print('Camera forge attemp')


def enviar_log(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        logging.info('Enviando log...')
        log_dir = os.path.dirname(os.path.abspath(__file__))
        #log_dir = os.path.join(log_dir, settings.pictures_directory)
        bot.send_document(chat_id=update.message.chat_id, document=open(log_dir + '/aetelbot.log', 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de la Junta Directiva de AETEL")
        logger.debug('Send log forge attemp')
        print('Send log forge attemp')


def actualizar(bot, update, args, job_queue, chat_data):
    log_message(update)
    if update.message.chat_id == settings.admin_chatid or update.message.chat_id == settings.president_chatid:
        logging.info('Actualizando bot...')
        bot.sendMessage(chat_id=update.message.chat_id, text="Be right back")
        update_bot()
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de la Junta Directiva de AETEL")
        logger.debug('Bot update forge attemp')
        print('Bot update forge attemp')


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
        mensaje_bus = bus.busE(bot, update, args, job_queue, chat_data)

    try:
        mensaje_bus
    except NameError:
        mensaje_bus = None

    try:
        bot_message
    except NameError:
        bot_message = None

    if update.message.chat.type in ('group','supergroup'):
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        if bot_message is not None:
            job = job_queue.run_once(deleteMessage, 90, context=bot_message)
        if mensaje_bus is not None:
            job = job_queue.run_once(deleteMessage, mensaje_bus[0], context=mensaje_bus[1])
        chat_data['job'] = job

def comprobar_abono(bot, update, args, job_queue, chat_data):
    log_message(update)
    tipo = args[0]
    numero = args[1]

    tarjeta = crtm_card.card_dates(tipo,numero)

    if tarjeta['renovation_date'].strftime('%Y') != '1991':
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        bot_message = bot.send_message(chat_id=update.message.chat_id, text="Tu abono caduca el "+tarjeta['renovation_date'].strftime('día %d de %B de %Y'))
    else:
        bot_message = bot.send_message(chat_id=update.message.chat_id, text="Tarjeta no válida")

def button(bot, update, job_queue, chat_data):
    query = update.callback_query
    text = query.data
    if text == '1027':
        logger.info("Comprobando parada 1027")
        mensaje_bus = bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '2603':
        logger.info("Comprobando parada 2603")
        mensaje_bus = bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '4702':
        logger.info("Comprobando parada 4702")
        mensaje_bus = bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    elif text == '4281':
        logger.info("Comprobando parada 4281")
        mensaje_bus = bus.busE(bot, update.callback_query, None, job_queue, chat_data)
    else:
        logger.info("Botón equivocado")
        print ("error")

    try:
        mensaje_bus
    except NameError:
        mensaje_bus = None

    if mensaje_bus is not None and mensaje_bus[1].chat.type in ('group','supergroup'):
        job = job_queue.run_once(deleteMessage, mensaje_bus[0], context=mensaje_bus[1])
        logger.info('Borrando mensaje '+str(mensaje_bus[1].message_id)+' en '+str(mensaje_bus[0])+' segundos')
        chat_data['job'] = job


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
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(CommandHandler('foto', hacer_foto,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('log', enviar_log,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('update', actualizar,
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
        dispatcher.add_handler(CommandHandler('apagarluz',apagar_luz,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('startanimation',animation,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('stopanimation',stop_animation,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        updater.dispatcher.add_handler(CommandHandler("bus", nuevo_bus,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        updater.dispatcher.add_handler(CommandHandler("abono", comprobar_abono,
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

        # Bienvenida a nuevos miembros
        updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member,pass_job_queue=True,pass_chat_data=True))

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
