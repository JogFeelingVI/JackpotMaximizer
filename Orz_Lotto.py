# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-31 17:33:32
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-13 23:09:00
import httpx, pathlib, ast
import threading, json, re
import time, datetime
from typing import Final, Callable


RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN= "\033[92m"
ENDC = "\033[0m"  # 重置颜色

updatesJson = pathlib.Path('./updates.json')
# 打印彩色字符
r = lambda s: f'{RED}{s}{ENDC}'
y = lambda s: f'{YELLOW}{s}{ENDC}'
b = lambda s: f'{BLUE}{s}{ENDC}'
g = lambda s: f'{GREEN}{s}{ENDC}'

class OrzBot:
    bot_token = '7160088286:AAHJoNVPE4ulqoxvH4w8gMhnxEu3o2NaAGI'
    chatid = '@Orz-Lotto'
    baseUrl = f"https://api.telegram.org/bot{bot_token}"
    delay = 5
    
    def __init__(self, args:dict={}) -> None:
        '''
        {token:'....',chatid:'lotto'}
        '''
        self.client = httpx.Client(verify=False)
        match args:
            case {'token': str() as token, 'chatid': str() as chatid}:
                self.token = token
                self.chatid = chatid
            case _:
                print(f'{g("`args` is not in the correct format and cannot be initialized.")}')
    
    def get_updates(self, offset=None):
        url = self.baseUrl + "/getUpdates"
        params = {"offset": offset} if offset else {}
        response = self.client.get(url, params=params)
        return response.json()
    
    def handle_updates(self, updates):
        for update in updates["result"]:
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text")
                
                if text and text.startswith("/") and len(text) > 3:
                    # 处理命令
                    command = text[1:].split()[0]
                    match command:
                        case 'start':
                            self.send_message(chat_id, 'Welcome to `Orz-Lotto` bot, which is a lottery service robot.')
                        case 'check':
                            self.send_message(chat_id, readCynsInfo())
                        case 'help':
                            self.send_message(chat_id, 'Available commands:/start, /help, /check')
                        case _:
                            pass
                    
                    # ... 添加更多命令处理 ...
                else:
                    # 处理普通消息
                    info = handle_response(text)
                    self.send_message(chat_id, f"you said so: {info}")

            # 更新 offset，避免重复处理已处理的更新
            offset = update["update_id"] + 1
            return offset
        
    def send_message(self, chat_id, text):
        url = self.baseUrl + "/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        self.client.post(url, json=data)
        
    def start(self):
        offset = None
        while True:
            updates = self.get_updates(offset)
            # with updatesJson.open('w') as upJson:
            #     upJson.write(json.dumps(updates, indent=4))
            if updates["result"]:
                offset = self.handle_updates(updates)
            time.sleep(self.delay)
            
def now_dt() -> str:
    now = datetime.datetime.now()
    # 格式化时间为指定的格式
    formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_time

def loger(e, name:str):
    now = now_dt()
    return f'@{name} The error occurred at {now}, specifically: {e}\n'

def handle_response(text:str) -> str:
    match text.lower():
        case str() as t if 'hello' in t:
            return 'Nice to meet you.'
        case str() as t if 'how are you' in t:
            return 'I`am good.'
        case str() as t if 'time' in t:
            return now_dt()
        case str() as t if 'i love you' in t:
            return 'Why do you always wear a tuxedo? The penguin replied: If I took off my tuxedo, I would be a naked bear!'
        case _:
            return text

def readCynsInfo():
    cyns_json = pathlib.Path('./cyns.log')
    search_id_r_b = re.compile(r"id\s+(\d+).*\*(.*)\s\+\s(.*)")
    search_id_cyn_r_b = re.compile(r'id\s+(\d+).*\{(.*)\}\s\*\s(.*)\s\+\s(.*)')
    data = []
    with cyns_json.open('r+') as f:
        for line in f:
            line = line.strip()  # 去除首尾空格
            if line:  # 检查是否为空行
                match_search = search_id_cyn_r_b.search(line)
                if match_search == None:
                    return 'search_id_r_b is None'
                
                _id, cyns, _r, _b = match_search.groups()
                r= ' '.join((f'{x:02}' for x in ast.literal_eval(_r)))
                b = ' '.join((f'{x:02}' for x in ast.literal_eval(_b)))
                cyns = ast.literal_eval( f'{{{cyns}}}').get(4,-1)
                data.append((int(_id),cyns,f'{r} - {b}'))
        # f.truncate(0)  # 将文件指针移动到开头
        # f.flush()
    # 排序
    data.sort(key=lambda item: item[1])
    infos = []
    count = 0
    # 打印信息，每行后添加空行
    for item in data[0:30]:
        id,cyns, info = item
        infos.append(f'{id:_>4}|{cyns}: {info} \n')
        count +=1 
        if count == 5:
            infos.append('\n')
            count = 0
    return_msg =  ''.join(infos)
    if return_msg == '':
        return_msg = 'No Find Data.'
    return return_msg


def worker_thread():
    print('Welcome to `Orz-Lotto` bot')
    orz = OrzBot()
    try:
        orz.start()
    except Exception as e:
        with open('error.log', 'a') as err:
            estr = loger(e, 'worker_thread')
            print(f'{r(estr)}')
            err.write(estr)
        worker_thread()



if __name__ == "__main__":
    worker_thread() 