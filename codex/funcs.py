#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-25 22:07:34

from typing import Any, Iterable, List
import os, re, json, enum, asyncio
from codex.ospath import findAbsp
from datetime import datetime as dtime
from codex.download import get_html
from codex.loadjson import Load_JSON, Resty
from codex import multip_v3, sq3database

maxdep: int = 3000
prompt: str = '[+]'
prompt_L = '[-]'
prompt_W = '[!]'
prompt_D = '[*]'


class Limit_i(enum.Enum):
    '''
    Limit_input 6-19 or 1-16
    '''
    r = (6, 19)
    b = (1, 16)

    def tovs(self) -> List:
        a, b = self.value
        return [x for x in range(a, b + 1)]


class insrt:

    def __init__(self, code: int, reP: re.Pattern) -> None:
        self.code = code
        self.reP = reP


def insregs(ins: str) -> insrt:
    ''' --ins '^(03) (08) (13)(.*)' '''
    try:
        temp: re.Pattern = re.compile(ins)
    except re.error as er:
        date = {'sp': '', 'info': ''}
        date['info'] = f'Regular error {er.pattern}'
        date['sp'] = f'{"-"*len(date["info"])}'
        for key in ['sp', 'info', 'sp']:
            print(f'{prompt_W} {date[key]}')
        return insrt(0, re.compile('(.*)'))
    else:
        return insrt(1, temp)


def get_file_path(name: str) -> str:
    '''
    File real path
    '''
    fp = findAbsp.file_path(name)
    return fp


def getdata() -> None:
    ''' 
        gethtml 
        >03,18,23,24,25,32</span>|<span class="c_bule">09<  
        (?=.*[0-9])(?=.*[,])[0-9,]{17} R
        
    '''
    try:
        data_file_path = get_file_path(Resty.OxData.tostr())
        data_file_path = data_file_path if data_file_path is not None else ''
        html_content = get_html(Load_JSON(Resty.OxStr, 'UTXT').read[1]).neirong
        if html_content != '':
            Rx = re.findall(r'>([0-9,]{17})<', html_content)
            Bx = re.findall(r'c_bule\">([0-9]{2})<', html_content)
            Lix = {
                'R': [int(x) for r in Rx for x in r.split(',')],
                'B': [int(x) for x in Bx],
                'date': dtime.now().__str__()
            }
            json_str = json.dumps(Lix)
            with open(data_file_path, 'w') as datajson:
                datajson.write(json_str)
                hszie = json_str.__sizeof__()
                print(f'{prompt} updata network data sizeof {hszie}')
        else:
            print(f'{prompt} updata network error')
    except Exception as e:
        print(f'{prompt} error: {e}')


def loaddata() -> dict[str, List[int]]:
    '''
    load data
    '''
    file_name = Resty.OxData.tostr()
    try:
        json_str = {}
        if (fps := get_file_path(file_name)) != None:
            with open(fps, 'r') as rbdata:
                json_str = json.load(rbdata)
                print(f'{prompt} loading buffer P{json_str["R"][-6:]}')
        return json_str
    except FileNotFoundError:
        print(f'{prompt} failed to load data from {file_name}, file not found')
        return {}


def jiaoyan(r: List) -> bool:
    ''' is [0,0,0,0] '''
    rex = False
    if type(r) in [list, tuple]:
        a, c, d = r
        if c != d:
            rex = True
    return rex


def showargs(ages: dict) -> None:
    '''
    echo debug msg
    '''
    for k, i in ages.items():
        msgs = f'{prompt_D} {k} = {i}'
        print(msgs)


def Limit_input(r: int, input: Limit_i) -> int:
    '''
    Limit input R 6-19
    '''
    if r in input.tovs():
        r = r
    else:
        r = input.tovs()[0]
        print(f'{prompt} - {input.name} in {input.value}')
    return r


def Prn(N: int = 33, R: int = 6, B: int = 1):
    '''
    P 概率
    R 选择几个数
    N 总共待选数字
    '''
    Ldei = {0: 0, 1: 0, 2: 0}
    Naz = [N, R, N - R]
    if N - R > 0:
        for inx in enumerate(Naz):
            i, n = inx
            Ldei[i] = Pjie(n)
        Ld = Ldei[0] // (Ldei[1] * Ldei[2])
    else:
        Ld = 1
    print(f'{prompt} objectives {N} -> {R} / {Ld} $ {Ld*2*B}')


def Pjie(N: int) -> int:
    '''
    N = 1*2*3*4*5*6*7....
    '''
    Ldei = 0
    for Rx in range(1, N + 1):
        if Ldei <= 0:
            Ldei = Rx
        else:
            Ldei = Ldei * Rx
    return Ldei


