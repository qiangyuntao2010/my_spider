#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from proxy_api import get_proxies

class Spider:
    
       
    def __init__(self, is_proxy = False):
        
        #If you want to use proxy
        if is_proxy == True:
            
            self.get_proxy()

        self.proxy = is_proxy   

        # This is my header and maybe you should use your browser header
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
            #r.raise_for_status()

#如果发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应)，我们可以通过 Response.raise_for_status() 来抛出异常
            r.encoding = r.apparent_encoding
            #print (str(sys._getframe().f_lineno)+"TEST:")
            return r.text
        else:
            for i in range(4):
#连续拉取代理3次，代理不能用报错
                try:
                    r = requests.get(url, headers = self.headers, verify = False, timeout=30)
                    r.raise_for_status()
                except requests.exceptions.ProxyError:
                        pass
                        print('Proxy falsed, please try again')
                        self.get_proxy()
#return 'ProxyError'
                else:
                    r.encoding = r.apparent_encoding
                    print("Open the websit successfully!")
                    return r.text

    def get_info(self, url, title):

        html = self.get_html(url)
        pattern=re.compile(title)
        title_i=str(title)

        if title_i in html:
            return url
        else:
            url=None
            

if __name__ == '__main__':  
    
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 
    x = Spider(False)
    url_base = 'https://www.8btc.com/article/45742'
    title_test='Libra'
    for count in range(500):
        url=url_base+str(count)
        print count
        result=x.get_info(url,title_test)
        if result is None:
            pass
        else:
            print result

    

    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
