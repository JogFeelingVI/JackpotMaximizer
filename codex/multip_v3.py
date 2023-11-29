# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-11-29 09:35:43
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-29 21:57:33
import multiprocessing as mlps, re, itertools as itr, time
from typing import List, Iterable
from codex import glns_v2, rego_v2

mdep: int = 3000
prompt = '[=]'
class_funx = {}


def ccp(a: Iterable, b: Iterable) -> itr.product:
    '''
        '''
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def work_init(data: dict, usereego: bool = True):
    '''work init'''
    global class_funx
    glns = glns_v2.glnsMpls(data)
    filte = glns_v2.filterN_v2()
    filte.Last = glns.getlast
    filte.Lever = glns.getabc
    regox = rego_v2.rego().parse_dict
    class_funx.update({
        'glns': glns,
        'filte': filte,
        'rego': regox,
        'usereego': usereego
    })


def run_works(data: dict, n: int, mcp=True, rego=True):
    '''
        n == self.fmn
        mcp True use pool / False Use List
        '''
    N = range(n)
    if mcp:
        # processes=self.cpu
        with mlps.Pool(mlps.cpu_count(),
                       initializer=work_init,
                       initargs=(data, rego)) as p:
            csize = n // mlps.cpu_count()
            #print(f'csize {csize} {n//self.cpu} {[1, 0][n % self.cpu == 0]}  {n}')
            N = [N[i:i + csize] for i in range(0, n, csize)]
            # 从这里开始出现错误
            iTx = p.map(group_size, N)
            return itr.chain.from_iterable(iTx)
    else:
        return [SpawnPoolWorker(x) for x in N]


def group_size(N: Iterable):
    return [SpawnPoolWorker(x) for x in N]


def SpawnPoolWorker(index: int) -> List:
    '''
            data {'r': [1,2,3...], 'b':[1-16]}
            Rlen R len 1, 2, 3, 4, 5, 6 + Blen
            Blen B len 1 - 16
            ins '^(01|07)....'
    '''

    depth: int = 1
    while depth <= mdep:
        #st = time.time()
        n, t = class_funx['glns'].creativity()  #__glnsv2.creativity()
        rinsx = __combinations_ols(n, t)
        if rinsx == True:
            #print(f'OSID {os.getpid()} SpawnPoolWorker {time.time() - st:.4f}`s')
            return [index, depth, sorted(n), sorted(t)]
        depth += 1
    return [index, depth, [0], [0]]


def __combinations_ols(n, t) -> bool:
    '''
        '''
    zipo = ccp(n, t)
    for zio in zipo:
        if filter_map(zio) == True:
            return True
    return False


def filter_map(zipo_item) -> bool:
    Nr, Nb = zipo_item
    N = glns_v2.Note(Nr, Nb)
    # print(f'OSID {os.getpid()} init reego {time.time() - st:.4f}`s')
    # run rego
    if class_funx['usereego']:
        # 这里依然是问题所在
        # st = time.time()
        for parst in class_funx['rego'].values():
            st = time.time()
            if getattr(rego_v2.rego_filter, parst['name'])(N, parst) == False:
                return False
    # fins
    # if fdins(N, iRx) == False:
    #         #print(f'debug fdins FALSE')
    #     return False
    # filterv2
    for kfunc in class_funx['filte'].filters.values():
        if kfunc(N) == False:
            #print(f'filters {k:>8} FALSE N {N}')
            return False
        # mapfilter = map(lambda x:x(N), self.__filterv2.filters.values())
        # if False in mapfilter:
        #     return False
        #print(f'filters True N {N}')

    return True


def fdins(N: glns_v2.Note, insre: re.Pattern) -> bool:
    '''
        Find Ins 
        Nums type list
        inse type str
        '''
    if insre == re.compile(f'(.*)'):
        # 不做任何限制
        return True
    else:
        try:
            Finx = len(insre.findall(N))
            return True if Finx >= 1 else False
        except re.error as rerror:
            print(f'{prompt} Findins error: {rerror.msg}')
            return False
