# JackpotMaximizer
> `JackpotMaximizer`：这个名字突出了程序可以帮助用户赢得头奖
###### usage: jpm.command load [-h] [--save] [--noinx] [--fix {r,b,a}] [--cpu {a,o}] [--loadins] [--usew {s,c,g}] [--debug] [--ins INS] [-n N] [-r R] [-b B]

* options:
  * -h, --help      show this help message and exit
  * --save          save to files
  * --noinx         No Show ID DEPTH
  * --fix {r,b,a}   repair data
  * --cpu {a,o}     repair data
  * --loadins       load insx.reg
  * --usew {s,c,g}  True choices not Weights
  * --debug         show debug info
  * --ins INS       Filtering numbers using regular expressions exp --ins ^(02|03|05)
  * -n N            Generate 10 pieces of data
  * -r R            Red number default 6, max 19
  * -b B            Default 1 blue ball, max 8
 
```shell
glns load -n10 --loadins                                                                                                                                                                      08:29:39
[+] loading buffer P[1, 15, 16, 20, 25, 27]
[+] fix B {2, 6, 13}
[+] objectives 6 -> 6 / 1 $ 2
[+] cpus 8 maxdep 3000
[c] use choices
[=] data 2024-01-03 08:31:20.189002
[-]    0 depth 1779  01 02 14 22 25 31 + 14 
[-]    1 depth 160   01 02 09 22 26 32 + 10 
[-]    2 depth 2848  01 02 09 17 23 31 + 14 
[-]    3 depth 1217  01 11 14 19 25 30 + 08 
[-]    4 depth 1517  01 02 14 24 25 30 + 16 
[-]
[-]    5 depth 1500  01 02 16 22 26 27 + 10 
[-]    6 depth 354   01 13 14 17 23 32 + 08 
[-]    7 depth 2241  01 15 19 20 26 27 + 09 
[-]    8 depth 1448  01 15 22 24 25 26 + 16 
[-]    9 depth 1362  01 02 16 20 25 29 + 01 
[+] Total 10 Notes
[+] runingtime 0.32 s
```
#### python3 jpm.command
> 执行主程序

#### --save
> 保存执行结果到 sava.log 文件

#### -n10
> 一次最多产生十注号码

#### --ins '^(03|05|07)\s(09|11)\s(10|12|18|20)\s(16|21|22|24)\s(.*)(28|30|32)'
> 这一条正则表达式，用来过滤号码，第一位数字限定在 03,05,07；第二位限定在 09,11;第三位限定在 10,12,18,20；第四位限定在16,21,22,24；第五位不做限制，第六位现在 28,30,32

## 参数说明
#### update 更新数据, 每次使用前都应该更新数据
#### load 进入主体功能
#### --debug 显示debug信息
#### --loadins 装载insx.rego 文件
#### --dnsr 是否显示最终结果 默认显示

#### --noinx 不显示辅助信息 
#### --cpu {o, a} 默认 a 全核心运行 o 单核心运行
#### --fix {r, b, a} r 修复红色号码区 b 修复蓝色号码区 a r+b
#### --usew {s, c, g} 使用三种不同的方式来随机号码，s 与历史记录毫无关系，c 最仅30期历史号码为依据随机号码，g 以统计历史作为依据，bitx.json 文件存储这些规律
#### --ins 用正则表达式限制号码
#### -n 产生注数 -n100
#### -r 产生号码的红色球数量, 最小6, 最大19
#### -b 产生号码的蓝色球数量, 默认1, 最大16


## linux macOS fish shell quick setup

#### Set file address
> ~/.config/fish/ `linux` `macos` `termux`
> edit config.fish

```shell
function glns
    python /data/data/com.termux/files/home/storage/downloads/github/JackpotMaximizer/jpm.command $argv
end
```
> `$argv` 传递参数

## insx.rego 文件规则说明
* `#` 注释行
* `- xxx as R｜B` 排除红色或蓝色号码, 每个号码用`空格`分割,数量不限. 注意R|B为大写
* `- 2 12 23 as R` 排除02,12,23这三个号码球
* `- 1 2 4 @bit1` 双色球号码第一位不可以出现 1 2 4
* `@bit[1-7]` bit1、bit2...bit6指红色号码球1 2 3 4 5 6,bit7指蓝色号码球,它们都支持 `+|-` 排除与限定

