#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39

from typing import Any, Callable, NoReturn, List


def file_to(name: str) -> str:
    '''
    File real path
    '''
    from codex.ospath import os_path
    fp = os_path.file_path(name)
    return fp


def getdata() -> NoReturn:
    ''' 
        gethtml 
        >03,18,23,24,25,32</span>|<span class="c_bule">09<  
        (?=.*[0-9])(?=.*[,])[0-9,]{17} R
        
    '''
    import re, json
    fp = file_to('./rbdata.json')
    from datetime import datetime as dtime
    from codex.download import get_html
    from codex.loadjson import Load_JSON, Resty
    html = get_html(Load_JSON(Resty.OxStr).read('UTXT')[1]).neirong()
    Rx = re.findall(b'(?=.*[0-9])(?=.*[,])[0-9,]{17}', html)
    Bx = re.findall(b'c_bule\">([0-9]{2})<', html)
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
        print(f':: updata network data sizeof {hszie}')


def loaddata() -> dict:
    '''
    load data
    '''
    import json
    fp = file_to('./rbdata.json')
    with open(fp, 'r') as rbdata:
        json_str = json.load(rbdata)
        print(':: loading buffer')
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
        import re
        try:
            sNr = ' '.join([f'{x:02}' for x in NR])
            sNb = ' '.join([f'{x:02}' for x in NB])
            sNums = f'{sNr} + {sNb}'
            Finx = len(re.findall(insre, sNums))
            return True if Finx >= 1 else False
        except re.error as rerror:
            print(f':: Findins error: {rerror.msg}')
            return 'ERROR'


def debugx(msg: Any) -> None:
    '''
    echo debug msg
    '''
    msgs = f'debug {msg}'
    print(msgs)


def truncate(avg, x):
    import math
    #debugx(int(num*(10**n)))
    integer = math.ceil(abs(avg - x))
    return integer


def makenux(Data: dict,
            Rlen: int,
            Blen: int,
            ins: str = None,
            depth: int = 1) -> list:
    '''
        data {'r': [1,2,3...], 'b':[1-16]}
        Rlen R len 1, 2, 3, 4, 5, 6 + Blen
        Blen B len 1 - 16
        ins '^(01|07)....'
    '''
    import random as RDX
    Dr = Data['R']
    Db = Data['B']
    R_keys = [x for x in {}.fromkeys(Dr).keys()]
    B_keys = [x for x in {}.fromkeys(Db).keys()]
    RDX.shuffle(R_keys)
    RDX.shuffle(B_keys)
    weights_R = [Data['R'].count(x) for x in R_keys]
    avg_r = sum(weights_R) / 33
    weights_R = [truncate(avg_r, x) for x in weights_R]
    # avg R
    weights_B = [Data['B'].count(x) for x in B_keys]
    avg_b = sum(weights_B) / 16
    weights_B = [truncate(avg_b, x) for x in weights_B]
    # avg B
    dr, Rs = choicesrb(R_keys, weights_R, Rlen, RDX.choices, depth + 1)
    db, Bs = choicesrb(B_keys, weights_B, Blen, RDX.choices, depth + 1)
    rfind = Findins(Rs, Bs, insre=ins)
    if rfind == 'ERROR':
        return [dr, rfind, rfind]
    if rfind == True:
        return [dr, Rs, Bs]
    else:
        if dr < 990 and db < 990:
            return makenux(Data, Rlen, Blen, ins, depth + 1)
        else:
            return [Dr, [0], [0]]


def choicesrb(keys: list,
              weights: list,
              lens: int,
              rdxfunx: Any,
              depth: int = 1) -> list:
    '''
    keys list 待选列表
    weights list 权重
    len int 选择长度
    depth int 计算深度
    rdx = RDX.choices
    '''
    Jieguo = rdxfunx(keys, weights=weights, k=lens)
    Jieguo = [x for x in sorted(Jieguo)]
    if (La := len(Jieguo)) > (Lb := list(set(Jieguo)).__len__()):
        if depth < 990:
            return choicesrb(keys, weights, lens, rdxfunx, depth + 1)
        else:
            return [depth, [0]]
    elif La == Lb:
        return [depth, Jieguo]
    else:
        if depth < 990:
            return choicesrb(keys, weights, lens, rdxfunx, depth + 1)
        else:
            return [depth, [0]]


def Limit_input_r(r: int) -> int:
    '''
    Limit input R 6-19
    '''
    if r >= 6 and r <= 19:
        return r
    elif r < 6:
        print(':: Change parameter R to 6')
        return 6
    elif r > 19:
        print(':: Change parameter R to 19')
        return 19


def Limit_input_b(r: int) -> int:
    '''
    Limit input R 6-19
    '''
    if r >= 1 and r <= 16:
        return r
    elif r < 1:
        print(':: Change parameter B to 1')
        return 1
    elif r > 16:
        print(':: Change parameter b to 16')
        return 16


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
    print(f':: N {N}, R {R}, BAST {Ld} CYN {Ld*2*B}')


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
    data = {}
    buffto = []

    def __init__(self, args: dict):
        from datetime import datetime as dtime
        self.args: dict = args if args != None else {'save': False}
        self.args['r'] = Limit_input_r(self.args['r'])
        self.args['b'] = Limit_input_b(self.args['b'])
        self.buffto.append(f'date {dtime.now()}')
        self.buffto.append(f'args {self.args}')
        debugx(self.args)

    def __fixrba__(self, rba: str) -> NoReturn:
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
        for n, l in Zdict:
            qsr = [x for x in l if x not in self.data[n]]
            if len(qsr) > 0:
                self.data[n] = self.data[n] + qsr
                print(f':: fix {n} {qsr}')

    def act_for_dict(self) -> NoReturn:
        ''' anys dict '''
        if self.args['update']:
            # update
            getdata()
            return 0
        self.data = loaddata()
        if self.args['fix'] != None:
            # 执行 fix 程序
            self.__fixrba__(self.args['fix'])
        Prn(N=self.args['r'], B=self.args['b'])
        N = [x for x in range(1, self.args['n'] + 1)]
        for nx in N:
            dep, Nr, Nb = makenux(self.data, self.args['r'], self.args['b'],
                                  self.args['ins'])
            if Nr == 'ERROR' or Nb == 'ERROR': break
            # 发现错误 终止执行程序
            if len(Nr) == self.args['r'] and len(Nb) == self.args['b']:
                lis = f'{" ".join([f"{x:02}" for x in Nr])} + {" ".join([f"{x:02}" for x in Nb])} '
                if self.args['noinx']:
                    self.buffto.append(f'N {lis}')
                else:
                    self.buffto.append(f'N {nx:>4} depth {dep:<5} {lis}')
                print(self.buffto[-1])
        if self.args['save']:
            with open(file_to('./save.log'), 'w') as sto:
                for slog in self.buffto:
                    sto.writelines(f'{slog}\n')
