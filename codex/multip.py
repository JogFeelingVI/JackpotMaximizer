# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-10-29 06:01:31
from collections import Counter
import multiprocessing as mlps, os, re, enum, random as rdm, itertools as itr
from typing import List, Iterable, Union
from codex.rego import rego, Note


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
    def nPool(self, value: List) -> None:
        self.__nPool = value

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, value: List) -> None:
        self.__weights = value

    @property
    def use_weights(self) -> bool:
        return self.__use_weights

    @use_weights.setter
    def use_weights(self, value: bool) -> None:
        self.__use_weights = value

    def remake(self) -> None:
        '''重新开始'''
        self.dep = [0] * len(self.dep)

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
            inverse_freq = {
                k: [total - v, 1][total == v]
                for k, v in counter.items()
            }
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


# end class
class mLpool:
    cpu = os.cpu_count()
    mdep = 3000
    prompt = '[=]'

    __use_weights = False
    __reego = False
    __class_rego = None

    def __init__(self, data: dict, R: int, B: int, iRx: re.Pattern) -> None:
        self.data = data
        self.rdada = self.data['R']
        self.groupby = [
            self.rdada[i:i + 6] for i in range(0, len(self.rdada), 6)
        ]
        self.last = self.rdada[-6:]
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
                self.iTx = p.map(self.makenuxe, N, chunksize=csize)
        else:
            self.iTx = [self.makenuxe(x) for x in N]
        return self.iTx

    def makenuxe(self, n: int) -> List:
        '''
        makenux for all cpu
        这里可以修改为 r, b = Note
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
        fix_r = self.data['R'] + self.data.get('fix_R', [])
        fix_b = self.data['B'] + self.data.get('fix_B', [])
        Dr = random_rb(fix_r, self.R)
        Db = random_rb(fix_b, self.B)
        depth: int = 1

        while True:
            Rs = self.__rdxchoices_N(Dr)
            Bs = self.__rdxchoices_N(Db)
            # rinsx: mode_f = Findins(Rs, Bs, insre=ins)
            rinsx = self.__combinations_ols(Rs, Bs)
            #print(f'{self.prompt} runingtime {rinsx:.2f} s')
            if mode_f.Ok in rinsx:
                return [depth, Rs, Bs]
            if depth >= self.mdep:
                return [depth, [0], [0]]
            depth += 1
            Dr.remake()
            Db.remake()

    def __rdxchoices_N(self, rand: random_rb) -> List[int]:
        rand.use_weights = self.UseWeights
        rand.get_number()
        return sorted(rand.dep)

    def filters(self, N: Note) -> mode_f:

        funx = {
            'fdins': lambda n, i: self.__fdins(n, i),
            'lianhao': lambda n, i: self.__lianhao(n),
            'linma': lambda n, i: self.__linma(n),
            'dzx': lambda n, i: self.__dzx(n),
            'jaccard': lambda n, i: self.__jaccard(n),
        }
        refilte = [f(N, self.iRx) for k, f in funx.items()]
        if self.reego and self.__class_rego == None:
            self.__class_rego = rego()
            self.__class_rego.parse()
        if self.reego and self.__class_rego != None:
            erbool = self.__class_rego.filtration(N)
            refilte.append([mode_f.No, mode_f.Ok][erbool])

        if mode_f.No in refilte:
            return mode_f.No
        else:
            return mode_f.Ok

    def __fdins(self, N: Note, insre: re.Pattern) -> mode_f:
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
                sNr = ' '.join([f'{x:02}' for x in N.setnumber_R])
                sNb = ' '.join([f'{x:02}' for x in N.setnumber_B])
                sNums = f'{sNr} + {sNb}'
                Finx = len(insre.findall(sNums))
                return mode_f.Ok if Finx >= 1 else mode_f.No
            except re.error as rerror:
                print(f'{self.prompt} Findins error: {rerror.msg}')
                return mode_f.Er

    def __lianhao(self, N:Note) -> mode_f:
        count = []
        for n in N.number:
            if not count or n != count[-1][-1] + 1:
                count.append([])
            count[-1].append(n)
        flgrex = sorted([len(n) for n in count if len(n) > 1])
        rebool = [mode_f.No, mode_f.Ok][flgrex in [[], [3], [2], [2, 2]]]
        return rebool

    def __linma(self, N:Note) -> mode_f:
        count = []

        for n in N.number:
            if n + 1 in self.last or n - 1 in self.last:
                count.append(n)
        reboot = [mode_f.No, mode_f.Ok][len(count) in [0, 1, 2, 3]]
        return reboot
    
    def __dzx(self, N:Note) -> mode_f:
        a = range(1, 34)
        g = [a[i:i+11] for i in range(0, len(a), 11)]
        count = [[],[],[]]
        for ai in N.setnumber_R:
            index = 1
            while True:
                if ai in g[index]:
                    count[index].append(ai)
                    break
                else:
                    if ai < min(g[index]):
                        index -= 1
                    if ai > max(g[index]):
                        index += 1
        flgrex = [len(x) for x in count]
        rebool = [mode_f.No, mode_f.Ok][5 not in flgrex or 6 not in flgrex]
        return rebool

    def __combinations_ols(self, Rs: List[int], Bs: List[int]) -> List:
        '''
        '''
        zipo = ccps.ccp(Rs, Bs)
        ex_f_z = [self.filters(Note(Lr,Lb)) for Lr, Lb in zipo]
        return ex_f_z

    def __jaccard(self, N:Note):
        '''雅卡尔相似数'''

        def jc(a: List, b) -> float:
            sa = set(a)
            sb = set(b)
            intersection = len(sa.intersection(sb))
            union = len(sa.union(sb))
            return intersection / union

        jcduilie = [jc(x, N.number) for x in self.groupby]
        reboot = [False, True][max(jcduilie) < 0.24]
        return reboot