class action:
    ''' 执行脚本分析动作 '''
    buffto = []
    diff_date = []
    __echo_index: int = 0

    def __init__(self, args: dict, diff: bool = False):
        '''
        action __init__
        '''
        self.args: dict[str, Any] = args if args != None else {
            'save': False,
            'r': 6,
            'b': 1,
            'jhr': [0, 1, 2, 3, 4, 5],
            'jhb': [0]
        }
        self.cpu = os.cpu_count()
        self.fmr = Limit_input(self.fmr, Limit_i.r)
        self.fmb = Limit_input(self.fmb, Limit_i.b)
        if diff == True:
            self.__Load_diff__()

    @property
    def fmr(self) -> int:
        ''' fmkey  '''
        value = 6
        if 'r' in self.args.keys():
            value: int = int(self.args.get('r', value))
        return value

    @fmr.setter
    def fmr(self, value: int):
        dvalu = {'r': value}
        self.args.update(dvalu)

    @property
    def fmb(self) -> int:
        ''' fmkey  '''
        value = 1
        if 'b' in self.args.keys():
            value: int = int(self.args.get('b', value))
        return value

    @fmb.setter
    def fmb(self, value: int):
        dvalu = {'b': value}
        self.args.update(dvalu)

    @property
    def fmn(self) -> int:
        value = 5
        if 'n' in self.args.keys():
            value: int = int(self.args.get('n', value))
        return value

    @property
    def fmins(self) -> str:
        value = '(.*)'
        if 'ins' in self.args.keys():
            value: str = str(self.args.get('ins', value))
        return value

    @fmins.setter
    def fmins(self, value: str) -> None:
        dvalu = {'ins': value}
        self.args.update(dvalu)

    @property
    def fmcpu(self) -> str:
        value = 'a'
        if 'cpu' in self.args.keys():
            value: str = str(self.args.get('cpu', value))
        return value

    @property
    def fmfix(self) -> str:
        value = 'a'
        if 'fix' in self.args.keys():
            value: str = str(self.args.get('fix', value))
        return value

    @property
    def fmupdate(self) -> bool:
        value = False
        if 'update' in self.args.keys():
            value = bool(self.args.get('update', value))
        return value

    @property
    def fmsave(self) -> bool:
        value = False
        if 'save' in self.args.keys():
            value = bool(self.args.get('save', value))
        return value

    @property
    def fmloadins(self) -> bool:
        value = False
        if 'loadins' in self.args.keys():
            value = bool(self.args.get('loadins', value))
        return value

    @property
    def fmnoinx(self) -> bool:
        value = False
        if 'noinx' in self.args.keys():
            value = bool(self.args.get('noinx', value))
        return value

    @property
    def fmdebug(self) -> bool:
        value = False
        if 'debug' in self.args.keys():
            value = bool(self.args.get('debug', value))
        return value

    @property
    def fmusew(self) -> str:
        value = 'c'
        if 'usew' in self.args.keys():
            value = str(self.args.get('usew', value))
        return value

    @property
    def fmjhr(self) -> list:
        value = [0]
        if 'jhr' in self.args.keys():
            value = list(self.args.get('jhr', value))
        return value

    @property
    def fmjhb(self) -> list:
        value = [0]
        if 'jhb' in self.args.keys():
            value = list(self.args.get('jhb', value))
        return value

    @property
    def fmsubcommand(self) -> str:
        value = 'load'
        if 'subcommand' in self.args.keys():
            value = str(self.args.get('subcommand', value))
        return value

    def __Load_diff__(self) -> None:
        listx = '611602513504414405315216116016000300200100'
        rex = re.compile('[0-6]{3}')
        self.diff_date = rex.findall(listx)

    def __fixrba__(self, rba: str) -> None:
        '''
        fix r b a
        rba is [ r, b, a ]
        '''
        Numa: List[int] = [b for b in range(1, 17)]
        Numb: List[int] = [a for a in range(17, 34)]
        cmds = {
            'r': lambda: [['R', Numa + Numb]],
            'b': lambda: [['B', Numa]],
            'a': lambda: [['R', Numa + Numb], ['B', Numa]]
        }
        Zdict = cmds[rba]()
        for kn, vl in Zdict:
            # kn = R vl = [1,2,3,4,5,6...]
            kn_val = self.data.get(kn, [0])
            fix_kn = set(vl) ^ set(kn_val)
            if len(fix_kn) > 0:
                self.data[f'fix_{kn}'] = list(fix_kn)
                print(f'{prompt} fix {kn} {fix_kn}')

    def __cpuse__(self, argb: str) -> None:
        '''
        str o one
        str a all
        str m Moni test
        '''
        match argb:
            case 'o':
                self.__cpu_one__()
            case 'a':
                self.__cpu_all__()
            case 'm':
                self.__cpu_all_moni__()
    

    def __echo__(self, Rexs: List) -> None:
        '''
        echo numbers
        '''
        if Rexs == 0:
            print(f'{prompt_L}')
            return
        inx, Nr, Nb = Rexs
        
        # 发现错误 终止执行程序
        lis = f'{Nr} + {Nb}'
        if self.fmnoinx:
            print(f'{prompt_L} {lis}')
        else:
            print(f'{prompt_L} {{{inx}}} {lis}')
        self.__echo_index += 1

    def __diff__(self, Rexs: List) -> List[int]:
        '''
        echo numbers
        '''
        id, Nr, Nb = Rexs
        Nr = [int(x) for x in Nr.split(' ')]
        Nb = [int(x) for x in Nb.split(' ')]
        dif_l = []
        jhr = self.fmjhr
        jhb = self.fmjhb
        zipo = multip_v3.ccp(Nr, Nb)
        # 发现错误 终止执行程序
        for zR, zB in zipo:
            dif_r = (set(zR) & set(jhr)).__len__()
            dif_b: int = (set(zB) & set(jhb)).__len__()
            key = f'^{dif_r}{dif_b}[0-6]'
            difex: str = [x for x in self.diff_date if re.match(key, x)][0]
            dif_l.append([int(difex[-1]), zR, zB])
            #print(f'Diff info  -> {Nr} {Nb}')
        return dif_l

    def __cpu_one__(self) -> None:
        '''
        only cpu A run work
        '''
        fmins_is = insregs(self.fmins)
        if fmins_is.code == 1:
            # cp_one = mLpool(self.data, self.fmr, self.fmb, fmins_is.reP, self.fmusew)
            # cp_one.reego = self.fmloadins
            # reds = cp_one.run_works(self.fmn, mcp=False)
            p = multip_v3
            p.settingLength(self.fmn)
            p.useRego(self.fmloadins)
            p.initPostCall(self.data, self.fmr, self.fmb, fmins_is.reP,self.fmusew)
            
            Retds = p.tasks_single()
            reds = self.__planning__(Retds)
            for inx in reds:
                self.__echo__(inx)

    def __cpu_all__(self) -> None:
        '''
        use all cpu cores
        '''
        fmins_is = insregs(self.fmins)
        if fmins_is.code == 1:
            print(f'{prompt} cpus {self.cpu} maxdep {maxdep}')
            p = multip_v3
            p.settingLength(self.fmn)
            p.useRego(self.fmloadins)
            p.initPostCall(self.data, self.fmr, self.fmb, fmins_is.reP,self.fmusew)
            Retds = p.tasks_futures_press()
            Retds = self.__planning__(Retds)
            for item in Retds:
                self.__echo__(item)

    def __planning__(self, rex: Iterable, step: int = 5) -> List:
        ''' 
        xxxxx ^ xxxxx
        '''
        glos = []
        temp = [x for x in rex if jiaoyan(x)]
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

    def __cpu_all_moni__(self) -> None:
        '''
        use all cpu cores
        '''
        fmins_is = insregs(self.fmins)
        if fmins_is.code == 1:
            print(f'{prompt} moni cpus {self.cpu} maxdep {maxdep}')
            # cp_all = mLpool(self.data, self.fmr, self.fmb, fmins_is.reP,
            #                 self.fmusew)
            # cp_all.reego = self.fmloadins
            # Retds = cp_all.run_works(self.fmn)
            p = multip_v3
            p.settingLength(self.fmn)
            p.useRego(self.fmloadins)
            p.initPostCall(self.data, self.fmr, self.fmb, fmins_is.reP,self.fmusew)
            Retds = p.tasks_futures_press()
            Rex: list = [y for x in Retds for y in self.__diff__(x)]
            iRex = len(Rex)
            if iRex == 0:
                return
            sum = 0.0
            f = lambda x, R: [(r, b) for m, r, b in R if m == x].__len__()
            listx = [[x, f(x, Rex)] for x in range(1, 7)]
            cyn = iRex * 2
            for l, v in listx:
                print(
                    f'{prompt_W} {l} Probability of Winning {v/iRex:>7.2%} {v}'
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
            print(f'{prompt_W} sum {sum:>7.2%} Len {iRex} cyn {cyn} $')

    def Moni_Calcu(self):
        '''
        执行模拟计算
        '''
        self.data = loaddata()
        # if self.fmloadins == True:
        #     self.reego = self.loadinsx
        if self.fmfix != None:
            # 执行 fix 程序
            self.__fixrba__(self.fmfix)
        if self.fmdebug == True:
            showargs(self.args)
        if self.fmcpu != None:
            self.__cpuse__(self.fmcpu)

    def act_for_dict(self):
        ''' anys dict '''
        if self.fmsubcommand == 'help':
            print(f'help {self.args}')
        elif self.fmsubcommand == 'update':
            getdata()
        elif self.fmsubcommand == 'load':
            self.data = loaddata()
            if self.fmfix != None:
                # 执行 fix 程序
                self.__fixrba__(self.fmfix)
            # if self.fmloadins == True:
            #     self.reego = self.loadinsx
            Prn(N=self.fmr, B=self.fmb)
            # show debug
            if self.fmdebug == True:
                showargs(self.args)
            # cpu switch
            self.__cpuse__(self.fmcpu)

            print(f'{prompt} Total {self.__echo_index} Notes')

