#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-17 09:28:52
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-03 22:44:25
from pathlib import Path, PurePath
from typing import Union


class findAbsp:
    '''
    get os path /data/data/com.termux.com/file
    '''

    @staticmethod
    def path() -> Path:
        '''
        huo qu li jing
        '''
        path = Path(__file__).parent
        return path

    @staticmethod
    def file_path(file: str) -> str:
        '''
        huo qu wen jian lu jing
        '''
        path = findAbsp.path()
        jpm = f'{PurePath(path, "LICENSE")}'
        find = ''
        while 1:
            find = f'{PurePath(path, file)}'
            if not Path(find).exists():
                if Path(jpm).exists():
                    return find           
            else:
                break
            path = path.parent
        return find