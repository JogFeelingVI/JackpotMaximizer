#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39

from typing import Union, Any, List
import multiprocessing as mlps, os, sys, re, json, random as RDX, enum
from codex.ospath import os_path
from datetime import datetime as dtime
from codex.download import get_html
from codex.loadjson import Load_JSON, Resty

maxdep: int = 3000
prompt: str = '[+]'


class mode_f(enum.Enum):
    '''
    find mode ok, no, er
    '''
    Ok = 1
    No = 2
    Er = -1


class Limit_i(enum.Enum):
    '''
    Limit_input 6-19 or 1-16
    '''
    r = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
    b = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)


def get_file_path(name: str) -> str:
    '''
    File real path
    '''
    fp = os_path.file_path(name)
    return fp


def getdata() -> None:
    ''' 
        gethtml 
        >03,18,23,24,25,32</span>|<span class="c_bule">09<  
        (?=.*[0-9])(?=.*[,])[0-9,]{17} R
        
    '''
    try:
        data_file_path = get_file_path('./rbdata.json')
        data_file_path = data_file_path if data_file_path is not None else ''
        html_content = get_html(Load_JSON(Resty.OxStr, 'UTXT').read[1]).neirong
        if html_content != '':
            Rx = re.findall(r'(?=.*[0-9])(?=.*[,])[0-9,]{17}', html_content)
            Bx = re.findall(r'c_bule\">([0-9]{2})<', html_content)
            Lix = {
                'R': [int(x) for r in Rx for x in r.split(',')],
                'B': [int(x) for x in Bx],
                'date': dtime.now().__str__()
            }
            json_str = json.dumps(Lix, indent=4)
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
    file_name = './rbdata.json'
    try:
        json_str = {}
        if (fps := get_file_path(file_name)) != None:
            with open(fps, 'r') as rbdata:
                json_str = json.load(rbdata)
                print(f'{prompt} loading buffer')
        return json_str
    except FileNotFoundError:
        print(f'{prompt} failed to load data from {file_name}, file not found')
        return {}


def jiaoyan(r: List) -> bool:
    rex = False
    a, b, c, d = r
    if type(a) == type(b) == int and c != [0] and d != [0]:
        rex = True
    return rex


def Findins(NR: list, NB: list, insre: str) -> mode_f:
    '''
    Find Ins 
    Nums type list
    inse type str
    '''
    if insre == '' or insre == '(.*)':
        # 不做任何限制
        return mode_f.Ok
    else:
        try:
            sNr = ' '.join([f'{x:02}' for x in NR])
            sNb = ' '.join([f'{x:02}' for x in NB])
            sNums = f'{sNr} + {sNb}'
            Finx = len(re.findall(insre, sNums))
            return mode_f.Ok if Finx >= 1 else mode_f.No
        except re.error as rerror:
            print(f'{prompt} Findins error: {rerror.msg}')
            return mode_f.Er


def debugx(msg: Any) -> None:
    '''
    echo debug msg
    '''
    msgs = f'debug {msg}'
    print(msgs)


def truncate(Dr: List, keys: List) -> List:
    #debugx(int(num*(10**n)))
    tmps = [Dr.count(x) for x in keys]
    #mx = max(tmps)
    #tmps = [[mx - x, 1][x == mx] for x in tmps]
    return tmps


def frommkeyx(Dx: List) -> List:
    tmps = [x for x in {}.fromkeys(Dx).keys()]
    RDX.shuffle(tmps)
    return tmps


def makenuxe(arglist: List) -> List:
    '''
    makenux for all cpu
    '''
    inx, D, R, B, i = arglist
    a, b, c = makenux(Data=D, Rlen=R, Blen=B, ins=i)
    return [inx, a, b, c]


