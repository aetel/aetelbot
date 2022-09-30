"""
The different dispatchers for the bot are located in this file
"""
from random import randint
import config
import helpers
import json


def start(bot, update, text=""):
    """/start->Starts the bot by sending a message to the chat.

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
        text (str): Message to send. Overwrites the message stored in settings.
    """
    if text =="":
        text=config.start_msg
    bot.send_message(chat_id=update.message.chat_id, text=text)


def help(bot, update, text=""):
    """/help->Sends a help message when asked

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
        text (str): Message to send. Overwrites the message stored in settings.
    """
    #bot.sendMessage(update.message.chat_id, text, parse_mode=telegram.ParseMode.MARKDOWN)
    if text =="":
        text=config.help_msg
    bot.sendMessage(update.message.chat_id, text)

def deleteMessage(bot, job):
    """Deletes the message that is passed in the "job" arg

    Args:
        bot (TelegramBot): bot
        job (TelegramJob): job containing the message to delete
    """
    print("MSG ID TO DELETE ->"+str(job.context.message_id))
    bot.delete_message(job.context.chat_id, message_id=job.context.message_id)

def openDoorRequest(bot, update, job_queue, chat_data):
    """Opens the AETEL door by sending an specific
       mqtt message to the door controller.

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
        job_queue (TelegramJobQueue): JobQueue to be able to execute "deleteMessage" job after 2 sec
        chat_data (TelegramChatData): Telegram chat data
    """
    #Obtener los usuarios que tienen acceso a la puerta
    with open('allowed_access_door.json') as f:
        users = json.load(f)

    print("Este mensajito es de: "+str(update.message.from_user.username) + " del grupo: "+str(update.message.chat_id))
    if update.message.chat_id in config.allowed_chats_id and update.message.from_user.username in users["allowed_usernames"]:
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        chat_data['job'] = job
        helpers.open_door()
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Este comando solo se puede usar en el grupo de AETEL y personas que hayan pagado la cuota, no me seas pillín...")
        job = job_queue.run_once(deleteMessage, 5, context=update.message)
        chat_data['job'] = job

def checkDoorRequest(bot,update,job_queue,chat_data):
    """
    Checks if the door mqtt system is online or not
    """
    #Obtener los usuarios que tienen acceso a la puerta
    with open('allowed_access_door.json') as f:
        users = json.load(f)
    
    if update.message.chat_id in config.allowed_chats_id and update.message.from_user.username in users["allowed_usernames"]:
        door_status=helpers.check_door_status()
        msg_sent=bot.sendMessage(chat_id=update.message.chat_id, text="El status de la puerta es: "+str(door_status, 'utf-8'))
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        job = job_queue.run_once(deleteMessage, 10, context=msg_sent)
        chat_data['job'] = job

def rebootDoorRequest(bot,update,job_queue,chat_data):
    """
    Reboot door mqtt device if it hangs
    """
    #Obtener los usuarios que tienen acceso a la puerta
    with open('allowed_access_door.json') as f:
        users = json.load(f)
    
    if update.message.chat_id in config.allowed_chats_id and update.message.from_user.username in users["allowed_usernames"]:
        helpers.reboot_door()
        msg_sent=bot.sendMessage(chat_id=update.message.chat_id, text="La puerta se está reiniciando...Paz+Ciencia")
        job = job_queue.run_once(deleteMessage, 2, context=update.message)
        job = job_queue.run_once(deleteMessage, 10, context=msg_sent)
        chat_data['job'] = job

def new_member(bot, update, job_queue, chat_data):
    """Sends the welcome picture whenever a new user enters the group.
       Also sets a job to delete that picture after 240 minutes.

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
        job_queue (TelegramJobQueue): JobQueue to be able to execute "deleteMessage" job after 14400 sec
        chat_data (TelegramChatData): Telegram chat data
    """
    for member in update.message.new_chat_members:
        update.message.reply_photo(photo=open(config.images + '/welcome.jpg', 'rb'))
        job = job_queue.run_once(deleteMessage, 14400, context=update.message)
        chat_data['job'] = job

