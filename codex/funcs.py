#!/usr/bin/env python3
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39


def gethtml():
    ''' gethtml 
        01,07,13,17,18,31</span>|<span class="c_bule">15</span>  
        ([\d]{2},[\d]{2},[\d]{2},[\d]{2},[\d]{2},[\d]{2})(.*)([\d]{2})
    '''
    from codex.download import get_html
    from codex.loadjson import Load_JSON, Resty
    html = get_html(Load_JSON(Resty.OxStr).read('UTXT')[1])
    return html.neirong()


class action:
    ''' 执行脚本分析动作 '''

    def __init__(self, args: dict) -> None:
        print(args)
        self.args: dict = args if args != None else {'save': False}
        print(f'action self.args {self.args}')

    def act_for_dict(self):
        ''' anys dict '''
        if 'NL' in self.args.keys():
            gethtml()
