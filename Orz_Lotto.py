# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-31 17:33:32
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-22 15:39:43
# @overwatch https://core.telegram.org/bots/api#sendphoto

import httpx, pathlib, ast, re
import time, datetime, Orz_Loadtojpg
from typing import Final, Callable, List
from PIL import Image, ImageDraw, ImageFont


RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDC = "\033[0m"  # 重置颜色

updatesJson = pathlib.Path("./updates.json")
# 打印彩色字符
r = lambda s: f"{RED}{s}{ENDC}"
y = lambda s: f"{YELLOW}{s}{ENDC}"
b = lambda s: f"{BLUE}{s}{ENDC}"
g = lambda s: f"{GREEN}{s}{ENDC}"


class OrzBot:
    bot_token = "7160088286:AAHJoNVPE4ulqoxvH4w8gMhnxEu3o2NaAGI"
    chatid = "@Orz-Lotto"
    baseUrl = f"https://api.telegram.org/bot{bot_token}"
    delay = 5

    def __init__(self, args: dict = {}) -> None:
        """
        {token:'....',chatid:'lotto'}
        """
        self.client = httpx.Client(verify=False)
        match args:
            case {"token": str() as token, "chatid": str() as chatid}:
                self.token = token
                self.chatid = chatid
            case _:
                print(
                    f'{g("`args` is not in the correct format and cannot be initialized.")}'
                )

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
                        case "start":
                            self.send_message(
                                chat_id,
                                f"Welcome to `Orz-Lotto` bot, which is a lottery service robot. chatid: {chat_id}",
                            )
                        case "check":
                            print(f'check chatid: {chat_id}')
                            pngs = readCynsInfo()
                            self.send_photo(chat_id, pngs, now_dt())
                        case "help":
                            self.send_message(
                                chat_id, "Available commands:/start, /help, /check"
                            )
                        case _:
                            pass

                    # ... 添加更多命令处理 ...
                else:
                    # 处理普通消息
                    info = handle_response(text)
                    if info != None:
                        self.send_message(chat_id, f"you said so: {info}")

            # 更新 offset，避免重复处理已处理的更新
            offset = update["update_id"] + 1
            return offset

    def send_message(self, chat_id, text):
        url = self.baseUrl + "/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = self.client.post(url, json=data)
        if response.status_code == 200:
            print("The Message was sent successfully.")
        else:
            print(f"Message sending failed, error code:{response.status_code}")
            print(response.text)

    def send_photo(self, chat_id, pngs, caption: str):
        url = self.baseUrl + "/sendPhoto"
        # files = []
        # match pngs:
        #     case str() as sp:
        #         p = pathlib.Path(sp)
        #         if p.exists():
        #             files.append(p.absolute())
        #     case list() as lp:
        #         for sp in lp:
        #             p = pathlib.Path(sp)
        #             if p.exists():
        #                 files.append(p.absolute())
        # 确保文件全部存在 并将所有文件转换 pathlib
        for f in pngs:
            filePath = pathlib.Path(f'./{f}')
            if filePath.exists():
                photo = {'photo': open(filePath, mode='rb')}
                data = {"chat_id": chat_id, "caption": caption}
                response = self.client.post(url, files=photo, data=data)
                # print(f'{response.text}')
                if response.status_code == 200:
                    print("The picture was sent successfully.")
                    filePath.unlink()
                else:
                    print(f"Image sending failed, error code:{response.status_code}")
                    print(response.text)
                

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


def loger(e, name: str):
    now = now_dt()
    return f"@{name} The error occurred at {now}, specifically: {e}\n"


def handle_response(text: str) -> str:
    # print(f'test {text}')
    match text:
        case str() as t if "hello" in t.lower():
            return "Nice to meet you."
        case str() as t if "how are you" in t.lower():
            return "I`am good."
        case str() as t if "time" in t.lower():
            return now_dt()
        case str() as t if "i love you" in t:
            return "Why do you always wear a tuxedo? The penguin replied: If I took off my tuxedo, I would be a naked bear!"
        case _:
            return text


def readCynsInfo():
    data = Orz_Loadtojpg.loadtoData()
    return Orz_Loadtojpg.datatoPngv3(data)


def worker_thread():
    print("Welcome to `Orz-Lotto` bot")
    orz = OrzBot()
    try:
        orz.start()
    except Exception as e:
        with open("error.log", "a") as err:
            estr = loger(e, "worker_thread")
            print(f"{r(estr)}")
            err.write(estr)
        worker_thread()


if __name__ == "__main__":
    worker_thread()
