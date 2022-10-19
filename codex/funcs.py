#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39


def getdata(load: True) -> dict:
    ''' 
        gethtml 
        >03,18,23,24,25,32</span>|<span class="c_bule">09<  
        (?=.*[0-9])(?=.*[,])[0-9,]{17} R
        
    '''
    import re
    from codex.ospath import os_path
    fp = os_path.file_path('./buffer')
    if load:
        from codex.download import get_html
        from codex.loadjson import Load_JSON, Resty
        from codex.ospath import os_path
        html = get_html(Load_JSON(Resty.OxStr).read('UTXT')[1]).neirong()
        with open(fp, 'wb') as buf:
            buf.write(html)
        print(':: updata network data')
    else:
        with open(fp, 'rb') as buf:
            html = buf.read()
        print(':: loading buffer')
    Rx = re.findall(b'(?=.*[0-9])(?=.*[,])[0-9,]{17}', html)
    Bx = re.findall(b'c_bule\">([0-9]{2})<', html)
    Lix = {'R': [], 'B': []}
    for zitem in zip(Rx, Bx):
        R, B = zitem
        R = [int(x) for x in R.decode('utf-8').split(',')]
        B = int(B.decode('utf-8'))
        for Rz in R:
            Lix['R'].append(Rz)
        Lix['B'].append(B)
    return Lix


def Findins(Nums: list, insre: str) -> bool:
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
        sNums = ' '.join([f'{x:02}' for x in Nums])
        Finx = len(re.findall(insre, sNums))
        return True if Finx >= 1 else False


def randoms_b(Dlist: list, Count: int, depth: int = 0) -> list:
    ''' 
    fromat info
    maximum recursion depth exceeded in comparison max 16 min 1
    '''
    import random as BDX
    dlis = [x for x in {}.fromkeys(Dlist).keys()]
    BDX.shuffle(dlis)
    if Count == 16:
        return [x for x in range(1, 17)]
    weig = [Dlist.count(x) for x in dlis]
    Jieguo = BDX.choices(dlis, weights=weig, k=Count)
    Jieguo = [x for x in sorted(Jieguo)]
    if len(Jieguo) > list(set(Jieguo)).__len__():
        return randoms_b(Dlist, Count, depth + 1)
    else:
        return Jieguo


def randoms_r(Clist: list,
              Count: int,
              depth: int = 1,
              ins: str = None) -> list:
    ''' 
    fromat info
    maximum recursion depth exceeded in comparison max 19 min 6
    '''
    import random as RDX
    clis = [x for x in {}.fromkeys(Clist).keys()]
    RDX.shuffle(clis)
    weig = [Clist.count(x) for x in clis]
    Jieguo = RDX.choices(clis, weights=weig, k=Count)
    Jieguo = [x for x in sorted(Jieguo)]
    # len(Jieguo) > list(set(Jieguo)).__len__():
    # 去除重复号码
    if (La := len(Jieguo)) > (Lb := list(set(Jieguo)).__len__()):
        if depth < 990:
            return randoms_r(Clist, Count, depth + 1, ins)
        else:
            return [depth, [0]]
    elif La == Lb:
        if Findins(Jieguo, insre=ins) == True:
            return [depth, Jieguo]
        else:
            if depth < 990:
                return randoms_r(Clist, Count, depth + 1, ins)
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


def Prn(N: int = 33, R: int = 6, B: int = 1) -> None:
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
    print(f'N {N}, R {R}, BAST {Ld} CYN {Ld*2*B}')


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

    def __init__(self, args: dict) -> None:
        from datetime import datetime as dtime
        self.args: dict = args if args != None else {'save': False}
        self.args['r'] = Limit_input_r(self.args['r'])
        self.args['b'] = Limit_input_b(self.args['b'])
        self.buffto.append(f'date {dtime.now()}')
        self.buffto.append(f'args {self.args}')
        print(f'action args {self.args}')

    def act_for_dict(self):
        ''' anys dict '''
        self.data = getdata(self.args['update'])
        Prn(N=self.args['r'], B=self.args['b'])
        N = [x for x in range(1, self.args['n'] + 1)]
        for nx in N:
            dep, lis = randoms_r(self.data['R'], self.args['r'], 0,
                                 self.args['ins'])
            if len(lis) == self.args['r']:
                lis = ' '.join([f'{x:02}' for x in lis])
                lisb = randoms_b(self.data['B'], self.args['b'])
                lisb = ' '.join([f'{x:02}' for x in lisb])
                if self.args['noinx']:
                    self.buffto.append(f'N {lis} + {lisb}')
                else:
                    self.buffto.append(
                        f'N {nx:>4} depth {dep:<5} {lis} + {lisb}')
                print(self.buffto[-1])
        if self.args['save']:
            with open('./save.log', 'w') as sto:
                for slog in self.buffto:
                    sto.writelines(f'{slog}\n')
