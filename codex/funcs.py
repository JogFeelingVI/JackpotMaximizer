#!/usr/bin/env python3
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
    if load:
        from codex.download import get_html
        from codex.loadjson import Load_JSON, Resty
        html = get_html(Load_JSON(Resty.OxStr).read('UTXT')[1]).neirong()
        with open('./buffer', 'wb') as buf:
            buf.write(html)
        print(':: updata network data')
    else:
        with open('./buffer', 'rb') as buf:
            html = buf.read()
        print(':: loading buffer')
    Rx = re.findall(b'(?=.*[0-9])(?=.*[,])[0-9,]{17}', html)
    Bx = re.findall(b'>([0-9]{2})<', html)
    Lix = {'R': [], 'B': []}
    for zitem in zip(Rx, Bx):
        R, B = zitem
        R = [int(x) for x in R.decode('utf-8').split(',')]
        B = int(B.decode('utf-8'))
        for Rz in R:
            Lix['R'].append(Rz)
        Lix['B'].append(B)
    return Lix


def randoms_b(Dlist: list, Count: int, depth: int = 0) -> list:
    ''' 
    fromat info
    maximum recursion depth exceeded in comparison max 16 min 1
    '''
    import random as BDX
    dlis = list(set(Dlist))
    weig = [Dlist.count(x) for x in dlis]
    Jieguo = BDX.choices(dlis, weights=weig, k=Count)
    Jieguo = [x for x in sorted(Jieguo)]
    if len(Jieguo) > list(set(Jieguo)).__len__():
        return randoms_r(Dlist, Count, depth + 1)
    else:
        return Jieguo


def randoms_r(Clist: list, Count: int, depth: int = 0) -> list:
    ''' 
    fromat info
    maximum recursion depth exceeded in comparison max 19 min 6
    '''
    import random as RDX
    clis = list(set(Clist))
    weig = [Clist.count(x) for x in clis]
    Jieguo = RDX.choices(clis, weights=weig, k=Count)
    Jieguo = [x for x in sorted(Jieguo)]
    if len(Jieguo) > list(set(Jieguo)).__len__():
        if depth < 990.01:
            return randoms_r(Clist, Count, depth + 1)
        else:
            print('Maximum recursion depth exceeded in comparison')
            print(f'Limit to 990, now {depth}')
            return [depth, [0]]
    else:
        return [depth, Jieguo]


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


class action:
    ''' 执行脚本分析动作 '''
    data = {}

    def __init__(self, args: dict) -> None:
        self.args: dict = args if args != None else {'save': False}
        self.args['r'] = Limit_input_r(self.args['r'])
        print(f'action args {self.args}')

    def act_for_dict(self):
        ''' anys dict '''
        self.data = getdata(self.args['update'])
        N = [x for x in range(1, self.args['n'] + 1)]
        for nx in N:
            dep, lis = randoms_r(self.data['R'], self.args['r'])
            lisb = randoms_b(self.data['B'], self.args['b'])
            print(f'N {nx:02} depth {dep:<5} {lis} + {lisb}')
