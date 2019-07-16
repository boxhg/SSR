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
import os

SSRShare_TXT = "ssr/ssrshare.com"
SSRShare_CC_TXT = "ssrshare.com.md"
IP_DICT_TXT = 'IPDict.txt'

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

def save_dict_to_file(dic):

    try:
        ipstr = str(dic)
        f = open(IP_DICT_TXT,'w',encoding='utf-8')  
        f.write(ipstr)
        f.close()
    except expression as e:
        print(e)
    

def load_dict_from_file():
    if(os.path.exists(IP_DICT_TXT)):
        f = open(IP_DICT_TXT,'r')
        data=f.read()
        f.close()
        return eval(data)
    else:
        return {}


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

    ipdict = load_dict_from_file()

    decode_str = base64_decode(html[0])
    try:
        country=[]
        country_ss={}
        lines=decode_str.split('\n')

        for line in lines:   

            IP = parse(line)
            if(IP == None):
                continue
            
            if(IP in ipdict):
                location = ipdict[IP]
            else:                
                location = QueryIPJson(IP)
                ipdict[IP] = location

            if(location != None):
                country_code = location['country']
                country.append(country_code)

                if(country_code in country_ss):
                    country_lines = country_ss[country_code] 
                    country_lines.append(line)
                else:
                    country_lines=[line]
                    country_ss[country_code] = country_lines
            
        if(len(ipdict)>0):
            save_dict_to_file(ipdict)

        country_set = set(country) 
        
        sscctxt = open(SSRShare_CC_TXT,'w')
        for item in country_set:
            msg = "- {0}: {1} \n".format(item,country.count(item))
            print(msg+"\n")
            sscctxt.write(msg)

            ssr_url = "https://raw.githubusercontent.com/boxhg/SSR/master/ssr/"+item+".txt"
            ssr_url_msg = "`"+ssr_url+"`\r\n"       
            sscctxt.write(ssr_url_msg)                         

            update_ssrlines_country(item,country_ss[item])
        sscctxt.close()

    except Exception as e:
        print('Error:',e)

def update_readme():
    
    readme1_md = open("readme1.md","r")
    readme1_txt = readme1_md.readlines()
    readme1_md.close()

    ssrshare_md = open(SSRShare_CC_TXT,"r")
    ssrshare1_txt = ssrshare_md.readlines()
    ssrshare_md.close()

    readme_md = open("README.md",'w')
    readme_md.writelines(readme1_txt)
    readme_md.writelines(ssrshare1_txt)

    readme_md.write("\r\n\r\n")
    readme_md.write("IP location data from `http://www.ip-api.com/`")

    #readme_md.write("# ss和ssr链接解析\r\n")
    #readme_md.write("https://raw.githubusercontent.com/boxhg/SSR/master/ssr/readme0.md")
    
    readme_md.close()
    
if __name__ == '__main__': 
    #update_ssr()
    paser_github()
    update_readme()