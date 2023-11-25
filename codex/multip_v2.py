# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-25 20:37:49
import multiprocessing as mlps, os, re, itertools as itr
import time
from typing import List, Iterable
from codex import glns_v2, rego


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
    cpu = os.cpu_count()
    mdep = 3000
    prompt = '[=]'

    __use_weights = False
    __reego = False

    def __init__(self, data: dict, R: int, B: int, iRx: re.Pattern) -> None:
        print(f'{self.prompt} Use mLpooL V2')
        self.__glnsv2 = glns_v2.glnsMpls(data)
        self.__filterv2 = glns_v2.filterN_v2()
        self.__filterv2.Last = self.__glnsv2.getlast
        self.__filterv2.Lever = self.__glnsv2.getabc
        self.__class_rego = rego.rego()
        self.R = R
        self.B = B
        self.iRx = iRx

    @property
    def reego(self) -> bool:
        return self.__reego

    @reego.setter
    def reego(self, value: bool):
        self.__reego = value

    @property
    def UseWeights(self) -> bool:
        '''
        True choices not Weights
        False Use Weights
        '''
        return self.__use_weights

    @UseWeights.setter
    def UseWeights(self, value: bool):
        self.__use_weights = value

    def run_works(self, n: int, mcp=True) -> List:
        '''
        n == self.fmn
        mcp True use pool / False Use List
        '''
        N = range(n)
        if mcp:
            # processes=self.cpu
            with mlps.Pool() as p:
                if self.cpu == None:
                    self.cpu = 4
                csize = n // self.cpu + [1, 0][n % self.cpu == 0]
                # 从这里开始出现错误
                iTx = p.map(self.SpawnPoolWorker, N, chunksize=csize)
                return iTx
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
            n = self.__glnsv2.creativity()
            rinsx = self.__combinations_ols(N=n)
            if True in rinsx:
                return [index, depth, n.number, n.tiebie]
            depth += 1
        return [index, depth, [0], [0]]

    def filter_map(self, zipo_item) -> bool:
        Nr, Nb = zipo_item
        N = glns_v2.Note(Nr, Nb)
        # run rego
        if self.reego:
            # if self.__class_rego == None:
            #     #st = time.time()
            #     self.__class_rego = rego.rego()
            #     #print(f'OSID {os.getgid()} init reego {time.time() - st:.4f}`s')
            if self.__class_rego.filtration_olde(N) == False:
                return False
        # fins
        if self.fdins(N, self.iRx) == False:
            #print(f'debug fdins FALSE')
            return False
        # filterv2
        for kfunc in self.__filterv2.filters.values():
            if kfunc(N) == False:
                #print(f'filters {k:>8} FALSE N {N}')
                return False
        # mapfilter = map(lambda x:x(N), self.__filterv2.filters.values())
        # if False in mapfilter:
        #     return False
        #print(f'filters True N {N}')
        return True

    def filters(self, N: glns_v2.Note) -> bool:
        # fins
        if self.fdins(N, self.iRx) == False:
            #print(f'debug fdins FALSE')
            return False
        # filterv2
        for kfunc in self.__filterv2.filters.values():
            if kfunc(N) == False:
                #print(f'filters {k:>8} FALSE N {N}')
                return False
        # run rego
        if self.reego:
            if self.__class_rego == None:
                self.__class_rego = rego.rego()
                self.__class_rego.parse_v2()

            if self.__class_rego.filtration(N) == False:
                #print(f'rego FALSE N {N}')
                return False
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

    def __combinations_ols(self, N: glns_v2.Note) -> map:
        '''
        '''
        zipo = ccps.ccp(N.setnumber_R, N.setnumber_B)
        #ex_f_z = [self.filters(Note(Lr,Lb)) for Lr, Lb in zipo]
        return map(self.filter_map, zipo)
