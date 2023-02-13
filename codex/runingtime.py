# @Author: JogFeelingVi
# @Date: 2023-02-13 20:48:14
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2023-02-13 20:48:14
import time

prompt: str = '[+]'


def runingtime(fun):
    '''
    runing time
    '''

    def works():
        s = time.perf_counter()
        fun()
        print(f'{prompt} runingtime {time.perf_counter() - s:.2f} s')

    return works