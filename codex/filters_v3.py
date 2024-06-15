# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-02-21 12:37:31
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-15 21:48:19
from collections import Counter
from typing import List
from functools import partial
import pathlib, json, inspect, itertools
from codex import ospath, note

CONF = {}


def parseNote(n: List[int], t: List[int]) -> note.Note:
    return note.Note(n, t)


def saveDictToJson(name: str, value: dict):
    """保存dict到json文件"""
    F = pathlib.Path(ospath.findAbsp.file_path(name))
    with F.open("w", encoding="utf-8") as Fopen:
        Fopen.write(json.dumps(value, indent=4))


def loadJsonToDict(name: str):
    """装载filte配置文件"""
    F = pathlib.Path(ospath.findAbsp.file_path(name))
    with F.open("r", encoding="utf-8") as Fopen:
        dicts = dict(json.loads(Fopen.read()))
        return dicts


def initialization():
    global CONF
    df = loadJsonToDict("DataFrame.json")
    fn = loadJsonToDict("filterN_v3.json")
    counter = Counter(df["R"])
    cold = [n for n, f in counter.most_common() if f < 5.01]
    fn["date"] = df["date"]
    fn["Last"] = df["R"][-6::]
    fn["Lever"] = cold
    CONF = fn
    saveDictToJson("filterN_v3.json", CONF)


def classAttrs():
    """
    按照配置表 返回哪些默认是需要被执行的
    """
    global CONF
    fter = []
    check = []
    for fterItem in CONF["filter"]:
        fter.append(fterItem["name"])
        if fterItem["checked"]:
            check.append(fterItem["name"])
    return [fter, check]


# Detailed configuration table
def Detailed_configuration_table():
    global CONF
    return CONF["filter"]


def Checkfunc():
    """默认选择器"""
    global CONF
    temp = SyntheticFunction()
    fter = {}
    for fterItem in CONF["filter"]:
        if fterItem["checked"]:
            fter[fterItem["name"]] = temp[fterItem["name"]]
    return fter


def SyntheticFunction():
    """全部过滤器"""
    global CONF
    funx = {}
    for method in inspect.getmembers(works):
        if inspect.isfunction(method[1]):
            funx.update({method[0]: method[1]})
    for fterItem in CONF["filter"]:
        if fterItem["name"] in funx.keys():
            args = [
                a.name
                for a in inspect.signature(funx[fterItem["name"]]).parameters.values()
                if a.name not in ["N", "n"]
            ]
            match args:
                case ["recommend"]:
                    func = partial(
                        funx[fterItem["name"]], recommend=fterItem["recommend"]
                    )
                case ["recommend", "Last"]:
                    func = partial(
                        funx[fterItem["name"]],
                        recommend=fterItem["recommend"],
                        Last=CONF["Last"],
                    )
                case ["recommend", "Lever"]:
                    func = partial(
                        funx[fterItem["name"]],
                        recommend=fterItem["recommend"],
                        Lever=CONF["Lever"],
                    )

            funx.update({fterItem["name"]: func})
    return funx


