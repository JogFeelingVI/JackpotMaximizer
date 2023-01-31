#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39

from typing import Union, Any, List
import multiprocessing as mlps, os, sys, re, json, random as RDX
from codex.ospath import os_path
from datetime import datetime as dtime
from codex.download import get_html
from codex.loadjson import Load_JSON, Resty

maxdep = sys.getrecursionlimit() - 30
prompt = '[+]'


def file_to(name: str) -> Union[str, None]:
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
    fp = file_to('./rbdata.json')
    fp = fp if fp is not None else ''
    html = get_html(Load_JSON(Resty.OxStr, 'UTXT').read[1]).neirong
    if html != '':
        Rx = re.findall(rb'(?=.*[0-9])(?=.*[,])[0-9,]{17}', html)
        Bx = re.findall(rb'c_bule\">([0-9]{2})<', html)
        Lix = {'R': [], 'B': [], 'date': dtime.now().__str__()}
        for zitem in zip(Rx, Bx):
            R, B = zitem
            R = [int(x) for x in R.decode('utf-8').split(',')]
            B = int(B.decode('utf-8'))
            for Rz in R:
                Lix['R'].append(Rz)
            Lix['B'].append(B)
        json_str = json.dumps(Lix, indent=4)
        with open(fp, 'w') as datajson:
            datajson.write(json_str)
            hszie = json_str.__sizeof__()
            print(f'{prompt} updata network data sizeof {hszie}')
    else:
        print(f'{prompt} updata network error')


def loaddata() -> dict[str, List]:
    '''
    load data
    '''
    json_str = {}
    if (fps := file_to('./rbdata.json')) != None:
        with open(fps, 'r') as rbdata:
            json_str = json.load(rbdata)
            print(f'{prompt} loading buffer')
    return json_str


def Findins(NR: list, NB: list, insre: str) -> bool:
    '''
    Find Ins 
    Nums type list
    inse type str
    '''
    if insre == None:
        # 不做任何限制
        return True
    else:
        try:
            sNr = ' '.join([f'{x:02}' for x in NR])
            sNb = ' '.join([f'{x:02}' for x in NB])
            sNums = f'{sNr} + {sNb}'
            Finx = len(re.findall(insre, sNums))
            return True if Finx >= 1 else False
        except re.error as rerror:
            print(f'{prompt} Findins error: {rerror.msg}')
            return False


def debugx(msg: Union[str, int, dict]) -> None:
    '''
    echo debug msg
    '''
    msgs = f'debug {msg}'
    print(msgs)


def truncate(Dr: list, keys: list) -> list:
    #debugx(int(num*(10**n)))
    tmps = [Dr.count(x) for x in keys]
    mx = max(tmps)
    tmps = [[mx - x, 1][x == mx] for x in tmps]
    return tmps


def frommkeyx(Dx: list) -> list:
    tmps = [x for x in {}.fromkeys(Dx).keys()]
    RDX.shuffle(tmps)
    return tmps


def makenuxe(arglist: list) -> list:
    '''
    makenux for all cpu
    '''
    inx, D, R, B, i = arglist
    a, b, c = makenux(Data=D, Rlen=R, Blen=B, ins=i, depth=1)
    return [inx, a, b, c]


def makenux(Data: dict,
            Rlen: int,
            Blen: int,
            ins: str,
            depth: int = 1) -> list:
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
    dr, Rs = choicesrb(R_keys, weights_R, Rlen, depth + 1)
    db, Bs = choicesrb(B_keys, weights_B, Blen, depth + 1)
    rfind = Findins(Rs, Bs, insre=ins)
    if rfind == 'ERROR':
        return [dr, rfind, rfind]
    if rfind == True:
        return [dr, Rs, Bs]
    else:
        if dr < maxdep and db < maxdep:
            return makenux(Data, Rlen, Blen, ins, depth + 1)
        else:
            return [dr, [0], [0]]


def choicesrb(keys: list, weights: list, lens: int, depth: int = 1) -> list:
    '''
    keys list 待选列表
    weights list 权重
    len int 选择长度
    depth int 计算深度
    rdx = RDX.choices
    '''
    Jieguo = RDX.choices(keys, weights=weights, k=lens)
    Jieguo = [x for x in sorted(Jieguo)]
    if (La := len(Jieguo)) > (Lb := list(set(Jieguo)).__len__()):
        if depth < maxdep:
            return choicesrb(keys, weights, lens, depth + 1)
        else:
            return [depth, [0]]
    elif La == Lb:
        return [depth, Jieguo]
    else:
        if depth < maxdep:
            return choicesrb(keys, weights, lens, depth + 1)
        else:
            return [depth, [0]]


