# - xxx as R|B 从这些待选列表中删除这些数字
# - 23 18 14 8 10 2 4 6 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 17 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# + 29 22 as R
+ 6 @bit1
+ 33 32 31 30 29 28 27 @bit6
+ 8 9 10 11 12 17 22 @bit2
- 9 12 15 17 20 23 25 28 31 @bit5
+ 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 @bit4

+ 1 5 7 8 9 @bit7
# bit7 * 8