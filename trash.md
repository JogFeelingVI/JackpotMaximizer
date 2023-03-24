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
## 判断一组数字是否为等差数列
```python
def is_arithmetic_progression(numbers):
    if len(numbers) <= 2:
        return False
    common_difference = numbers[1] - numbers[0]
    for i in range(2, len(numbers)):
        if numbers[i] - numbers[i - 1] != common_difference:
            return False
    return True

numbers = [1, 3, 5, 7, 9]
if is_arithmetic_progression(numbers):
    print("The list is an arithmetic progression.")
else:
    print("The list is not an arithmetic progression.")

```
> 在这个代码中，我们定义了一个函数 is_arithmetic_progression，该函数接收一个参数 numbers，表示要判断的数字列表。在函数内部，使用循环语句和判断语句，判断相邻两项的差值是否相等。如果相等，则返回 True，否则返回 False。

## 在 Python 中，可以使用循环语句和算数运算符来计算等比数列。

> 首先，需要知道等比数列的首项和公比，然后使用循环语句通过公比不断地乘以首项，计算出整个等比数列。

#### 代码如下：
```python
def generate_geometric_progression(first_term, common_ratio, n):
    result = [first_term]
    for i in range(1, n):
        result.append(result[i - 1] * common_ratio)
    return result

first_term = 2
common_ratio = 3
n = 5
result = generate_geometric_progression(first_term, common_ratio, n)
print(result)

```

> 在这个代码中，我们定义了一个函数 generate_geometric_progression，该函数接收三个参数：first_term 表示等比数列的首项，common_ratio 表示等比数列的公比，n 表示要计算的项数。在函数内部，使用循环语句通过公比不断地乘以首项，计算出整个等比数列。最后，将结果存储在列表中并返回。

## 计算数组的散列度（hash dispersion）可以用于评估数组内元素的分布情况，进而判断散列函数的性能。

> 一种常用的计算散列度的方法是使用桶的数量和每个桶中元素的数量之比。

### 以下是用 Python 计算固定长度数组的散列度的代码示例：

```python
def calculate_hash_dispersion(arr, bucket_count):
    # 创建桶
    buckets = [0] * bucket_count

    # 遍历数组，统计每个桶中元素的数量
    for value in arr:
        bucket_index = hash(value) % bucket_count
        buckets[bucket_index] += 1

    # 计算散列度
    dispersion = 0
    for count in buckets:
        dispersion += (count - len(arr) / bucket_count) ** 2

    return dispersion / len(arr)

```

> 在上面的代码中，我们首先创建了 bucket_count 个桶，并使用每个元素的散列值将其分配到相应的桶中。然后，我们使用每个桶中元素的数量计算散列度。散列度越低，说明元素的分布越均匀，散列函数的性能越好。

```python
def rdxchoices_x(keys: List, weights: List, k: int) -> list[int]:
    ''' 系统缓慢根本问题
    '''
    choi = [0] * k
    while 0 in choi:
        if keys.__len__() > 0:
            i = choi.index(0)
            kv = RDX.choices(keys, weights=weights, k=1)[-1]
            ki = keys.index(kv)
            choi[i] = kv
            keys.pop(ki)
            weights.pop(ki)
        else:
            i = choi.index(0)
            choi.pop(i)
    return choi
```

```python
@staticmethod
    def distribute(
        D: dict,
        R: int,
        B: int,
        P: re.Pattern,
        max: int = 6,
    ) -> list:
        ''' '''
        base = [0, {}, 0, 0, '(.*)']
        Nx = [base] * max
        counter = 1
        while True:
            if base in Nx:
                index = Nx.index(base)
                Nx[index] = [counter, D, R, B, P]
                counter += 1
            else:
                break
        return Nx
```