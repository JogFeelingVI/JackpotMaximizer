# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-19 14:34:34
import multiprocessing as mlps, os, re, itertools as itr
from typing import List, Iterable
from codex import glns_v2
from codex.rego import rego, Note


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
    __class_rego = None

    def __init__(self, data: dict, R: int, B: int, iRx: re.Pattern) -> None:
        print(f'{self.prompt} Use mLpooL V2')
        self.__glnsv2 = glns_v2.glnsMpls(data)
        #print(f'debug {self.__glnsv2.maxjac_v2([3, 8, 19, 22, 26, 32])}')
        self.__filterv2 = glns_v2.filterN_v2()
        self.__filterv2.Last = self.__glnsv2.getlast
        self.__filterv2.Lever = self.__glnsv2.getabc
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
        N = [x for x in range(1, n + 1)]
        if mcp:
            with mlps.Pool(processes=self.cpu) as p:
                ns = n / [self.cpu, 4][self.cpu == None]
                csize = [int(ns), 1][ns < 1]
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
            这个算法不够优秀
        '''
        depth: int = 1
        while depth <= self.mdep:
            n = self.__glnsv2.creativity()
            rinsx = self.__combinations_ols(N=n)
            if True in rinsx:
                #print(f'{self.prompt} runingtime {rinsx} s')
                return [index, depth, n.number, n.tiebie]
            depth += 1
        return [index, depth, [0], [0]]

    def filter_map(self, zipo_item) -> bool:
        Nr, Nb = zipo_item
        N = Note(Nr, Nb)
        # run rego
        if self.reego:
            if self.__class_rego == None:
                self.__class_rego = rego()
                self.__class_rego.parse_v2()

            if self.__class_rego.filtration_olde(N) == False:
                #print(f'rego FALSE N {N}')
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
        #print(f'filters True N {N}')
        return True

    def filters(self, N: Note) -> bool:

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
                self.__class_rego = rego()
                self.__class_rego.parse_v2()

            if self.__class_rego.filtration(N) == False:
                #print(f'rego FALSE N {N}')
                return False
        #print(f'filters True N {N}')
        return True

    def fdins(self, N: Note, insre: re.Pattern) -> bool:
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
                sNr = ' '.join([f'{x:02}' for x in N.setnumber_R])
                sNb = ' '.join([f'{x:02}' for x in N.setnumber_B])
                sNums = f'{sNr} + {sNb}'
                Finx = len(insre.findall(sNums))
                return True if Finx >= 1 else False
            except re.error as rerror:
                print(f'{self.prompt} Findins error: {rerror.msg}')
                return False

    def __combinations_ols(self, N: Note) -> map:
        '''
        '''
        zipo = ccps.ccp(N.setnumber_R, N.setnumber_B)
        #ex_f_z = [self.filters(Note(Lr,Lb)) for Lr, Lb in zipo]
        ex_f_z = map(self.filter_map, zipo)
        return ex_f_z
