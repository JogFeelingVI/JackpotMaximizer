#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-04 17:18:11
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-04 17:18:11

import urllib.request


class get_html:
    ''' get download url '''
    text = ''

    def __init__(self, url: str) -> None:
        if url == None:
            return None
        try:
            self.text = urllib.request.urlopen(url).read()
        except:
            self.text = ''

    def neirong(self) -> str:
        ''' get text '''
        return self.text