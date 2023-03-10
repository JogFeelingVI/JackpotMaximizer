# QuickLCK
> Generate lucky numbers
> usage: qls.command [-h] [--save] [--update] [--noinx] [--fix {r,b,a}] [--cpu {a,o}] [--loadins] [--debug] [--ins INS]
                   [-n N] [-r R] [-b B]
 
```shell
glns --loadins -n10                                                                                                23:27:37
[+] loading buffer
[+] fix B [1, 7, 9]
[!] ---------------------------
[!] Regular error (3[320]|2[87)
[!] ---------------------------
[+] objectives 6 -> 6 / 1 $ 2
[+] cpus 4 maxdep 3000
[-]    1 depth 1     07 08 22 23 25 27 + 03
[-]    2 depth 1     10 18 23 25 26 30 + 07
[-]    3 depth 1     07 08 10 18 19 33 + 01
[-]    4 depth 4     07 10 13 14 17 31 + 09
[-]    5 depth 1     04 07 20 22 24 25 + 05
[-]
[-]    6 depth 1     02 03 13 16 23 29 + 03
[-]    7 depth 4     03 06 14 17 21 32 + 12
[-]    8 depth 1     03 16 17 18 30 31 + 12
[-]    9 depth 2     05 07 10 13 25 27 + 11
[-]   10 depth 1     01 09 14 22 25 26 + 16
[+] Total 10 Notes
[+] runingtime 0.44 s
```
#### python3 qls.command
> 执行主程序

#### --save
> 保存执行结果到 sava.log 文件

#### -n10
> 一次最多产生十注号码

#### --ins '^(03|05|07)\s(09|11)\s(10|12|18|20)\s(16|21|22|24)\s(.*)(28|30|32)'
> 这一条正则表达式，用来过滤号码，第一位数字限定在 03,05,07；第二位限定在 09,11;第三位限定在 10,12,18,20；第四位限定在16,21,22,24；第五位不做限制，第六位现在 28,30,32

## 参数说明
#### --debug 显示debug信息
#### --loadins 装载insx.reg 文件
#### --save 保存数据 save.log
#### --update 更新数据, 每次使用前都应该更新数据
#### --noinx 不显示辅助信息 
#### --cpu {o, a} 默认 a 全核心运行 o 单核心运行
#### --fix {r, b, a} r 修复红色号码区 b 修复蓝色号码区 a r+b
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
    python /data/data/com.termux/files/home/storage/downloads/github/QuickLCK/qls.command $argv
end
```
> `$argv` 传递参数

## insx.reg 文件规则说明
* `#` 注释行
* `- xxx as R｜B` 排除红色或蓝色号码, 每个号码用`空格`分割,数量不限. 注意R|B为大写
* `- 02 12 23 as R` 排除02,12,23这三个号码球

### insx.reg 文件内容
```insx.rag
# 注释行
# 每行一条数据
# - xxx as R|B 从这些待选列表中删除这些数字 ^-([\s\d]+)as [R|B]
# - 3 6 9 16 31 32 as R
# - 3 6 5 7 13 as B
# 23027 07 13 22
^
(0[4]\s.*(?=07|13|22).*)\s\+\s(03)
$
```

* `()\s\+\s()` 分割红号蓝号、可以在括号里面加入单独的限制条件，但优先级别低于 - xxx as R|B
* `0[4]\s.*(?=07|13|22).*` 第一位号码是04,后面的号码中必须出现 07|13|22 或出现其中之一 或全部出现

### glns --loadins
```shell
...
[+] cpus 8 maxdep 3000
[-]    1 depth 2     04 10 20 22 28 33 + 03
[-]    2 depth 1     04 13 14 18 22 29 + 03
[-]    3 depth 1     04 05 10 20 22 32 + 03
[-]    4 depth 1     04 15 18 19 22 28 + 03
[-]    5 depth 2     04 13 17 18 24 31 + 03
...
```

#### ins regex
* 在正则表达式后面加上排除 `'^(0[124])((?!22|24|05).)*$'`