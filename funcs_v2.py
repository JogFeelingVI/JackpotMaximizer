# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-26 14:13:37
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-29 16:15:29
import pathlib, json, re
from codex import gethtml_v2

class action:
    def __init__(self, args:dict) -> None:
        match args:
            case {'subcommand': str() as act} if act == 'update':
                update()
            case {'subcommand': str() as act} if act == 'load':
                load(args=args)
            case _:
                pass
            
class update:
    json_path = pathlib.Path('./DataFrame.json')
    def __init__(self) -> None:
        url = 'https://www.cjcp.cn/zoushitu/cjwssq/hqaczhi.html'
        data_fr = gethtml_v2.toDict(gethtml_v2.get_html(url).neirong)
        Last = f'{self.__f(data_fr["R"][-6::])} + {self.__f([data_fr["B"][-1]])}'
        json_str = json.dumps(data_fr)
        with open(self.json_path, 'w') as datajson:
            datajson.write(json_str)
            hszie = json_str.__sizeof__()
            print(f'The data has been updated, sized {hszie}kb, {Last = }')
            
    def __f(self, x:list) -> str:
        return' '.join([f'{n:02}' for n in x])

class load:
    def __init__(self, args:dict) -> None:
        '''
        {'dnsr': True, 'noinx': False, 'fix': 'a', 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
        '''
        if 'subcommand' in args.keys() and args['subcommand'] == 'load':
            self.__Execute_args(args)
            
            
    def __loaddata(self) -> dict:
        '''
        load data
        '''
        json_path = pathlib.Path('./DataFrame.json')
        json_str = {}
        try:
            with open(json_path, 'r') as jsonread:
                json_str = json.load(jsonread)
                print(f'loading buffer P{json_str["R"][-6:]}')
                
        except:
            print(f'failed to load data from {json_path}, file not found')
        finally:
            return json_str
        
    def __fixrba(self, rba: str, data:dict) -> None:
        '''
        fix r b a
        rba is [ r, b, a ]
        '''
        fix = {}
        match rba:
            case 'r':
                na = [x for x in range(1, 34)]
            case 'b':
                na = [x for x in range(1, 17)]
            case 'a':
                self.__fixrba('r', data)
                self.__fixrba('b', data)
                return
            case _:
                return
        _data =  set(data[rba.upper()]) ^ set(na)
        fix.update({rba: (x for x in _data) if _data.__len__() != 0 else 0})
        for key, val in fix.items():
            if isinstance(val, int) == False:
                print(f'Fix {" ".join(map(str , val))} of column "{key}"')
            
    def __Execute_args(self, args:dict):
        print(f'Execute args...')
        _data = self.__loaddata()
        match args:
            case {'fix': str() as fix, 'cpu': str() as cpu, 'usew': str() as usew}:
                self.__fixrba(fix, _data)
            case _:
                df = {'dnsr': True, 'noinx': False, 'fix': 'a', 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
                print(f'Command parameter error')
                for k, v in args.items():
                    if type(v) != type(df[k]):
                        print(f'The name "{k}" should have a value of "{df[k]}", but you provided "{v}".')
        
    

def main():
    args_a ={'r': 6, 'b': 1}
    args_b = {'subcommand': 'update', 'r': 6, 'b': 1}
    args_c = {'dnsr': True, 'noinx': False, 'fix': 'a', 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
    args_d = {'dnsr': True, 'noinx': False, 'fix': 1, 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
    print("Hello, World!")
    act = action((args_d))


if __name__ == "__main__":
    main()
