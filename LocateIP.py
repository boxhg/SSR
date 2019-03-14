# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:21:49 2019

@author: Administrator
"""
import requests
import re
from pyquery import PyQuery as pq
import json

def QueryIPJson(IP):
    try:
        if IP == None:
            return
        url = 'http://ip-api.com/json/'+str(IP)+'?lang=en'
        response = requests.get(url)
        response.encoding = 'utf8'
        html = response.text
        ipjson = json.loads(html)
        print("Location:",ipjson['country'])
        return ipjson
    except:
        print("Location IP Fail")
        
def LocateIP(IP):
    try:
        if IP == None:
            return
        #url = 'http://www.ip138.com/ips1388.asp?ip=' + str(IP) + '&action=2'
        url = 'http://www.882667.com/ip_'+str(IP)+".html"
        response = requests.get(url)
        response.encoding = 'gbk'
        html = response.text
        #print(html)
        doc = pq(html)
        temp = doc('body div div div:nth-child(4) .shenlansezi')
        #print(temp)
        location=re.findall(".*zi\">(.*?)<",str(temp))[0]
        print("Location:",location)
        return location
    except:
        print("Location IP Fail")

        
if __name__ == '__main__':
    IP = '144.34.158.30'
    #LocateIP(IP)
    QueryIPJson(IP)
