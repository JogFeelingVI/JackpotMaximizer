# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   Your name
# @Last Modified time: 2023-12-22 21:05:31
from datetime import datetime as dtime
import multiprocessing as mlps, re, itertools as itr, time, os
from typing import List, Iterable
from codex import glns_v2, rego_v2


class ccps:

    @staticmethod
    def ccp(a: Iterable, b: Iterable) -> itr.product:
        '''
        '''
        Lir = itr.combinations(a, 6)
        Lib = itr.combinations(b, 1)
        zipo = itr.product(Lir, Lib)
        return zipo


# end class
class mLpool:
    mdep = 3000
    prompt = '[=]'

    __reego = False

    def __init__(self,
                 data: dict,
                 R: int,
                 B: int,
                 iRx: re.Pattern,
                 w: str = 'w') -> None:
        '''
        w False is not usew
        '''
        self.glnsv2 = glns_v2.glnsMpls(data, w=w)
        self.filterv2 = glns_v2.filterN_v2()
        self.filterv2.Last = self.glnsv2.getlast
        self.filterv2.Lever = self.glnsv2.getabc
        self.class_rego = rego_v2.rego().parse_dict
        self.R = R
        self.B = B
        self.iRx = iRx

    @property
    def reego(self) -> bool:
        return self.__reego

    @reego.setter
    def reego(self, value: bool):
        self.__reego = value

    def run_works(self, n: int, mcp=True):
        '''
        n == self.fmn
        mcp True use pool / False Use List
        f'date {dtime.now()}'
        '''
        print(f'{self.prompt} data {dtime.now()}')
        N = range(n)
        if mcp:
            # processes=self.cpu
            csize = int(n * 0.083)
            if csize <= 30:
                return [self.SpawnPoolWorker(x) for x in N]
            with mlps.Pool() as p:
                return p.map(self.SpawnPoolWorker, N, chunksize=csize)
        else:
            return [self.SpawnPoolWorker(x) for x in N]

    def SpawnPoolWorker(self, index: int) -> List:
        '''
            data {'r': [1,2,3...], 'b':[1-16]}
            Rlen R len 1, 2, 3, 4, 5, 6 + Blen
            Blen B len 1 - 16
            ins '^(01|07)....'
        '''
        # print(f'GID {os.getpid():>10} index {index}')
        depth: int = 1
        while depth <= self.mdep:
            #st = time.time()
            n, t = self.glnsv2.creativity()

            rinsx = self.__combinations_ols(n, t)
            if rinsx == True:
                #print(f'OSID {os.getpid()} SpawnPoolWorker {time.time() - st:.4f}`s')
                return [index, depth, n, t]
            depth += 1
        return [index, depth, [0], [0]]

    def filter_map(self, zipo_item) -> bool:
        Nr, Nb = zipo_item
        N = glns_v2.Note(Nr, Nb)

        # run rego
        if self.reego:
            # 这里依然是问题所在
            for k, parst in self.class_rego.items():
                rex = parst['f'](N, parst['a'])
                #rex = self.class_rego.Func[parst['name']](N, parst)
                if rex == False:
                    return False

        # fins
        if self.fdins(N, self.iRx) == False:
            #print(f'debug fdins FALSE')
            return False
        # filterv2
        for kfunc in self.filterv2.filters.values():
            if kfunc(N) == False:
                #print(f'filters {k:>8} FALSE N {N}')
                return False
        # mapfilter = map(lambda x:x(N), self.__filterv2.filters.values())
        # if False in mapfilter:
        #     return False
        #print(f'filters True N {N}')
        return True

    def fdins(self, N: glns_v2.Note, insre: re.Pattern) -> bool:
        '''
        Find Ins 
        Nums type list
        inse type str
        '''
        if insre == re.compile('(.*)'):
            # 不做任何限制
            return True
        else:
            try:
                Finx = len(insre.findall(N))
                return True if Finx >= 1 else False
            except re.error as rerror:
                print(f'{self.prompt} Findins error: {rerror.msg}')
                return False

    def __combinations_ols(self, n, t) -> bool:
        '''
        '''
        zipo = ccps.ccp(n, t)
        for zio in zipo:
            if self.filter_map(zio) == True:
                return True
        return False