def Limit_input_r(r: int) -> int:
    '''
    Limit input R 6-19
    '''
    if r in range(6, 20):
        r = r
    else:
        r = 6
        print(f'{prompt} Change parameter R to 6')
    return r


def Limit_input_b(r: int) -> int:
    '''
    Limit input R 6-19
    '''
    if r in range(1, 17):
        r = r
    else:
        r = 1
        print(f'{prompt} Change parameter B to 1')
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

    def __init__(self, args: dict):
        '''
        action __init__
        '''
        self.args: dict = args if args != None else {
            'save': False,
            'r': 6,
            'b': 1
        }
        self.args['r'] = Limit_input_r(self.args['r'])
        self.args['b'] = Limit_input_b(self.args['b'])
        self.buffto.append(f'date {dtime.now()}')
        self.buffto.append(f'args {self.args}')
        debugx(self.args)

    def __fixrba__(self, rba: str) -> None:
        '''
        fix r b a
        rba is [ r, b, a ]
        '''
        cmds = {
            'r':
            lambda: [['R', [x for x in range(1, 34)]]],
            'b':
            lambda: [['B', [x for x in range(1, 17)]]],
            'a':
            lambda: [['R', [x for x in range(1, 34)]],
                     ['B', [x for x in range(1, 17)]]]
        }
        Zdict = cmds[rba]()
        for kn, vl in Zdict:
            # kn = R vl = [1,2,3,4,5,6...]
            kn_val = self.data.get(kn)
            fix_kn = [x for x in vl if x not in kn_val]
            if len(fix_kn) > 0:
                self.data[kn] += fix_kn
                print(f'{prompt} fix {kn} {fix_kn}')
        """ for kn, vl in Zdict:
            qsr = [x for x in l if x not in self.data[n]]
            if len(qsr) > 0:
                self.data[n] = self.data[n] + qsr
                print(f'{prompt} fix {n} {qsr}') """

    def __cpuse__(self, argb: str) -> None:
        '''
        '''
        cmds = {
            'o': lambda: self.__cpu_one__(),
            'a': lambda: self.__cpu_all__(),
        }
        cmds[argb]()

    def __echo__(self, Rexs: list) -> None:
        '''
        echo numbers
        '''
        inx, dep, Nr, Nb = Rexs
        if Nr == 'ERROR' or Nb == 'ERROR':
            print(f' ⠿ Error')
        # 发现错误 终止执行程序
        elif len(Nr) == self.args['r'] and len(Nb) == self.args['b']:
            lis = f'{" ".join([f"{x:02}" for x in Nr])} + {" ".join([f"{x:02}" for x in Nb])} '
            if self.args['noinx']:
                self.buffto.append(f'{prompt} {lis}')
            else:
                self.buffto.append(f'{prompt} {inx:>4} depth {dep:<5} {lis}')
            print(self.buffto[-1])

    def __cpu_one__(self) -> None:
        '''
        only cpu A run work
        '''
        N = [x for x in range(1, self.args['n'] + 1)]
        for nx in N:
            dep, Nr, Nb = makenux(self.data, self.args['r'], self.args['b'],
                                  self.args['ins'])
            self.__echo__([nx, dep, Nr, Nb])

    def __cpu_all__(self) -> None:
        '''
        use all cpu cores
        '''
        cpus = os.cpu_count()
        print(f'{prompt} cpus {cpus} maxdep {maxdep}')
        N = [[x, self.data, self.args['r'], self.args['b'], self.args['ins']]
             for x in range(1, self.args['n'] + 1)]
        with mlps.Pool(processes=cpus) as p:
            Retds = p.map(makenuxe, N)
            for item in Retds:
                self.__echo__(item)

    def act_for_dict(self) -> None:
        ''' anys dict '''
        if self.args['update']:
            # update
            getdata()
            return
        self.data = loaddata()
        if self.args['fix'] != None:
            # 执行 fix 程序
            self.__fixrba__(self.args['fix'])
        Prn(N=self.args['r'], B=self.args['b'])
        # cpu switch
        if self.args['cpu'] != None:
            self.__cpuse__(self.args['cpu'])

        if self.args['save']:
            if (fps := file_to('./save.log')) != None:
                with open(fps, 'w') as sto:
                    for slog in self.buffto:
                        sto.writelines(f'{slog}\n')
