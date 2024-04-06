# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-31 17:33:32
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-06 17:42:26
import asyncio, telegram, pathlib, ast
import threading
import time
from typing import Final
from telegram import Update, Bot, ForceReply
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, Updater


RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN= "\033[92m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
r = lambda s: f'{RED}{s}{ENDC}'
y = lambda s: f'{YELLOW}{s}{ENDC}'
b = lambda s: f'{BLUE}{s}{ENDC}'
g = lambda s: f'{GREEN}{s}{ENDC}'

class OrzBot:
    token = '7160088286:AAHJoNVPE4ulqoxvH4w8gMhnxEu3o2NaAGI'
    chatid = '@Orz-Lotto'
    state = False
    
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
    def start(self):
        try:
            # Application.builder().token("Token").read_timeout(7).get_updates_read_timeout(42).build()
            self.app = ApplicationBuilder().token(self.token).read_timeout(7).get_updates_read_timeout(42).build()
            self.app.add_handler(CommandHandler('start', start_command))
            self.app.add_handler(CommandHandler('check', check_command))
            self.app.add_error_handler(error)
            self.app.run_polling(poll_interval=5)
        except Exception as e:
            self.state = False
            with open('error.log', 'a') as file:
            # 将信息写入文件
                file.write(f'{e} from OrzBot.\n')
    
    
        
async def error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    err_info = f'Update {update} Error'
    await context.bot.sendMessage(chat_id=context.bot.id, text=err_info)
    
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if update.message != None:
        await update.message.reply_text('Welcome to `Orz-Lotto` bot, which is a lottery service robot.')

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cyns_json = pathlib.Path('./cyns.log')

    data = []
    with cyns_json.open('r') as f:
        for line in f:
            line = line.strip()  # 去除首尾空格
            if line:  # 检查是否为空行
                parts = line.split("/ cyn")
                # print(f'{parts = }')
                # # parts = ['@Last Modified time: 2024-04-04 09:36:32 -> id  930 ', ' 26 * [4, 9, 13, 18, 24, 32] + [13]']
                # return
                if len(parts) == 2:
                    # 提取 id 和信息
                    cyns, info = parts[1].split("*")
                    # print(f'{id_str = } {info = }')
                    # return
                    try:
                        cyns = int(cyns.strip())
                        r, b = info.split('+')
                        r= ' '.join((f'{x:02}' for x in ast.literal_eval(r)))
                        b = ' '.join((f'{x:02}' for x in ast.literal_eval(b)))
                        data.append((cyns, f'■ {r} ▣ {b}'))
                        # print(f'{id_num = } {info = }')
                        # return 
                    except ValueError:
                        print(f"Invalid row: {line}")
    # 排序
    data.sort(key=lambda item: item[0])
    infos = []
    count = 0
    # 打印信息，每行后添加空行
    for item in data[0:20]:
        id, info = item
        infos.append(f'{id} {info} \n')
        count +=1 
        if count == 5:
            info += '\n'
            count = 0
    
    if update.message != None:
        await update.message.reply_text(''.join(infos))
                            

def worker_thread():
    orz = OrzBot()
    try:
        orz.start()
    except Exception as e:
        with open('error.log', 'a') as err:
            err.write(f'worker_thread:{e}\n')
        
            
def start_thread():
    thread = threading.Thread(target=worker_thread, name='Orz_Lotto')
    thread.daemon = True  # 设置为守护线程
    thread.start()
    thread.join()


def main():
    print('Welcome to `Orz-Lotto` bot')
    worker_thread()
    


if __name__ == "__main__":
    main() 