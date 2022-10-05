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


def randoms(Clist: list, Count: int, inx:int = 0) -> None:
    ''' 
    fromat info
    '''
    import random as RDX
    clis = list(set(Clist))
    weig = [Clist.count(x) for x in clis]
    Jieguo = RDX.choices(clis, weights=weig, k=Count)
    Jieguo = [x for x in sorted(Jieguo)]
    if len(Jieguo) > list(set(Jieguo)).__len__():
        randoms(Clist, Count,inx+1)
    else:
        print(f'inx {inx} {Jieguo}')


class action:
    ''' 执行脚本分析动作 '''
    data = {}

    def __init__(self, args: dict) -> None:
        self.args: dict = args if args != None else {'save': False}
        print(f'action self.args {self.args}')

    def act_for_dict(self):
        ''' anys dict '''
        self.data = getdata(self.args['update'])
        randoms(self.data['R'], self.args['r'])
