
# A very simple Flask Hello World app for you to get started with...

from telegram.ext import CommandHandler, CallbackQueryHandler,Updater,MessageHandler, Filters,Dispatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Bot,Update
from get_data import get_states_data
from flask import Flask, request
from api_token import API_TOKEN
import json
import requests

#handlers
def start(update,context):
    update.message.reply_text(main_menu_message(),reply_markup=main_menu_keyboard())

def main_menu(update,context):
    query=update.callback_query
    query.answer()
    query.edit_message_text(
        text=main_menu_message(),
        reply_markup=main_menu_keyboard()
    )

def first_menu(update,context):
    query=update.callback_query
    query.answer()
    query.edit_message_text(
        text=first_menu_text(),
        reply_markup=first_menu_keyboard()
    )

def word_game(update,context):
    query=update.callback_query
    query.answer() #planned game
    query.edit_message_text(
        text='Lets start the word game.\nBtw whats ur name??',
        reply_markup=back_home_keyboard()
    )

def ret_num(update,context):
    query=update.callback_query
    state=query.data
    data=get_states_data()
    data=data.get(state)
    query.edit_message_text(
        text='{}\n🏥active : {}\n🦠total : {}\n💀deaths : {}\n✔recoveries : {}'.format(state,data[0],data[1],data[2],data[3]),
        reply_markup=back_home_keyboard()
    )

def bio(update,context):
    name=update.message.text
    print(name)

######################################################
def main_menu_message():
    return('Iam a Bot.Please use me 😉')

def first_menu_text():
    return('select any of the states')

##################################
def main_menu_keyboard():
    keyboard=[
        [InlineKeyboardButton('🎯Word-Game',callback_data='word_game')],
        [InlineKeyboardButton('🌐Website',url='https://covid-india-webapp.herokuapp.com/')],
        [InlineKeyboardButton('🦠Covid-Cases',callback_data='covid')]]
    return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
    names=get_states_data()
    names_list=[]
    for i in names.keys():
        names_list.append([InlineKeyboardButton('{}'.format(i),callback_data='{}'.format(i))])
    names_list.append([InlineKeyboardButton('Main menu', callback_data='main')])
    return InlineKeyboardMarkup(names_list)

def back_home_keyboard():
    keyboard=[
        [InlineKeyboardButton('Main menu', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)

#####################################################
app = Flask(__name__)
def main():
    bot = Bot(API_TOKEN)
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    dp.add_handler(CommandHandler('start', start))
    #addhandlers
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(first_menu, pattern='covid'))
    dp.add_handler(CallbackQueryHandler(word_game,pattern='word_game'))
    dp.add_handler(CallbackQueryHandler(ret_num))
    dp.add_handler(MessageHandler(Filters.text, bio))
    # start webhook
    bot.delete_webhook()
    url = 'https://{}.pythonanywhere.com/{}'.format('heraldjose111',API_TOKEN)
    bot.set_webhook(url=url)

    # process updates
    @app.route('/' + API_TOKEN, methods=['POST'])
    def webhook():
        json_string = request.stream.read().decode('utf-8')
        update = Update.de_json(json.loads(json_string), bot)
        dp.process_update(update)
        return 'ok', 200


# make sure you've inserted your app.py name
if __name__ == "main":
    main()

