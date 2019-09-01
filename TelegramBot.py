from config import TELEGRAM_BOT_TOKEN, tags, times, main_menu
import logging
import telegram
import schedule
from feedHandler import get_timed_digest, get_immediately_digest
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from utils import divide_chunks
from datetime import time

updater = Updater(token=TELEGRAM_BOT_TOKEN,use_context=True)
j = updater.job_queue

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)






def timed_digest_sender(context: telegram.ext.CallbackContext):
    chat_id = context.job.context[0]
    user_data = context.job.context[1]
    digest = get_timed_digest(user_data['categories'], user_data['time'])
    for item in digest:
       context.bot.send_message(chat_id=chat_id, text="{}\n{}".format(item['title'],item['link']))

def digest_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    setted_time = context.user_data['time']
    daily_time = time(int(setted_time[:2]), int(setted_time[3:]))
    context.job_queue.run_daily(timed_digest_sender, time = daily_time, context=[update.message.chat_id,context.user_data])
    context.bot.send_message(chat_id=update.message.chat_id, 
                text="🙌 Ви щойно підписались на отримання щоденного дайджесту!")







def categories_handler(update, context):
    if update.message.text in tags:
        context.user_data['categories'].add(update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, 
        text="<b>Ви підписалися на категорії:</b>\n✅ {}. \n⌚ Налаштуйте час, коли ви хочете отримувати щоденний дайджест.".format(',\n✅ '.join(context.user_data['categories'])),
        parse_mode=telegram.ParseMode.HTML)

def time_handler(update, context):
    context.user_data['time'] = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, 
        text="<b>Ви підписалися на категорії:</b>\n✅ {}. \n⌚ Час отримання дайджесту: {}\n🚀 <b>Запустити отримання щоденного дайджесту:</b> /launch. ".format(',\n✅ '.join(context.user_data['categories']),context.user_data['time']),
        parse_mode=telegram.ParseMode.HTML)







def start(update, context):
    context.user_data.clear()
    context.user_data['categories']= set()
    user = update.message.from_user.first_name
    reply_markup = telegram.ReplyKeyboardMarkup(main_menu)
    context.bot.send_message(chat_id=update.message.chat_id, 
                 text="Привіт, <b>{}</b>!\nЯ <i>дайджест-бот</i> 6262.com.ua! \n• Обери категорії новин, які тебе цікавлять та час, коли хочеш їх отримувати! \n• Щоб змінити налаштування використай команду /reset".format(user), 
                 parse_mode=telegram.ParseMode.HTML,
                 reply_markup=reply_markup)


def stop(update, context):
    pass

    

def echo(update, context):
    if update.message.text == '📆 Отримати миттєві новини за добу':
        digest = get_immediately_digest()
        for item in digest:
            context.bot.send_message(chat_id=update.message.chat_id, 
                text="{}\n{}".format(item['title'],item['link']))

    if update.message.text == '◀ Назад':
        custom_keyboard = divide_chunks(main_menu,2)
        reply_markup = telegram.ReplyKeyboardMarkup(main_menu)
        context.bot.send_message(chat_id=update.message.chat_id, 
                 text="Головне меню", 
                 reply_markup=reply_markup)

        
    if update.message.text =='📌 Налаштувати категорії':
        custom_keyboard = divide_chunks(tags, 2)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.message.chat_id, 
                 text="Обирайте категорії новин", 
                 reply_markup=reply_markup)


    if update.message.text =='🕓 Налаштувати час':
        custom_keyboard = divide_chunks(times, 2)
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.message.chat_id, 
                 text="Оберіть час отримання дайджесту", 
                 reply_markup=reply_markup)
    

    if update.message.text =='🔧 Мої налаштування':
        if context.user_data and len(context.user_data['categories'])>0 and context.user_data.get('time') is not None:
            context.bot.send_message(chat_id=update.message.chat_id, 
                text="<b>Ви підписані на категорії:</b>\n✅ {}. \n⌚ Час отримання дайджесту: {}. \n• Змінити налаштування /reset\n".format(',\n✅ '.join(context.user_data['categories']),context.user_data['time']),
                parse_mode=telegram.ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, 
                text="⚠\nВи ще не налаштували дайджест")

    if update.message.text in tags and update.message.text!= '◀ Назад':
        categories_handler(update, context)

    if update.message.text in times and update.message.text!= '◀ Назад':
        time_handler(update, context)


 
reset_handler  = CommandHandler('reset', start)
dispatcher.add_handler(reset_handler)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

timer_handler = CommandHandler('launch', digest_timer)
dispatcher.add_handler(timer_handler)


updater.start_polling()
