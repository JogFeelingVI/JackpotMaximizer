# - xxx as R|B 从这些待选列表中删除这些数字
# - 8 18 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 13 15 18 26 29 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# + 5 14 15 16 17 23 24 25 26 27 28 29 30 as R
+ 3 4 6 @bit1
- 6 7 10 14 15 18 22 23 26 @bit3
+ 22 32 @bit6
+ 3 13 @bit7