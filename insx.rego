# 注释行
# - xxx as R|B 从这些待选列表中删除这些数字
# - 20 as R
- 13 6 as B
# 必须包含 + 23 as R 只针对 R
# + 13 15 18 26 29 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# 同一个位置可以指定多条规则 结果将是它们综合结果
+ 29 28 15 11 as R
+ 1 2 3 4 5 6 7 @bit1
+ 25 @bit6
+ 5 6 7 9 10 12 @bit2
+ 17 18 19 20 @bit5
+ 5 8 11 14 17 20 23 26 29 @bit3
#+ 29 6 31 5 @bit4