def makenux(Data: dict, Rlen: int, Blen: int, ins: str) -> List:
    '''
        data {'r': [1,2,3...], 'b':[1-16]}
        Rlen R len 1, 2, 3, 4, 5, 6 + Blen
        Blen B len 1 - 16
        ins '^(01|07)....'
    '''
    Dr = Data['R']
    Db = Data['B']
    R_keys = frommkeyx(Dr)
    B_keys = frommkeyx(Db)
    # EDIT
    weights_R = truncate(Dr, R_keys)
    # avg R
    weights_B = truncate(Db, B_keys)
    # avg B
    depth: int = 1
    while True:
        dr, Rs = choicesrb_dd(R_keys, weights_R, Rlen)
        db, Bs = choicesrb_dd(B_keys, weights_B, Blen)
        rinsx: mode_f = Findins(Rs, Bs, insre=ins)
        if rinsx == mode_f.Ok:
            return [dr, Rs, Bs]
        depth += 1
        if depth >= maxdep:
            return [dr, [0], [0]]


def choicesrb_dd(keys: List, weights: List, lens: int) -> List:
    '''
    _dd
    keys list 待选列表
    weights list 权重
    len int 选择长度
    depth int 计算深度
    rdx = RDX.choices
    '''
    depth: int = 1
    while True:
        Jieguo = RDX.choices(keys, weights=weights, k=lens)
        Jieguo = [x for x in sorted(Jieguo)]
        if len(Jieguo) == list(set(Jieguo)).__len__():
            return [depth, Jieguo]
        depth += 1
        if depth >= maxdep:
            return [depth, [0]]


