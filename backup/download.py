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
    headers = {
        'GET': '/zoushitu/cjwssq/hqfgzglclrw.html HTTP/1.1',
        'Cookie':
        'wzws_sessionid=gWYwOTdkMIJhM2UyZmWgZEXfGYAxNzEuNDMuNzAuMTM3; PHPSESSID=6345a3df94ae7a3e9cfc807c26ce6a23; Hm_lvt_17c098d74ec9e8dd63ced946aa8ac16d=1682231834,1682235355',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'm.cjcp.cn',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    def __init__(self, url: str) -> None:
        if url == None:
            raise ValueError("url cannot be None")
        try:
            #context = ssl.SSLContext()
            context = ssl._create_unverified_context()
            req = urllib.request.Request(
                url,
                headers=self.headers,
            )
            response = urllib.request.urlopen(url=req, context=context)
            if response.status == 200:
                html_content = response.read().decode('utf-8')
                self.text = html_content
            else:
                self.text = f"Error: {response.status}"
        except Exception as e:
            raise ValueError(
                f"Failed to retrieve content from URL ({url}), error: {str(e)}"
            )

    @property
    def neirong(self) -> str:
        ''' get text '''
        return self.text