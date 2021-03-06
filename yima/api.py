# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 14:53:41 2019

@author: Simon Zhou
"""
import time
import requests
from .error_codes import _codes

class YMClient:
    baseURL = "http://api.fxhyd.cn/UserInterface.aspx"
    def __init__(self, username, password, token=None, itemid=None, mobile=None):
        self.username = username
        self.password = password
        self.token = token
        if self.token == None:
            self.token = self.get_token()
            if self.token[0] != 'success':
                print(self.token)
            else:
                self.token = self.token[1]
        
        self.itemid = itemid
        self.mobile = mobile
                
    def get_token(self):
        params = {}
        params['action'] = 'login'
        params['username'] = self.username
        params['password'] = self.password
        response = requests.get(self.baseURL, params=params).text.split("|")
        if response[0] == 'success':
            return tuple(response)
        else:
            return '获取TOKEN错误'+response[0]+':'+_codes.get(int(response[0]))
    
    def get_account_info(self):
        params = {}
        params['action'] = 'getaccountinfo'
        params['token']=self.token
        response = requests.get(self.baseURL, params).text.split("|")
        if response[0] == 'success':
            info = {k:v for k,v in zip(["用户名","账户状态","账户等级","账户余额","冻结金额","账户折扣","获取号码最大数量"],response[1:])}
            return info
        else:
            return '获取账户信息错误'+response[0]+':'+_codes.get(int(response[0]))
    
    def get_mobile(self, itemid, isp=None, province=None, city=None, mobile=None, excludeno=None):
        params = {}
        params['action'] = 'getmobile'
        params['token'] = self.token
        params['itemid'] = itemid
        response = requests.get(self.baseURL, params=params).text.split("|")
        if response[0] == 'success':
            return int(response[1])
        else:
            return '错误'+response[0]+':'+_codes.get(int(response[0]))
        
    def get_sms(self, itemid, mobile, release=None, getsendno=None):
        params = {}
        params['action'] = 'getsms'
        params['token'] = self.token
        params['itemid'] = itemid
        params['mobile'] = mobile
        params['release'] = release
        response = requests.get(self.baseURL, params=params)
        response.encoding = 'utf-8'
        response = response.text.split("|", 1)
        if response[0] == 'success':
            return ('success', response[1])
        else:
            return (int(response[0]), _codes.get(int(response[0])))
        
    def fetch_sms_until_succeed(self, itemid, mobile, release=1, getsendno=None, timeout=90):
        stime = time.time()
        while time.time()-stime <= timeout:
            a = self.get_sms(itemid, mobile, release=release)
            if a[0] == 3001:
                print(a[1]+"，5秒后重试...")
                time.sleep(5)
            elif a[0] == 'success':
                print("获取短信成功，短信内容为：\n"+a[1])
                return a[1]
                break
            else:
                raise Exception(a[1])
        if a[0] != 'success':
            raise Exception("Timeout")
        
    def send_sms(self, itemid, mobile, sms, number=None):
        params = {}
        params['action'] = 'sendsms'
        params['token'] = self.token
        
    def get_send_sms_state(self, itemid, mobile):
        params = {}
        params['action'] = 'getsendsmsstate'
        params['token'] = self.token
        
    def release(self, itemid, mobile):
        params = {}
        params['action'] = 'release'
        params['token'] = self.token
        params['itemid'] = itemid
        params['mobile'] = mobile
        response = requests.get(self.baseURL, params).text
        if response == 'success':
            return response
        else:
            return '错误'+response+':'+_codes.get(int(response))

    def add_ignore(self, itemid, mobile):
        params = {}
        params['action'] = 'addignore'
        params['token'] = self.token
        params['itemid'] = itemid
        params['mobile'] = mobile
        response = requests.get(self.baseURL, params).text
        if response == 'success':
            return response
        else:
            return '错误'+response+':'+_codes.get(int(response))

if __name__ == '__main__': 
    pass
