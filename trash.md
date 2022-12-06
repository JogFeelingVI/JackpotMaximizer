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