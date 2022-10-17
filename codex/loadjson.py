#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 12:25:40
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 12:25:40
import json, enum


class Resty(enum.Enum):
    OxStr = './String.json'


class Load_JSON:

    def __init__(self, res: Resty) -> None:
        ''' res: Resty '''
        self.JSON = self.__loadjson__(res.value)

    def __loadjson__(self, path: str) -> dict:
        ''' Load ./String.json '''
        from codex.ospath import os_path
        fp = os_path.file_path('./String.json')
        with open(path, 'r') as f:
            jdata: dict = json.load(f)
        return jdata

    def read(self, key: str) -> list:
        ''' read(key) return list [str, xxxoooxxx ] '''
        return [type(self.JSON[key]), self.JSON[key]]