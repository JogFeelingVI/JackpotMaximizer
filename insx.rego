# 注释行
# - xxx as R|B 从这些待选列表中删除这些数字
# - 17 24 25 34 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 13 15 18 26 29 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# 同一个位置可以指定多条规则 结果将是它们综合结果
# + 29 as R
+ 1 2 3 4 5 6 7 @bit1
+ 29 31 32 33 @vit6
+ 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 22 @bit2
+ 19 20 21 22 23 25 26 27 28 29 30 31 32 @bit5
+ 3 5 6 8 9 11 12 14 15 17 18 20 21 23 24 26 27 29 @bit3
+ 6 7 9 10 12 13 15 25 27 28 30 31 @bit4
+ 6 2 3 13 @bit7



