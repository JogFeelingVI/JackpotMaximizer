# @Author: JogFeelingVi
# @Date: 2023-02-13 20:48:14
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-12-10 08:08:45
import time

prompt: str = '[+]'


def runingtime(fun):
    '''
    runing time
    '''

    def works():
        s = time.time()
        fun()
        print(f'{prompt} runingtime {time.time() - s:.2f} s')

    return works