def send_nepe(bot, update, job_queue):
    """Sends nepe picture to the group. It also checks if the user has enough nepe points to send it

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
    """

    #print("Attempting send nepe...")
    if helpers.cooldown(1):
         
        """
        Here we need to find the user that is asking, then search in the inside_variables if 
        the user has "tickets" for sending nepe, if yes, send and reduce ticket. If not, inform the user and 
        return to the main execution normally.
        """
	
        
        msg_id = update.message.message_id
        first_name = update.message.chat.first_name
        last_name = update.message.chat.last_name
        username = update.message.from_user.username
			
        #print(update.message)
        try:
            if update.message.entities[0].type == 'bot_command':
                return
        except:
            pass
		
        for k,v in config.users.items():
            if k == username:
                if v<=0:
                    rand=randint(0,7)
                    if rand==0:
                        msg_sent=bot.sendMessage(update.message.chat_id,"¿Dónde están tus nepePoints compañero?", reply_to_message_id=msg_id)
                    if rand==1:
                        msg_sent=bot.sendMessage(update.message.chat_id,"Ejem...No tickets no juego...", reply_to_message_id=msg_id)
                    if rand==2:
                        msg_sent=bot.sendMessage(update.message.chat_id,"No te lo voy a mandar, te has portado mal y te ha tocado carbón...", reply_to_message_id=msg_id)
                    if rand==3:
                        msg_sent=bot.sendMessage(update.message.chat_id,"¿Y tus nepePoints?", reply_to_message_id=msg_id)
                    if rand==4:
                        msg_sent=bot.sendMessage(update.message.chat_id,"No tan rápido camarada... Necesitas nepePoints para eso...", reply_to_message_id=msg_id)
                    if rand==5:
                        msg_sent=bot.sendMessage(update.message.chat_id,"No te voy a dar el placer, pero me has caido bien, te digo: nepe", reply_to_message_id=msg_id)
                    if rand==6:
                        msg_sent=bot.sendMessage(update.message.chat_id,"Tus nepePoints ya son negativos....para de intentarlo", reply_to_message_id=msg_id)
                    if rand==7:
                        msg_sent=bot.sendMessage(update.message.chat_id,"¿Enserio te pensabas que iba a colar?", reply_to_message_id=msg_id)
                else:
                    config.users[username]=v-1
                    msg_sent=bot.sendSticker(update.message.chat_id, "https://i.ibb.co/th3L8cw/Aetel-logo.webp")#send nepe
        job = job_queue.run_once(deleteMessage, 28800, context=msg_sent)

def checkNepePoints(bot, update, job_queue, chat_data):
    """Checks the nepePoints of the user who is asking for it.
        If user is not found in the list, no answer is made.

    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
    """
    print("ChecknepePoints")
    
    username = update.message.from_user.username
    #print(type(username))
    #print("message->"+str(username))
    msg_id = update.message.message_id
    #print(update)
    
    for k,v in config.users.items():
        if k == username:
            msg_sent=bot.sendMessage(update.message.chat_id,"Tus puntos nepe son: ("+str(v)+") !!", reply_to_message_id=msg_id)
            #print("MSG-SENT->"+str(msg_sent))
            job = job_queue.run_once(deleteMessage, 8, context=update.message)
            job = job_queue.run_once(deleteMessage, 10, context=msg_sent)
            chat_data['job'] = job
        else: #Ask administrators to add you to the list	
            pass