class works:

    @staticmethod
    def jmsht(N: note.Note, recommend: List[str]):
        five_map = {
            "J": [9, 10, 21, 22, 33],
            "M": [3, 4, 15, 16, 27, 28],
            "S": [1, 12, 13, 24, 25],
            "H": [6, 7, 18, 19, 30, 31],
            "T": [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32],
        }
        key_list = []
        for key, value_list in five_map.items():
            if any(num in value_list for num in N.setnumber_R):
                key_list.append(key)
        if len(key_list) in map(int, recommend):
            return True
        return False

    @staticmethod
    def dzx(N: note.Note, recommend: List[str]) -> bool:
        """xiao zhong da [2,2,2]"""

        g = [range(i + 1, i + 1 + 11) for i in range(0, 33, 11)]
        countofg = map(lambda x: N.setnumber_R.intersection(x).__len__(), g)
        flg = [f"{x}" for x in countofg]
        flg.reverse()
        flg = ":".join(flg)
        return [False, True][flg in recommend]

    @staticmethod
    def acvalue(N: note.Note, recommend: List[str]) -> bool:
        """计算数字复杂程度 默认 P len = 6 这里操造成效率低下"""
        f= lambda x: x[0]-x[1]
        p = itertools.product(N.number, N.number)
        ac = set(_n for x in p if (_n:=f(x)) > 0).__len__() - 1 - len(N.number)
        return [False, True][ac in map(int, recommend)]

    @staticmethod
    def linma(N: note.Note, recommend: List[str], Last: List[int]) -> bool:
        """计算邻码"""
        plus_minus = 0
        for n in N.number:
            if n + 1 in Last or n - 1 in Last:
                plus_minus += 1
                if plus_minus not in map(int, recommend):
                    return False
        return True

    @staticmethod
    def duplicates(N: note.Note, recommend: List[str], Last: List[int]) -> bool:
        """计算数组是否有重复项目"""
        duplic = N.setnumber_R & set(Last)
        return [False, True][duplic.__len__() in map(int, recommend)]

    @staticmethod
    def sixlan(N: note.Note, recommend: List[str]) -> bool:
        """判断红色区域是否等于 1, 2, 3, 4, 5, 6, 7"""
        sum_n = sum(N.setnumber_R)
        recommend_int = map(int, recommend)
        # print(f'{xi=} {da=} {sum(N.setnumber_R) =}')
        rb = any([x + 4.01 > sum_n > x - 3.9 for x in recommend_int])
        return rb

    @staticmethod
    def lianhao(n: note.Note, recommend: List[str]) -> bool:
        count = []
        for v in n.number:
            if not count or v != count[-1][-1] + 1:
                count.append([])
            count[-1].append(v)
        flgrex = sorted([len(v) for v in count if len(v) > 1])
        flg = x if (x := ":".join(map(str, flgrex))) != "" else "NA"

        return [False, True][flg in recommend]

    @staticmethod
    def mod2(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [["J", "O"][x % 2 == 0] for x in n.setnumber_R]
        _c = Counter(counts)
        flg = f'{_c["J"]}:{_c["O"]}'
        if flg not in recommend:
            return False
        return True

    @staticmethod
    def mod3(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in '2:2:2', '3:1:2', '3:2:1', '2:1:3', '2:3:1', '1:1:4', '3:0:3'"""
        counts = [f"{x%3}" for x in n.setnumber_R]
        _c = Counter(counts)
        flg = f'{_c["0"]}:{_c["1"]}:{_c["2"]}'
        if flg not in recommend:
            return False
        return True

    @staticmethod
    def mod4(n: note.Note, recommend: List[str]) -> bool:
        """mod 4 not in [[6], [5,1],[3,3]]"""
        counts = [x % 4 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def mod5(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [x % 5 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def mod6(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [x % 6 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def mod7(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [x % 7 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def mod8(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [x % 8 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def mod9(n: note.Note, recommend: List[str]) -> bool:
        """mod 3 not in [[6], [5,1],[3,3]]"""
        counts = [x % 9 for x in n.setnumber_R]
        if sum(counts) not in map(int, recommend):
            return False
        return True

    @staticmethod
    def dx16(n: note.Note, recommend: List[str]) -> bool:
        """
        da:xiao 1:5 n > 16.02 is da
        """
        f = lambda x: x > 16.02
        s = [["X", "D"][f(x)] for x in n.setnumber_R]
        counts = Counter(s)
        flg = f'{counts["D"]}:{counts["X"]}'
        if flg not in recommend:
            return False
        return True

    @staticmethod
    def zhihe(n: note.Note, recommend: List[str]) -> bool:
        """
        da:xiao 1:5 n > 16.02 is da
        """
        z = (1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
        s = [["H", "Z"][x in z] for x in n.setnumber_R]
        _c = Counter(s)

        flg = f'{_c["Z"]}:{_c["H"]}'
        # + _b =False list(_L) = [9, 10, 25, 30, 32]
        # + _b =True list(_L) = [13]
        if flg not in recommend:
            return False
        return True

    @staticmethod
    def coldns(n: note.Note, recommend: int, Lever: List[int]) -> bool:
        """
        这个方法会造成命中率降低弃用
        [(4, 1), (20, 3), (7, 3), (23, 3), (21, 3), (2, 4), (29, 4), (28, 4), (5, 4), (12, 4), (17, 4)]
        """
        # ninc = set(Lever).intersection(n.number).__len__()
        # if ninc == 0 or ninc <= recommend:
        #     return False
        return True

    @staticmethod
    def onesixdiff(n: note.Note, recommend: List[str]) -> bool:
        """1 - 6 diff > 15.06"""
        _cha = abs(n.index(1) - n.index(6))
        recommend_int = map(int, recommend)
        rb = any([x + 2.5 > _cha > x - 2.4 for x in recommend_int])
        return rb
