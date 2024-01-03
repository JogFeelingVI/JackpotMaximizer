#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 12:25:40
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-03 15:48:11
import json, enum
from codex.ospath import findAbsp


class Resty(enum.Enum):
    OxStr = './String.json'
    Oxinsreg = './insx.reg'
    OxSave = './save.log'
    OxData = './DataFrame.json'

    def tostr(self) -> str:
        return self.value


class Load_JSON:

    def __init__(self, res: Resty, keys: str) -> None:
        ''' res: Resty '''
        self.json_data = self.__loadjson__(res.tostr())
        self.keys = keys

    def __loadjson__(self, path: str) -> dict:
        ''' Load ./String.json '''
        jdata: dict = {}
        try:
            fp: str = findAbsp.file_path(path)
            with open(fp, 'r') as f:
                jdata: dict = json.loads(f.read())
        except:
            jdata = {'Error': 1}

        return jdata

    @property
    def read(self) -> tuple:
        ''' read(key) return list [str, xxxoooxxx ] '''
        date = self.json_data.get(self.keys)
        rex = (type(date), date)
        return rex