def Limit_input(r: int, input: Limit_i) -> int:
    '''
    Limit input R 6-19
    '''
    if r in input.value:
        r = r
    else:
        r = 6
        print(f'{prompt} -{input.name} in {input.value}')
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
    __echo_index: int = 1

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
        self.fmr = Limit_input(self.fmr, Limit_i.r)
        self.fmb = Limit_input(self.fmb, Limit_i.b)
        self.buffto.append(f'date {dtime.now()}')
        self.buffto.append(f'args {self.args}')
        if diff == True:
            self.__Load_diff__()
        if self.fmloadins == True:
            self.fmins = self.loadinsx
        debugx(self.args)

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
    def fmins(self, value: str):
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
    def loadinsx(self) -> str:
        _huan = re.compile('\\n')
        _zhus = re.compile('^#.*')
        _regs = re.compile('^[^#].*')
        _insx = get_file_path('./insx.reg')
        regadd = ['']
        with open(file=_insx, mode='r', encoding='utf-8') as regs:
            reglins = regs.readlines()
            for linx in reglins:
                if _zhus.match(linx) == None and _regs.match(linx) != None:
                    regadd.append(_huan.sub('', linx))
        return ''.join(regadd)

    def __Load_diff__(self) -> None:
        listx = '611602513504414405315216116016000300200100'
        rex = re.compile('[0-6]{3}')
        self.diff_date = rex.findall(listx)

    def __fixrba__(self, rba: str) -> None:
        '''
        fix r b a
        rba is [ r, b, a ]
        '''
        Numa = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        Numb = [
            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33
        ]
        cmds = {
            'r': lambda: [['R', Numa + Numb]],
            'b': lambda: [['B', Numa]],
            'a': lambda: [['R', Numa + Numb], ['B', Numa]]
        }
        Zdict = cmds[rba]()
        for kn, vl in Zdict:
            # kn = R vl = [1,2,3,4,5,6...]
            kn_val = self.data.get(kn)
            fix_kn = [x for x in vl if x not in kn_val]
            if len(fix_kn) > 0:
                self.data[kn] += fix_kn
                print(f'{prompt} fix {kn} {fix_kn}')

    def __cpuse__(self, argb: str) -> None:
        '''
        str o one
        str a all
        str m Moni TEST
        '''
        cmds = {
            'o': lambda: self.__cpu_one__(),
            'a': lambda: self.__cpu_all__(),
            'm': lambda: self.__cpu_all_moni__(),
        }
        cmds[argb]()

    def __echo__(self, Rexs: List) -> None:
        '''
        echo numbers
        '''
        inx, dep, Nr, Nb = Rexs
        # 发现错误 终止执行程序
        if len(Nr) == self.fmr and len(Nb) == self.fmb:
            lis = f'{" ".join([f"{x:02}" for x in Nr])} + {" ".join([f"{x:02}" for x in Nb])} '
            if self.fmnoinx:
                self.buffto.append(f'{prompt} {lis}')
            else:
                self.buffto.append(f'{prompt} {inx:>4} depth {dep:<5} {lis}')
            print(self.buffto[-1])
        else:
            print('')

    def __diff__(self, Rexs: List) -> int:
        '''
        echo numbers
        '''
        inx, dep, Nr, Nb = Rexs
        jhr = self.fmjhr
        jhb = self.fmjhb
        dif_l = 0

        # 发现错误 终止执行程序
        if len(Nr) == self.fmr and len(Nb) == self.fmb:
            dif_r = [x for x in Nr if x in jhr].__len__()
            dif_b: int = [x for x in Nb if x in jhb].__len__()
            key = f'^{dif_r}{dif_b}[0-6]'
            difex: str = [x for x in self.diff_date if re.match(key, x)][0]
            dif_l = int(difex[-1])
            #print(f'Diff info  -> {Nr} {Nb}')
        return dif_l

    def __cpu_one__(self) -> None:
        '''
        only cpu A run work
        '''
        N = [x for x in range(1, self.fmn + 1)]
        for nx in N:
            dep, Nr, Nb = makenux(self.data, self.fmr, self.fmb, self.fmins)
            self.__echo__([nx, dep, Nr, Nb])

    def __cpu_all__(self) -> None:
        '''
        use all cpu cores
        '''
        cpus = os.cpu_count()
        print(f'{prompt} cpus {cpus} maxdep {maxdep}')
        N = [[x, self.data, self.fmr, self.fmb, self.fmins]
             for x in range(1, self.fmn + 1)]
        with mlps.Pool(processes=cpus) as p:
            Retds = p.map(makenuxe, N)
            Retds = self.__planning__(Retds)
            for item in Retds:
                self.__echo__(item)

    def __planning__(self, rex: List) -> List:
        ''' 
        xxxxx ^ xxxxx
        '''
        glos = []
        step = 5
        temp = [x for x in rex if jiaoyan(x)]
        len_t = temp.__len__()
        for i in range(0, len_t, step):
            ts = temp[i:i + step]
            if len(ts) == step and i + step < len_t:
                glos.extend(ts)
                glos.extend([[0, 0, [0], [0]]])
            else:
                glos.extend(ts)
        return glos

    def __cpu_all_moni__(self) -> None:
        '''
        use all cpu cores
        '''
        cpus = os.cpu_count()
        print(f'{prompt} cpus {cpus} maxdep {maxdep}')
        N = [[x, self.data, self.fmr, self.fmb, self.fmins]
             for x in range(1, self.fmn + 1)]
        with mlps.Pool(processes=cpus) as p:
            Retds = p.map(makenuxe, N)
            Rex = [self.__diff__(x) for x in Retds]
            len_rets = Retds.__len__()
            sum = 0.0
            listx = [[x, Rex.count(x)] for x in range(1, 7)]
            for l, v in listx:
                print(
                    f'{prompt} {l} Probability of Winning {v/len_rets:>7.2%} {v}'
                )
                sum += v / len_rets
            print(f'{prompt} sum {sum:>7.2%}')
            #6 Probability of Winning

    def Moni_Calcu(self):
        '''
        '''
        self.data = loaddata()
        self.__fixrba__('a')
        self.__cpuse__('m')

    def act_for_dict(self) -> None:
        ''' anys dict '''
        if self.fmupdate:
            # update
            getdata()
            return
        self.data = loaddata()
        if self.fmfix != None:
            # 执行 fix 程序
            self.__fixrba__(self.fmfix)
        Prn(N=self.fmr, B=self.fmb)
        # cpu switch
        if self.fmcpu != None:
            self.__cpuse__(self.fmcpu)

        print(f'{prompt} Total {self.__echo_index-1} Notes')

        if self.fmsave:
            if (fps := get_file_path('./save.log')) != None:
                with open(fps, 'w') as sto:
                    for slog in self.buffto:
                        sto.writelines(f'{slog}\n')
