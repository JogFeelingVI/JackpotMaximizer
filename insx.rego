# - xxx as R|B 从这些待选列表中删除这些数字
# - 8 18 as R
# - 13 2 3 6 11 7 12 15 as B
# 必须包含 + 23 as R 只针对 R
# + 13 15 18 26 29 as R
# bit1 需要出现的数字 +|- 1 2 3 4 5 6 7 @bit[1-7]
# + 5 14 15 16 17 23 24 25 26 27 28 29 30 as R
+ 4 6 9 10 12 @bit1
# + 3 5 7 11 13 17 19 23 29 @bit3
+ 26 27 25 28 24 30 23 29 @bit5
+ 2 3 4 5 6 7 8 10 11 13 14 @bit7