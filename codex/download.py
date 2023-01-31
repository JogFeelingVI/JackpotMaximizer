#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-04 17:18:11
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-04 17:18:11

import urllib.request
import ssl

class get_html:
    ''' get download url '''
    text: str = ''

    def __init__(self, url: str) -> None:
        if url == None:
            raise ValueError("url cannot be None")
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=context) as response:
                rscode = response.read().decode('gb2312')
                self.text = rscode.encode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to retrieve content from URL ({url}), error: {str(e)}")

    @property
    def neirong(self) -> str:
        ''' get text '''
        return self.text