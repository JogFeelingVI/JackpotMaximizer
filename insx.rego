# - xxx as R|B 从这些待选列表中删除这些数字
# - 23 18 14 8 10 2 4 6 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 17 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# + 29 22 as R
+ 10 12 14 16 @bit7
+ 5 @bit1
+ 2 3 4 5 6 7 8 9 10 11 12 13 @bit2
+ 7 9 11 13 15 17 19 21 @bit3
+ 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 @bit4
+ 18 19 20 21 22 23 24 25 26 27 28 29 30 31 @bit5
+ 21 22 23 24 25 26 27 28 29 30 31 32 33 @bit6
# bit7 * 8