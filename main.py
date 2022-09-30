import telegram
import helpers 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackQueryHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import config
import bot_functions as bot

def main():
    """
    Start the bot subroutine!
    """
    logger= helpers.Logger()
    try:
        #connecting with Telegram API
        updater = Updater(config.telegram_token)
        dispatcher = updater.dispatcher
              
        
        #Different dispatchers for different commands
        dispatcher.add_handler(CommandHandler('start', bot.start))
        dispatcher.add_handler(CommandHandler('help', bot.help))
        dispatcher.add_handler(CommandHandler('puerta', bot.openDoorRequest,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        #Commands related to Nepe Points
        dispatcher.add_handler(CommandHandler('check', bot.checkNepePoints,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('give', bot.giveNepePoints,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        #Commands related to door access
        dispatcher.add_handler(CommandHandler('access', bot.giveAccessDoor,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('revoke', bot.revokeAccessDoor,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('printAccess', bot.printAccessDoor,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        #Command to check status of door mqtt device
        dispatcher.add_handler(CommandHandler('puerta_status', bot.checkDoorRequest,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        dispatcher.add_handler(CommandHandler('puerta_reboot', bot.rebootDoorRequest,
                                              pass_args=False,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        # Send nepe picture when asked
        filterByWord = helpers.FilterByContainingNepe()
        dispatcher.add_handler(MessageHandler(filterByWord, bot.send_nepe,pass_job_queue=True))
        #dispatcher.add_error_handler(error_callback)
        updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, bot.new_member,pass_job_queue=True,pass_chat_data=True))
        
        #Add error handling via Logging
        dispatcher.add_error_handler(logger)
    except Exception as e:
        pass
        print(e)
        quit()
    try:
        jobs = updater.job_queue
        #logger.info("Iniciando jobs")
    except Exception as e:
        #logger.exception("Error al cargar la job list. Ignorando jobs...")
        print(e)
        pass

    #Here is where the bot keeps listening
    updater.start_polling()
    #logger.info("aetelbot a la escucha...")
    updater.idle()

if __name__ == "__main__":
    main()
