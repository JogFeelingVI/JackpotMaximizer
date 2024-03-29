# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-26 14:13:37
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-29 23:40:26
import pathlib, json, re
from codex import gethtml_v2, multip_v3

class action:
    def __init__(self, args:dict) -> None:
        match args:
            case {'subcommand': str() as act} if act == 'update':
                update()
            case {'subcommand': str() as act} if act in ['simulation', 'load']:
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
        if 'subcommand' in args.keys() and args['subcommand'] in ['simulation', 'load']:
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
            
    @staticmethod    
    def __show_args(args:dict, debug:bool):
        if debug:
            for k, v in args.items():
                print(f'{k:>6}: {f"{v}"}')
                
                
    def __cpu_one(self, args:dict, data:dict, core:bool=False) -> list:
        '''
        only cpu A run work
        '''
        Retds = []
        match args:
            case {'n':int() as n, 'loadins': bool() as loadins, 'r': int() as r, 'b': int() as b, 'ins': str() as ins,'usew': str() as usew}:
                p = multip_v3
                p.settingLength(n)
                p.useRego(loadins)
                p.initPostCall(data, r, b,ins,usew)
                if core == False:
                    Retds = p.tasks_single()
                Retds = p.tasks_futures_press()
            case _:
                pass
        return Retds
                
        #     Retds = p.tasks_single()
        #     reds = self.__planning__(Retds)
        #     for inx in reds:
        #         self.__echo__(inx)
    
    def __cpu_simulation(self, args:dict, data:dict):
        match args:
            case {'Compared-R': list() as cR, 'Compared-B': list() as cB}:
                Retds = self.__cpu_one(args, data, True)
                Rex: list = [y for x in Retds for y in self.__diff__(x, cR, cB)]
                iRex = len(Rex)
                if iRex == 0:
                    return
                sum = 0.0
                f = lambda x, R: [(r, b) for m, r, b in R if m == x].__len__()
                listx = [[x, f(x, Rex)] for x in range(1, 7)]
                cyn = iRex * 2
                for l, v in listx:
                    print(
                        f'{l} Probability of Winning {v/iRex:>7.2%} {v}'
                    )
                    match l:
                        case 1:
                            cyn = cyn - 5000000 * v
                        case 2:
                            cyn = cyn - 100000 * v
                        case 3:
                            cyn = cyn - 3000 * v
                        case 4:
                            cyn = cyn - 200 * v
                        case 5:
                            cyn = cyn - 10 * v
                        case 6:
                            cyn = cyn - 5 * v
                    sum += v / iRex
                print(f'sum {sum:>7.2%} Len {iRex} cyn {cyn} $')
            case _:
                print(f'The simulation program found no data to compare with.')
        
    def __diff__(self, Rexs: list, cR:list, cB:list) -> list:
        '''
        echo numbers
        '''
        diff_date = ['611', '602', '513', '504', '414', '405', '315', '216', '116', '016', '000', '300', '200', '100']
        id, Nr, Nb = Rexs
        Nr = [int(x) for x in Nr.split(' ')]
        Nb = [int(x) for x in Nb.split(' ')]
        dif_l = []
        zipo = multip_v3.ccp(Nr, Nb)
        # 发现错误 终止执行程序
        for zR, zB in zipo:
            dif_r = (set(zR) & set(cR)).__len__()
            dif_b: int = (set(zB) & set(cB)).__len__()
            key = f'^{dif_r}{dif_b}[0-6]'
            difex: str = [x for x in diff_date if re.match(key, x)][0]
            dif_l.append([int(difex[-1]), zR, zB])
            #print(f'Diff info  -> {Nr} {Nb}')
        return dif_l
        
    def __planning__(self, rex: list, step: int = 5) -> list:
        ''' 
        xxxxx ^ xxxxx
        '''
        glos = []
        temp = [x for x in rex if x[1] != x[2]]
        lent = temp.__len__()
        for i in range(0, lent, step):
            es = i + step
            ts = temp[i:es]
            if len(ts) == step and es < lent:
                glos.extend(ts)
                glos.extend([0])
            else:
                glos.extend(ts)
        return glos
    
    def __echo__(self, Rexs: list, noinx:bool = True) -> None:
        '''
        echo numbers
        '''
        if Rexs == 0:
            print(f'')
            return
        inx, Nr, Nb = Rexs
        
        # 发现错误 终止执行程序
        lis = f'{Nr} + {Nb}'
        if noinx:
            print(f'{lis}')
        else:
            print(f'{{{inx}}} {lis}')
            
    def __Execute_args(self, args:dict):
        print(f'Execute args...')
        _data = self.__loaddata()
        match args:
            case {'fix': str() as fix, 'cpu': str() as cpu, 'usew': str() as usew, 'debug': bool() as debug, 'dnsr':bool() as dnsr, 'noinx': bool() as noinx}:
                self.__fixrba(fix, _data)
                self.__show_args(args, debug)
                Return_data = []
                match cpu:
                    case '0':
                        Return_data = self.__cpu_one(args, _data)
                    case 'a':
                        Return_data = self.__cpu_one(args, _data, True)
                        # Enable multi-core
                    case 'm':
                        self.__cpu_simulation(args, _data)
                    case _:
                        print(f'No way to parse unknown parameter "{cpu}"')
                if Return_data == []:
                    print('Return data is empty.')
                elif dnsr:
                    planning = self.__planning__(Return_data)
                    for plan in planning:
                        self.__echo__(plan, noinx)
                else:
                    print(f'Found the "dnsr" tag. Skip display.')
            case _:
                df = {'Compared-R':[],'Compared-B':[],'dnsr': True, 'noinx': False, 'fix': 'a', 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
                print(f'Command parameter error')
                for k, v in args.items():
                    if type(v) != type(df[k]):
                        print(f'The name "{k}" should have a value of "{df[k]}", but you provided "{v}".')
        
    
# 测试用
# def main():
#     args_a ={'r': 6, 'b': 1}
#     args_b = {'subcommand': 'update', 'r': 6, 'b': 1}
#     args_c = {'dnsr': False, 'noinx': False, 'fix': 'a', 'cpu': 'a', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
#     args_d = {'dnsr': True, 'noinx': False, 'fix': 'a', 'cpu': 'm', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1, 'subcommand': 'load'}
#     print("Hello, World!")
#     act = action(args_d)


# if __name__ == "__main__":
#     main()
