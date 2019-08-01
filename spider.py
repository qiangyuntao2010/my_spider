#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Sun Jun 30 23:23:14 2019

author: 一文 --最远的你们是我最近的爱
'''

import re
import sys
import requests

from proxy_api import get_proxies

class Spider:
    
       
    def __init__(self, is_proxy = False):
        
        if is_proxy == True:#如果请求要使用代理则拉取代理
            
            self.get_proxy()
        self.proxy = False   #指定是否使用代理

        self.headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}    
    
    def get_proxy(self):
        
        '''
        
        调用get_proxies()方法
        
        一个面象管道提取代理的方法，详细介绍见proxy_api.py
        
        将get_proxies()方法调取的代理处理成供requests发起请求时传给proxies参数的形式
        
        return:  {'http': 'http://223.240.211.23:28500', 
        
                  'https': 'http://223.240.211.23:28500'}
        
        
        供requests发起请求时传给proxies参数
        
        
        
        
        '''
        proxy_dict = get_proxies()
            
        proxy_ip = proxy_dict['ip']
        
        proxy_port = proxy_dict['port']
        
        proxy_url = "http://{}:{}".format(proxy_ip, proxy_port)
        
        self.proxies = {
                    'http': proxy_url,
                    'https': proxy_url,
                    }
        
        
        return self.proxies
        
        
    
    """
    向网页发起请求，并反回网页源代码
        
    url : 要访问的链接
            
    return: 网页源代码
    """
    def get_html(self, url):
        
        if self.proxy == False:
            r = requests.get(url, headers = self.headers, verify = False)
            r.raise_for_status()
#如果发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应)，我们可以通过 Response.raise_for_status() 来抛出异常
            r.encoding = r.apparent_encoding
            print (str(sys._getframe().f_lineno)+"TEST:"+r.text)
            return r.text
        else:
            for i in range(4):
#连续拉取代理3次，代理不能用报错
                try:
                    r = requests.get(url, headers = self.headers, verify = False)
                    r.raise_for_status()
#如果发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应)，我们可以通过 Response.raise_for_status() 来抛出异常
                except requests.exceptions.ProxyError:
                    if i == 3:
                        raise  
#连续拉取代理3次，代理不能用报错
                    print('Proxy falsed, please try again')
                    self.get_proxy()
#return 'ProxyError'
                else:
                    r.encoding = r.apparent_encoding
                    return r.text

    def get_info(self, url, **regexs):
        info = {}
        html = self.get_html(url)
        for key, regex in regexs.items():
            info[key] = re.findall(regex, html)
        return info

if __name__ == '__main__':  
    
    
    url = 'https://www.x23us.com/class/1_101.html'
      

    book_name_url_regex = '\[简介\]</a><a href="(.*?)" target="_blank">(.*?)</a></td>'

    author_regex = '</a></td>\s+?<td class="C">(.*?)</td>'

    x = Spider(False)
    print("TEST:"+str(sys._getframe().f_lineno))
    
    info = x.get_info(
        url,
        book_name_url = book_name_url_regex,
        author = author_regex,
        )
    
#    print(info)

    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
