import json
import telegram
from telegram.ext import CommandHandler, MessageHandler, Application, ContextTypes, filters, CallbackQueryHandler, CallbackContext
from telegram import  Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv()



import requests
Token = os.getenv('TELE_KEY')

qrcode = 'QR Code'
shortlink = 'Short Link'
userlink = ''
ar=[]

application = Application.builder().token(Token).build()



async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Insert a link")



async def help(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='''
    /start -> Welcome to tryTalk url shortener
    /help -> Send me a url an I'll generate a sweet QR code or short link for you
    /contact -> Contact the bot creator
    ''')


#async def shorten(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter your URL")


async def contact(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='''
    email: princeodoi39@gmail.com
    linkedin: https://www.linkedin.com/in/prince-odoi/
    mobile: +233 5457 30281
    ''')

async def trytalk(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    userlink = update.message.text
    ar.append(userlink)
    #print(userlink)
    buttons = [[InlineKeyboardButton(qrcode, callback_data='1')], [InlineKeyboardButton(shortlink, callback_data = '2')]]

    await update.message.reply_text(text= 'What are we generating?', reply_markup=InlineKeyboardMarkup(buttons))

async def buttRepHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(ar[-1])
    readymessage = ''
    query = update.callback_query

    await query.answer()

    if query.data == '1':
        url = ar[-1]
        base_url = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='
        shorten = base_url + url
        payload={}
        headers = {}
        response = requests.request("GET", shorten, headers=headers, data=payload)
        img = response.content
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)
        readymessage ='Your QR code, Download and share'
    if query.data == '2':
        url = ar[-1]
        base_url = 'http://rogueman.pythonanywhere.com/v1/shorten?url='
        shorten = base_url + url
        payload={}
        headers = {}
        response = requests.request("GET", shorten, headers=headers, data=payload)
        p=response.json()
        l=json.loads(p) 
        readymessage = 'Here are some short URLs for your link:\n' + l['result']['short_link'] + '\n' + l['result']['short_link2']+ '\n' + l['result']['short_link3']
        
    
    await query.edit_message_text(text=readymessage)





echo_handler = MessageHandler(filters.TEXT, trytalk)
#echolink_handler = MessageHandler(filters.TEXT,buttRepHandler)

application.add_handler(CommandHandler('contact', contact))
application.add_handler(CommandHandler('help', help))
#application.add_handler(CommandHandler('shorten', shorten))
application.add_handler(CommandHandler('start',start))
application.add_handler(echo_handler)
#application.add_handler(echolink_handler)
application.add_handler(CallbackQueryHandler(buttRepHandler))

application.run_polling()

