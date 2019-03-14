# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:10:02 2019

@author: Administrator
"""
import sys
from SSR_parse2 import parse,update_ssr_group
from PingIP import get_ping_result
from LocateIP import QueryIPJson
import requests
import base64

SSRShare_TXT = "ssr/ssrshare.com"
SSRShare_CC_TXT = "ssr/ssrshare.com.txt"

#log
class Logger(object):
    def __init__(self,fileN ="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN,"w")
    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        pass
sys.stdout = Logger("data/result.txt") 
#下面所有的方法，只要控制台输出，都将写入"result.txt"


def paser_data():
    country=[]
    for line in open("data/SSR.txt","r"): #设置文件对象并读取每一行文件
        temp=line.split('\t')
        ss = "\r\nNo. "+temp[0]+":"
        print(ss)
        ssr = temp[1][:-1]
        print(ssr)
        
        IP = parse(ssr)
        # get_ping_result(IP)
        # location = LocateIP(IP)

        location = QueryIPJson(IP)
        if(location != None):
            country.append(location['country'])

    #print(country)

    country_set = set(country) 
    for item in country_set: 
        print("%s have %d :" %(item,country.count(item)))

def fill_padding(base64_encode_str):

   need_padding = len(base64_encode_str) % 4 != 0

   if need_padding:
       missing_padding = 4 - need_padding
       base64_encode_str += '=' * missing_padding
   return base64_encode_str

def base64_decode(base64_encode_str):
   base64_encode_str = fill_padding(base64_encode_str)
   return base64.urlsafe_b64decode(base64_encode_str).decode('utf-8')

def update_ssr():
    ssrurl = 'https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com'
    response = requests.get(ssrurl)
    response.encoding = 'utf8'
    html = response.text

    ssrshare = open(SSRShare_TXT,"w")
    ssrshare.write(html)
    ssrshare.close()

def update_ssrlines_country(country,lines):

    new_lines = []
    for line in lines: 
        print(line+"\r\n")
        ssr = update_ssr_group(line,'SSR_'+country)
        new_lines.append(ssr)
        print(ssr+"\r\n")

    new_lines_str = '\n'.join(new_lines)
    new_lines_str = base64.urlsafe_b64encode(new_lines_str.encode('utf-8')).decode("utf-8")
    
    SS_Country_TXT = "ssr/"+country +".txt"
    ssr_cc = open(SS_Country_TXT,'w')
    ssr_cc.write(new_lines_str)
    ssr_cc.close()

def paser_github():

    ssrshare = open(SSRShare_TXT,"r")
    html = ssrshare.readlines()
    ssrshare.close()

    decode_str = base64_decode(html[0])
    try:
        country=[]
        country_ss={}
        lines=decode_str.split('\n')

        for line in lines: 
            
            IP = parse(line)

            location = QueryIPJson(IP)
            if(location != None):
                country_code = location['country']
                country.append(country_code)

                if(country_code in country_ss):
                    country_lines = country_ss[country_code] 
                    country_lines.append(line)
                else:
                    country_lines=[line]
                    country_ss[country_code] = country_lines
            

        country_set = set(country) 
        
        sscctxt = open(SSRShare_CC_TXT,'w')
        for item in country_set:
            msg = "{0}: {1} \n".format(item,country.count(item))
            print(msg+"\n")
            sscctxt.write(msg)

            update_ssrlines_country(item,country_ss[item])
        sscctxt.close()

    except Exception as e:
        print('Error:',e)

if __name__ == '__main__': 
    # update_ssr()
    paser_github()