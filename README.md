# QuickLCK
### Generate lucky numbers
 
```shell
python3 qls.command --save -n10 --ins '^(03|05|07)\s(09|11)\s(10|12|18|20)\s(16|21|22|24)\s(.*)(28|30|32)'
```
#### python3 qls.command
> 执行主程序

#### --save
> 保存执行结果到 sava.log 文件

#### -n10
> 一次最多产生十注号码

#### --ins '^(03|05|07)\s(09|11)\s(10|12|18|20)\s(16|21|22|24)\s(.*)(28|30|32)'
> 这一条正则表达式，用来过滤号码，第一位数字限定在 03,05,07；第二位限定在 09,11;第三位限定在 10,12,18,20；第四位限定在16,21,22,24；第五位不做限制，第六位现在 28,30,32

### 参数说明
#### --save 保存数据 save.log
#### --update 更新数据，每次使用前都应该更新数据
#### --noinx 不显示辅助信息 
#### --fix {r, b, a} r 修复红色号码区 b 修复蓝色号码区 a r+b
#### --ins 用正则表达式限制号码
#### -n 产生注数
#### -r 产生号码的红色球数量，最小6，最大19
#### -b 产生号码的蓝色球数量， 默认1，最大16


## linux macOS fish shell quick setup

#### Set file address
> ~/.config/fish/ `linux` `macos` `termux`
> edit config.fish

```shell
function glns
    python /data/data/com.termux/files/home/storage/downloads/github/QuickLCK/qls.command $argv
end
```
> $argv 传递参数