# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-10-15 21:58:18
from collections import Counter
import multiprocessing as mlps, os, re, enum, random as rdm, itertools as itr
from typing import List, Iterable, Union


class mode_f(enum.Enum):
    '''
    find mode ok, no, er
    '''
    Ok = 1
    No = 2
    Er = -1


class ccps:

    @staticmethod
    def ccp(a: Iterable, b: Iterable) -> itr.product:
        '''
        '''
        Lir = itr.combinations(a, 6)
        Lib = itr.combinations(b, 1)
        zipo = itr.product(Lir, Lib)
        return zipo

class random_rb:
    '''random R & B'''

    def __init__(self, rb: List[int], L: int) -> None:
        self.dep = [0] * L
        self.duilie = rb
        self.__nPool = []
        self.__weights = None
        self.__use_weights = False
    
    @property   
    def nPool(self):
        return self.__nPool
    
    @nPool.setter
    def nPool(self, value:List) -> None:
        self.__nPool = value
        
    @property
    def weights(self):
        return self.__weights
    
    @weights.setter
    def weights(self, value:List) -> None:
        self.__weights = value
        
    @property
    def use_weights(self) -> bool:
        return self.__use_weights
    
    @use_weights.setter
    def use_weights(self, value:bool) -> None:
        self.__use_weights = value

    def find_zero(self) -> int:
        '''find zero'''
        if 0 in self.dep:
            return self.dep.index(0)
        return -1

    def __initializations(self):
        '''initialization data'''
        if self.nPool == [] or self.weights == None:
            counter = Counter(self.duilie)
            total = max(counter.values())
            inverse_freq = {k: [total - v, 1][total == v] for k, v in counter.items()}
            self.nPool = list(inverse_freq.keys())
            self.weights = list(inverse_freq.values())

    def get_number(self):
        find = self.find_zero()
        if find == -1:
            return True

        if self.nPool == []:
            self.__initializations()
        if self.use_weights:
            result = rdm.choices(self.nPool, weights=self.weights, k=6)
        else:
            result = rdm.choices(self.nPool, k=6)
        for num in result:
            if self.__isok(n=num, index=find):
                self.dep[find] = num
                if self.get_number():
                    return True
                self.dep[find] = 0
        return False

    def __isok(self, n: int, index: int) -> bool:
        '''判断数字是否符合标准'''
        if n in self.dep:
            return False
        return True

class mLpool:
    cpu = os.cpu_count()
    mdep = 3000
    prompt = '[=]'

    __use_weights = False

    def __init__(self, data: dict, R: int, B: int, iRx: re.Pattern) -> None:
        self.data = data
        self.R = R
        self.B = B
        self.iRx = iRx

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
                self.iTx = p.map(self.makenuxe, N, chunksize=csize)
        else:
            self.iTx = [self.makenuxe(x) for x in N]
        return self.iTx

    def makenuxe(self, n: int) -> List:
        '''
        makenux for all cpu
        '''
        d, r, b = self.__SpawnPoolWorker()
        return [n, d, r, b]

    def __SpawnPoolWorker(self) -> List:
        '''
            data {'r': [1,2,3...], 'b':[1-16]}
            Rlen R len 1, 2, 3, 4, 5, 6 + Blen
            Blen B len 1 - 16
            ins '^(01|07)....'
            这个算法不够优秀
        '''
        #T1 = time.perf_counter()
        Dr = self.data['R']
        Db = self.data['B']
        depth: int = 1
        R_keys = self.__frommkeyx(Dr)
        B_keys = self.__frommkeyx(Db)
        weights_R = self.__truncate(Dr, R_keys)
        weights_B = self.__truncate(Db, B_keys)
        
        while True:

            Rs = self.__rdxchoices_N(R_keys, weights_R, self.R)
            Bs = self.__rdxchoices_N(B_keys, weights_B, self.B)
            # rinsx: mode_f = Findins(Rs, Bs, insre=ins)
            rinsx = self.__combinations_ols(Rs, Bs, insre=self.iRx)
            #print(f'{prompt} runingtime {time.perf_counter() - T1:.2f} s')
            if mode_f.Ok in rinsx:
                return [depth, Rs, Bs]
            depth += 1
            if depth >= self.mdep:
                return [depth, [0], [0]]

    def __frommkeyx(self, Dx: List) -> List:
        #tmps = list({}.fromkeys(Dx).keys())
        tmps = list(set(Dx))
        rdm.shuffle(tmps)
        return tmps

    def __truncate(self, Dr: List, keys: List) -> List:
        #debugx(int(num*(10**n)))
        tmps = [Dr.count(x) for x in keys]
        mx = max(tmps)
        tmps = [[mx - x, 1][x == mx] for x in tmps]
        return tmps

    def __rdxchoices(self, keys: List, weights: List, k: int) -> List[int]:
        numbers = set()
        while (lm := numbers.__len__()) < k:
            if self.__use_weights:
                selected = rdm.choices(keys, k=k - lm)
            else:
                selected = rdm.choices(keys, weights, k=k - lm)
            numbers |= set(selected)
        return sorted(numbers)
    
    def __rdxchoices_N(self, keys: List, weights: List, k: int) -> List[int]:
        rb_rand = random_rb(self.data['R'],L=k)
        rb_rand.nPool = keys
        rb_rand.weights = weights
        rb_rand.use_weights = self.UseWeights
        rb_rand.get_number()
        return sorted(rb_rand.dep)
        

    def __fdins(self, NR: Union[list, tuple], NB: Union[list, tuple],
                insre: re.Pattern) -> mode_f:
        '''
        Find Ins 
        Nums type list
        inse type str
        '''
        if insre == re.compile('(.*)'):
            # 不做任何限制
            return mode_f.Ok
        else:
            try:
                sNr = ' '.join([f'{x:02}' for x in NR])
                sNb = ' '.join([f'{x:02}' for x in NB])
                sNums = f'{sNr} + {sNb}'
                Finx = len(insre.findall(sNums))
                return mode_f.Ok if Finx >= 1 else mode_f.No
            except re.error as rerror:
                print(f'{self.prompt} Findins error: {rerror.msg}')
                return mode_f.Er

    def __combinations_ols(self, Rs: List[int], Bs: List[int],
                           insre: re.Pattern) -> List:
        '''
        '''
        zipo = ccps.ccp(Rs, Bs)
        ex_f_z = [self.__fdins(Lr, Lb, insre) for Lr, Lb in zipo]
        return ex_f_z
