# - xxx as R|B 从这些待选列表中删除这些数字
# - 1 2 3 4 7 8 9 10 11 13 14 16 17 19 21 22 23 25 26 27 28 29 31 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 13 15 18 26 29 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# + 29 22 as R
+ 9 7 8 @bit1
- 6 8 9 10 14 15 17 18 22 25 26 28 29 30 31 @bit4
+ 15 17 19 29 31 33 @bit6
+ 2 3 4 8 10 11 @bit7