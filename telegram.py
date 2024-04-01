# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-31 17:33:32
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-31 22:21:18
import asyncio, telegram
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


class awbot:
    token = '7160088286:AAHJoNVPE4ulqoxvH4w8gMhnxEu3o2NaAGI'
    chatid = '@Orz-Lotto'
    
    def __init__(self, args:dict={}) -> None:
        '''
        {token:'....',chatid:'lotto'}
        '''
        print(f'{telegram = }')
        match args:
            case {'token': str() as token, 'chatid': str() as chatid}:
                self.token = token
                self.chatid = chatid
            case _:
                print('`args` is not in the correct format and cannot be initialized.')
        
        self.application = ApplicationBuilder().token(self.token).build()
        start_handler = CommandHandler('start', start)
        self.application.add_handler(start_handler)
        self.application.run_polling()
        
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
                            


def main():
    print("Hello, World!")
    atb = awbot()


if __name__ == "__main__":
    main() 