# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 00:03:18 2019

@author: Administrator
"""
import base64
from PingIP import get_ping_result
from LocateIP import LocateIP

def parse(ssr):
   try:
        server = None
        if ssr.startswith('ss://'):
           base64_encode_str = ssr[5:]
           server = parse_ss(base64_encode_str)
    
        if ssr.startswith('ssr://'):
           base64_encode_str = ssr[6:]
           server = parse_ssr(base64_encode_str)

        return server
   except:
       print("parse fail")
       return None
        


def parse_ss(base64_encode_str):
   decode_str = base64_decode(base64_encode_str)
   parts = decode_str.split(':')
   if len(parts) != 3:
       print('can''t pass SS-Link: %s' % base64_encode_str)
       return
   method = parts[0]
   password_and_ip = parts[1]
   port = parts[2]

   pass_and_server = password_and_ip.split('@')
   password = pass_and_server[0]
   server = pass_and_server[1]

   print('Crypt: %s, password: %s, server: %s, port: %s' % (method, password, server, port))
   return server

def parse_ssr(base64_encode_str):
   decode_str = base64_decode(base64_encode_str)
   print("decode_str:",decode_str)
   parts = decode_str.split(':')
   if len(parts) != 6:
       print('can''t pass SSR-Link: %s' % base64_encode_str)
       return

   server = parts[0]
   port = parts[1]
   protocol = parts[2]
   method = parts[3]
   obfs = parts[4]
   password_and_params = parts[5]
   print("password_and_params:",password_and_params)
   password_and_params = password_and_params.split("/?")

   password_encode_str = password_and_params[0]
   password = base64_decode(password_encode_str)
   print("password:",password)

   print('server: %s, port: %s, proto: %s, crypt: %s, password: %s, obfs: %s'
       % (server, port, protocol, method, password, obfs))
   return server

def update_ssr_group(ssr,groupname):
   if ssr.startswith('ssr://'):
      base64_encode_str = ssr[6:]
   else:
      return

   decode_str = base64_decode(base64_encode_str)
   parts = decode_str.split('/?')
   if len(parts) != 2:
       print('can''t pass SSR-Link: %s' % base64_encode_str)
       return

   sparam =parts[1]
   # new_group = base64.urlsafe_b64encode(groupname.encode('utf-8')).decode("utf-8")
   new_group = base64_encode(groupname)
   new_sparam = sparam.replace("V1dXLlNTUlRPT0wuQ09N", new_group)
   
   server = parts[0] + '/?'+new_sparam
   # new_server = 'ssr://'+ base64.urlsafe_b64encode(server.encode('utf-8')).decode("utf-8")
   new_server = 'ssr://'+ base64_encode(server)

   return new_server   

def fill_padding(base64_encode_str):

   need_padding = len(base64_encode_str) % 4 != 0

   if need_padding:
       missing_padding = 4 - need_padding
       base64_encode_str += '=' * missing_padding
   return base64_encode_str


def base64_decode(base64_encode_str):
   base64_encode_str = fill_padding(base64_encode_str)
   return base64.urlsafe_b64decode(base64_encode_str).decode('utf-8')

def base64_encode(encode_str):
   base64_encode_str = base64.urlsafe_b64encode(encode_str.encode('utf-8')).decode("utf-8")
   b_str= base64_encode_str.strip(r'=+')

   return b_str


if __name__ == '__main__':
   # ssr = input("Input SS or SSR:")

   text = "SSR_Germany"
   print(base64_encode(text))

   print(base64.encodestring(text.encode('utf-8')).decode('utf-8'))
   print(base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8'))  
   print(base64.standard_b64encode(text.encode('utf-8')).decode('utf-8'))
   print(base64.b64encode(text.encode('utf-8')).decode('utf-8'))

   ssr = "ssr://MTQyLjkzLjEwMy45MzozNDc2NjphdXRoX3NoYTFfdjQ6YWVzLTI1Ni1jZmI6cGxhaW46ZEdWc1pXZHlZVzFBWm5KbFpUTTBOdy8_cmVtYXJrcz1VMU5TVkU5UFRGX2x2cmZsbTcwdFNHVnpjMlU2TkRjJmdyb3VwPVYxZFhMbE5UVWxSUFQwd3VRMDlO"
   update_ssr_group = update_ssr_group(ssr,'SSR_China')

   print(update_ssr_group)


   IP = parse(update_ssr_group)
   get_ping_result(IP)
   LocateIP(IP)

