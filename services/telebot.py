from telegram.ext import Updater, CommandHandler
import logging
import os
import sqlalchemy as db
from dotenv import load_dotenv
load_dotenv()

teletoken = os.getenv('TELEGRAM_KEY')
engine = db.create_engine('mysql+mysqlconnector://root:root@localhost:3306/notification')
connection = engine.connect()
metadata = db.MetaData()
notification = db.Table('notification', metadata, autoload=True, autoload_with=engine)


# writting functionality of the command
def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    print(user_id,user_name)
    query = db.insert(notification).values(chatid=user_id, telegramtag=user_name) 
    ResultProxy = connection.execute(query) 
    message = 'Welcome to the bot',user_name   
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

updater = Updater(token=teletoken, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# give a name to the command and add it to the dispaatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()