def giveNepePoints(bot, update, job_queue, chat_data):
    """
    Gives nepePoints to the user. It must be used in this-> /give @user num_puntos
    Args:
        bot (TelegramBot): bot
        update (TelegramUpdater): updater
    """
    print("GivenepePoints")
    
    username = update.message.from_user.username
    msg_id = update.message.message_id
    if username not in config.allowed_usernames:
        rand=randint(0,4)
        if rand==0:
            msg_sent=bot.sendMessage(update.message.chat_id,"Usted no tiene ninguna autoridad sobre mí!", reply_to_message_id=msg_id)
        if rand==1:
            msg_sent=bot.sendMessage(update.message.chat_id,"Cuando seas mayor comerás huevos...", reply_to_message_id=msg_id)
        if rand==2:
            msg_sent=bot.sendMessage(update.message.chat_id,"Nope", reply_to_message_id=msg_id)
        if rand==3:
            msg_sent=bot.sendMessage(update.message.chat_id,"Nop", reply_to_message_id=msg_id)
        if rand==4:
            msg_sent=bot.sendMessage(update.message.chat_id,"Comando para admins!", reply_to_message_id=msg_id)
        job = job_queue.run_once(deleteMessage, 8, context=msg_sent)
    else:
        msg_text=update.message.text
        splitted=msg_text.split(" ")
        print(splitted[1][1:])
        for k,v in config.users.items():
            if k == splitted[1][1:]:
                print("User "+str(k)+" now has " +str(config.users[k]))
                config.users[k]=int(config.users[k])+int(splitted[2])
                print("User "+str(k)+" now has "+str(config.users[k]))
                rand=randint(0,2)
                if rand==0:
                    msg_sent=bot.sendMessage(update.message.chat_id,"Okele colegui", reply_to_message_id=msg_id)
                if rand==1:
                    msg_sent=bot.sendMessage(update.message.chat_id,"Oido cocina", reply_to_message_id=msg_id)
                if rand==2:
                    msg_sent=bot.sendMessage(update.message.chat_id,"Marchando!", reply_to_message_id=msg_id)
                job = job_queue.run_once(deleteMessage, 8, context=msg_sent)
        #print("MSG-SENT->"+str(msg_sent))
        job = job_queue.run_once(deleteMessage, 5, context=update.message)

        chat_data['job'] = job
        
def giveAccessDoor(bot, update, job_queue, chat_data):
    username = update.message.from_user.username
    msg_id = update.message.message_id

    if username in config.allowed_usernames:
        msg_text = update.message.text
        splitted = msg_text.split(" ")

        with open ('allowed_access_door.json', 'r') as outfile:
            users = json.load(outfile)
        if splitted[1][1:] not in users["allowed_usernames"]:
            users["allowed_usernames"].append(splitted[1][1:])
            with open ('allowed_access_door.json', 'w') as outfile:
                json.dump(users, outfile)

    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Buen intento...")

    job = job_queue.run_once(deleteMessage, 2, context=update.message)
    chat_data['job'] = job

def revokeAccessDoor(bot, update, job_queue, chat_data):
    username = update.message.from_user.username
    msg_id = update.message.message_id

    if username in config.allowed_usernames:
        msg_text = update.message.text
        splitted = msg_text.split(" ")

        with open ('allowed_access_door.json', 'r') as outfile:
            users = json.load(outfile)

        if splitted[1][1:] in users["allowed_usernames"]:
            users["allowed_usernames"].remove(splitted[1][1:])

            with open ('allowed_access_door.json', 'w') as outfile:
                json.dump(users, outfile)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="No tienes accesso chaval")
    job = job_queue.run_once(deleteMessage, 2, context=update.message)
    chat_data['job'] = job

def printAccessDoor(bot, update, job_queue, chat_data):
    username = update.message.from_user.username
    msg_id = update.message.message_id

    if username in config.allowed_usernames:
        msg_text = update.message.text
        splitted = msg_text.split(" ")

        with open ('allowed_access_door.json', 'r') as outfile:
            users = json.load(outfile)

        bot.sendMessage(chat_id=update.message.chat_id, text=' '.join(users["allowed_usernames"]))
    job = job_queue.run_once(deleteMessage, 2, context=update.message)
    chat_data['job'] = job
