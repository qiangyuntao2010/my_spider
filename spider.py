#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Written by QYT, please contact me by qiangyutao2010@gmail.com
Copyright 2019 QYT

'''

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

        Invoke get_proxy() method.
        Detail please see proxy_api.py
        
        return:  {'http': 'http://223.240.211.23:28500', 
                  'https': 'http://223.240.211.23:28500'}
        
        Give the paras to proxy


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
        
        '''

        invoke request to web page and return the source code

        ''' 
    
    def get_html(self, url):
        
        if self.proxy == False:
            r = requests.get(url, headers = self.headers, verify = False)
            if r.status_code==200:
                pass
            else:
                return None
            #r.raise_for_status()

#If you send an error request and get the 4XX or 5XX error respone, we can use respone.raise_for_status to throw the exception 
            
            r.encoding = r.apparent_encoding

            return r.text
        else:
            for i in range(4):

# Pull the proxy three times and no error is allowed
                
                try:
                    r = requests.get(url, headers = self.headers, verify = False, timeout=30)
                    r.raise_for_status()
                except requests.exceptions.ProxyError:
                        pass
                        print('Proxy falsed, please try again')
                        self.get_proxy()
                        return 'ProxyError'
                else:
                    r.encoding = r.apparent_encoding
                    print("Open the websit successfully!")
                    return r.text

    def get_info(self, url, title):

        html = self.get_html(url)

        if html==None:
            return None

        pattern=re.compile(title)
        m=pattern.findall(html)
        if m:
            return url
        else:
            return None 

if __name__ == '__main__':  
    
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 
    x = Spider(False)
    url_base = 'https://www.8btc.com/article/'
    title_test=r'<title data-vue-meta="true">(.*?)Libra(.*?)</title>'
    for count in range(460781,465000):
        url=url_base+str(count)
        result=x.get_info(url,title_test)
        if result is None:
            pass
        else:
            print result

    

    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