### insx.rego 文件内容
```insx.rag
# 注释行
# - xxx as R|B 从这些待选列表中删除这些数字
- 33 27 as R
#- 16 15 12 1 9 as B
# 必须包含 + 23 N.set_number_r 
# + 4 22 as R
+ 4 @bit1
- 5 6 7 8 9 12 @bit2
+ 10 11 12 13 14 15 16 17 18 @bit3
- 23 24 25 26 27 28 29 30 31 32 @bit4
#- 26 27 25 28 24 30 29 23 22 21 20 19 31 18 32 17 16 15 14 12 10 11 8 9 @bit5
- 33 31 30 29 28 27 @bit6
+ 1 16 12 15 9 @bit7
```

* `()\s\+\s()` 分割红号蓝号、可以在括号里面加入单独的限制条件，但优先级别低于 - xxx as R|B
* `0[4]\s.*(?=07|13|22).*` 第一位号码是04,后面的号码中必须出现 07|13|22 或出现其中之一 或全部出现


#### ins regex
* 在正则表达式后面加上排除 `'^(0[124])((?!22|24|05).)*$'`

#### 如何提高中将机率
* 提高双色球中奖概率的有效方法并不存在，因为双色球是一种概率游戏，中奖结果具有不确定性。但是，有一些技巧可以帮助您略微提高中奖的可能性：

    * 选择冷门号码： 冷门号码是指较少被选择的号码。虽然冷门号码中奖的概率与热门号码相同，但由于选择冷门号码的人较少，因此如果中奖，您将获得更高的奖金。
    * 选择跨度较大的号码： 跨度是指红球号码与蓝球号码之间的最大差值。一般来说，跨度较大的号码组合中奖的概率较高。
    * 选择邻近号码： 邻近号码是指相邻的两个或多个号码。邻近号码组合中奖的概率也相对较高。
    * 选择胆拖号码： 胆拖投注是指选择一个或多个胆码，然后从剩下的号码中选择若干个拖码。胆码必须出现在当期开奖号码中，拖码可以出现在当期开奖号码中，也* 可以不出现。胆拖投注可以提高中奖概率，但同时也增加了投注成本。
    * 使用数学方法选号： 有一些数学方法可以帮助您选择号码，例如：除3余1法、除3余2法、和值法、尾数法等。这些方法可以帮助您提高选号的准确率，但并不能保证中奖。

* 需要注意的是，以上技巧仅供参考，并不能保证中奖。双色球是一种概率游戏，中奖结果具有不确定性。理性购彩，量力而行。

#### glns 的中奖概率
```shell
python3 calculus.py                                                                                08:31:20
[+] loading buffer P[1, 15, 16, 20, 25, 27]
[+] fix B {2, 6, 13}
[+] moni cpus 8 maxdep 3000
[c] use choices
[=] data 2024-01-03 08:43:42.920207
[!] 1 Probability of Winning   0.00% 0
[!] 2 Probability of Winning   0.00% 0
[!] 3 Probability of Winning   0.14% 1
[!] 4 Probability of Winning   2.33% 17
[!] 5 Probability of Winning  10.70% 78
[!] 6 Probability of Winning  14.95% 109
[!] sum  28.12% Len 729 cyn -6267 $
[+] runingtime 11.72 s
```
> 在不计算一等奖和二等奖这类浮动奖金的情况下，每一千注彩票可以获得6267元纯收益。

#### 名字的由来
* LuckyPicker：这个名字简单易记，并且与程序的功能相关。
* LotteryOptimizer：这个名字突出了程序的功能，即优化乐透型彩票的中奖概率。
* ChanceEnhancer：这个名字传达了程序可以提高中奖概率的信息。
* FortuneBooster：这个名字暗示了程序可以带来好运和财富。
* `JackpotMaximizer`：这个名字突出了程序可以帮助用户赢得头奖。
