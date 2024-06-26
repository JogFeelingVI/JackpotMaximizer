#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 17:48:34
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-01 00:00:42
import argparse


class loading:
    ''' command seting '''

    def __init__(self) -> None:
        self.command = argparse.ArgumentParser(
            'jpm.command',
            description='The name highlights that the program can help users win the jackpot',
            add_help=True,
            allow_abbrev=False)
        self.subparsers = self.command.add_subparsers()
        # update
        update_args = self.subparsers.add_parser(
            'update', help='Do not load network data')
        update_args.set_defaults(subcommand='update')

        # load
        load_args = self.subparsers.add_parser('load', help='generate number')
        load_args.add_argument('--dnsr',
                               default=True,
                               action='store_false',
                               help='Do not show results')

        load_args.add_argument('--noinx',
                               default=False,
                               action='store_true',
                               help='No Show ID DEPTH')
        load_args.add_argument('--fix',
                               type=str,
                               default='a',
                               choices=['r', 'b', 'a'],
                               help='repair data')
        load_args.add_argument('--cpu',
                               type=str,
                               default='a',
                               choices=['a', 'o'],
                               help='repair data')
        load_args.add_argument('--loadins',
                               default=False,
                               action='store_true',
                               help='load insx.reg')
        load_args.add_argument('--usew',
                               type=str,
                               default='s',
                               choices=['s', 'c', 'g'],
                               help='True choices not Weights')
        load_args.add_argument('--debug',
                               default=False,
                               action='store_true',
                               help='show debug info')
        load_args.add_argument(
            '--ins',
            default='(.*)',
            type=str,
            help=
            'Filtering numbers using regular expressions exp --ins ^(02|03|05)'
        )
        load_args.add_argument('-n',
                               default=25,
                               type=int,
                               help='Generate 10 pieces of data')
        load_args.add_argument('-r',
                               default=6,
                               type=int,
                               help='Red number default 6, max 20')
        load_args.add_argument('-b',
                               default=1,
                               type=int,
                               help='Default 1 blue ball, max 16')
        load_args.set_defaults(subcommand='load')

    def gparse(self) -> dict:
        ''' parse_args return dict '''
        args = self.command.parse_args()
        return args.__dict__
