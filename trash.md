## trash code
```python
def randoms_b(Dlist: list, Count: int, depth: int = 0) -> list:
    ''' 
    已经废弃
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
```

```python
def randoms_r(Clist: list,
              Count: int,
              depth: int = 1,
              ins: str = None) -> list:
    ''' 
    已经废弃
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
        rfind = Findins(Jieguo, insre=ins)
        if rfind == 'ERROR': return [depth, rfind]
        if rfind == True:
            return [depth, Jieguo]
        else:
            if depth < 990:
                return randoms_r(Clist, Count, depth + 1, ins)
            else:
                return [depth, [0]]

```

```python
def Cji(lisd: list) -> int:
    '''
    n1*n2*n3..**(1/len(n))
    '''
    Rex = 1
    for x in lisd:
        Rex *= x
    return Rex**(1 / len(lisd))
```

```shell
debug {'save': False, 'update': True, 'noinx': False, 'fix': 'a', 'ins': '(.*)', 'n': 5, 'r': 6, 'b': 1}
Traceback (most recent call last):
  File "/Users/feelingvi/Downloads/GitHub/QuickLCK/qls.command", line 19, in <module>
    maix()
  File "/Users/feelingvi/Downloads/GitHub/QuickLCK/qls.command", line 15, in maix
    act.act_for_dict()
  File "/Users/feelingvi/Downloads/GitHub/QuickLCK/codex/funcs.py", line 259, in act_for_dict
    getdata()
  File "/Users/feelingvi/Downloads/GitHub/QuickLCK/codex/funcs.py", line 31, in getdata
    html = get_html(Load_JSON(Resty.OxStr).read('UTXT')[1]).neirong()
TypeError: __init__() should return None, not 'str'
```

```python
def choicesrb(keys: List, weights: List, lens: int, depth: int = 1) -> List:
    '''
    keys list 待选列表
    weights list 权重
    len int 选择长度
    depth int 计算深度
    rdx = RDX.choices
    '''
    Jieguo = RDX.choices(keys, weights=weights, k=lens)
    Jieguo = [x for x in sorted(Jieguo)]
    if len(Jieguo) != list(set(Jieguo)).__len__():
        if depth < maxdep:
            return choicesrb(keys, weights, lens, depth + 1)
        else:
            return [depth, [0]]
    else:
        return [depth, Jieguo]
```

```python
#old
    dr, Rs = choicesrb_dd(R_keys, weights_R, Rlen, depth)
    db, Bs = choicesrb_dd(B_keys, weights_B, Blen, depth)
    rinsx: mode_f = Findins(Rs, Bs, insre=ins)
    if rinsx == mode_f.Ok:
        return [dr, Rs, Bs]
    elif rinsx == mode_f.No:
        if dr < maxdep and db < maxdep:
            return makenux(Data, Rlen, Blen, ins, depth + 1)
        else:
            return [dr, [0], [0]]
    elif rinsx == mode_f.Er:
        return [dr, [0], [0]]
```