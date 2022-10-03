#!/usr/bin/env python3
# @Author: JogFeelingVi
# @Date: 2022-10-03 12:25:40
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 12:25:40
import json,enum

class Resty(enum.Enum):
    String = './String.json'
    

class Load_JSON:

    def __init__(self) -> None:
        self.JSON = self.__load()

    def __load(self) -> dict:
        ''' Load ./String.json '''
        with open('./String.json', 'r') as f:
            jdata: dict = json.load(f)
        return jdata

    def read(self, key: str) -> list:
        ''' read(key) return list [str, xxxoooxxx ] '''
        return [type(self.JSON[key]), self.JSON[key]]