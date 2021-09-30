#!/usr/bin/python3
#coding=utf-8
import urllib3
import json
import datetime as dt
import time
import sys
import random
def getCode(phone):#获取验证码！
    url="http://tiantang.mogencloud.com/web/api/login/code"
    body_json="phone="+phone
    encoded_body=body_json.encode('utf-8')
    http = urllib3.PoolManager()
    header={"Content-Type":"application/x-www-form-urlencoded"}
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("getCode方法请求失败，结束程序")

       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        print("请输入正确的手机号码！")
        exit()
    data=data['data']
    return

def getAuthorization(phone,authCode):#获取Authorization
    url="http://tiantang.mogencloud.com/web/api/login"
    body_json="phone="+phone+"&authCode="+authCode
    encoded_body=body_json.encode('utf-8')
    header={"Content-Type":"application/x-www-form-urlencoded"}
    http = urllib3.PoolManager()
    response= http.request('POST', url,body=encoded_body,headers=header)
    if response.status!=201 and response.status!=200:
       print("getAuthorization方法请求失败，结束程序")
       exit()
    data=response.data.decode('utf-8')
    data=json.loads(data)

    if data['errCode']!=0:
        print("验证码错误!等待1分钟后重新运行再次获取验证码！\n")
        exit()
    data=data['data']

    return data['token']
def promotes(code):
    url="http://tiantang.mogencloud.com/api/v1/promotes?promote_code=" + code
    header={"Content-Type":"application/json","authorization":authorization}
    http = urllib3.PoolManager()
    response= http.request('POST', url,headers=header)
    data=response.data.decode('utf-8')
#********************************main******************************************
path=sys.path[0]
print("免责声明：\n本程序唯一下载地址：https://www.right.com.cn/forum/thread-4048219-1-1.html 如果你在别的地方下载的，出现问题与作者无关！\n本程序开源，开源自己查阅源码是否有后门。一切个人信息只用于甜糖程序api，请放心使用！，同时禁止转载本相关程序文件！\n禁止使用本程序用于一切商业活动，本程序只供个人学习研究使用。如有侵权请联系作者删除相关内容！\n")
stats=input("接受此免责声明：输入1为接受，输入任意字符为不接受,结束程序\n")
stats=int(stats)
if stats!=1:
    print("谢谢，请24小时删除本程序，程序已结束")
    exit()
    
authorization=""
week=0

phonenum=input("请输入手机号码回车键提交:\n")
phonenum=str(phonenum)
if len(phonenum)!=11:
    print("请输入正确的手机号码!!请重新运行")
    exit()
getCode(phonenum)
print("验证码发送成功请耐心等待！\n")
authCode=input("请确保你输入验证码短信是甜糖发的验证码短信，以免造成经济损失，概不负责。\n请输入验证码：\n")
authCode=str(authCode)
if len(authCode)!=6:
    print("请输入正确的验证码!!请重新运行")
    exit()
authorization=getAuthorization(phonenum,authCode)
print("\n你的authorization：\n"+authorization+"\n\n")
print("复制一下内容到青龙配置文件并保存")
print("export TT_AUTHORIZATION='"+ authorization +"'")
stats=1
stats=input("\n\n是否愿意填写作者的邀请码123463以支持作者？\n[1]支持原作者\n[2]改造用于青龙作者\n[0]不支持作者\n[任意字符]随机支持作者\n")
stats=str(stats)
if stats=='0':
    print("作者：发际线都高了2cm，你居然不支持我，讨厌你！讨厌你！哼！")
    exit()
if stats == '1':
    promotes('123463')
if stats == '2':
    promotes('240390')
promotes(random.choice(["123463", "240390", "240390","123463","123463", "240390", "240390","123463","123463", "240390","123463", "240390","123463", "240390","123463", "240390","123463", "240390","123463", "240390"]))
print("作者：谢谢大老板，祝大老板天天跑满上传，日进斗金，迎娶白富美。")
exit()