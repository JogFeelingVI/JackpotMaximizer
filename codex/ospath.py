#!/usr/bin/env python
# @Author: JogFeelingVi 
# @Date: 2022-10-17 09:28:52 
# @Last Modified by:   By JogFeelingVi 
# @Last Modified time: 2022-10-17 09:28:52
import pathlib
class os_path:
    '''
    get os path /data/data/com.termux.com/file
    '''
    @staticmethod
    def path() -> str:
        '''
        huo qu li jing
        '''
        import os, sys
        path, _ = os.path.split(os.path.realpath(sys.argv[0]))
        return path
    
    @staticmethod
    def file_path(file:str) -> str:
        '''
        huo qu wen jian lu jing
        '''
        path = os_path.path()
        fp = f'{pathlib.PurePath(path, file)}'
        return fp if pathlib.Path(fp).exists() else ''