# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-31 17:33:32
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-01 16:48:12
import asyncio, telegram, pathlib
from typing import Final
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, Updater


class OrzBot:
    token = '7160088286:AAHJoNVPE4ulqoxvH4w8gMhnxEu3o2NaAGI'
    chatid = '@Orz-Lotto'
    
    def __init__(self, args:dict={}) -> None:
        '''
        {token:'....',chatid:'lotto'}
        '''
        match args:
            case {'token': str() as token, 'chatid': str() as chatid}:
                self.token = token
                self.chatid = chatid
            case _:
                print('`args` is not in the correct format and cannot be initialized.')
        # We create an Updater instance with our Telegram token.
        self.app = ApplicationBuilder().token(self.token).build()
        self.app.add_handler(CommandHandler('list', list))
        self.app.run_polling()
        
    
async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cyns_json = pathlib.Path('./cyns.log')
    info = ''
    if cyns_json.exists() == False:
        info = f'{cyns_json} is not exists'
    else:
        with cyns_json.open('r') as cjson:
            info = cjson.read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=info)
                            


def main():
    print('Welcome to `Orz-Lotto` bot')
    orz = OrzBot()


if __name__ == "__main__":
    main() 