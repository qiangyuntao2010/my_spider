#!/usr/bin/env python
# coding=utf-8

import requests

res=requests.post(url=url, headers=headers, data=data, allow_redirects=False)

print (res.headers)
