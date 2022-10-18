#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 17:48:34
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 17:48:34
import argparse
import string


class loading:
    ''' command seting '''

    def __init__(self) -> None:
        self.command = argparse.ArgumentParser(
            'qls.command',
            description='Generate lucky numbers',
            add_help=True,
            allow_abbrev=False)
        self.command.add_argument('--save',
                                  default=False,
                                  action='store_true',
                                  help='save to files')
        self.command.add_argument('--update',
                                  default=False,
                                  action='store_true',
                                  help='Do not load network data')
        self.command.add_argument('--noinx',
                                  default=False,
                                  action='store_true',
                                  help='No Show ID DEPTH')
        self.command.add_argument('--ins',
                                  default='(.*)',
                                  type=str,
                                  help='Filtering numbers using regular expressions exp --regx ^(02|03|05)')
        self.command.add_argument('-n',
                                  default=5,
                                  type=int,
                                  help='Generate 10 pieces of data')
        self.command.add_argument('-r',
                                  default=6,
                                  type=int,
                                  help='Red number default 6, max 20')
        self.command.add_argument('-b',
                                  default=1,
                                  type=int,
                                  help='Default 1 blue ball, max 16')

    def gparse(self) -> dict:
        ''' parse_args return dict '''
        args = self.command.parse_args()
        return args.__dict__