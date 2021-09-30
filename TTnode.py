#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
请修改定时运行时间。
cron: 50 9 * * * TTnode.py
new Env('收取甜糖星愿');

# qinglong  如无法识别定时任务，自行修改时间
https://github.com/aibeso/ttnode.git

Env环境设置 参数
export authorization = '*****'  # 抓包获取甜糖客户端cookie的authorization参数

Env环境设置 通知服务
export BARK=''                   # bark服务,苹果商店自行搜索;
export SCKEY=''                  # Server酱的SCKEY;
export TG_BOT_TOKEN=''           # tg机器人的TG_BOT_TOKEN;
export TG_USER_ID=''             # tg机器人的TG_USER_ID;
export TG_API_HOST=''            # tg 代理api
export TG_PROXY_IP=''            # tg机器人的TG_PROXY_IP;
export TG_PROXY_PORT=''          # tg机器人的TG_PROXY_PORT;
export DD_BOT_TOKEN=''           # 钉钉机器人的DD_BOT_TOKEN;
export DD_BOT_SECRET=''          # 钉钉机器人的DD_BOT_SECRET;
export QQ_SKEY=''                # qq机器人的QQ_SKEY;
export QQ_MODE=''                # qq机器人的QQ_MODE;
export QYWX_AM=''                # 企业微信；http://note.youdao.com/s/HMiudGkb
export PUSH_PLUS_TOKEN=''        # 微信推送Plus+ ；
'''
import json
import os
import random
import time
import datetime as dt
import requests
messages=[]
log = 0
class TTnode:
    authorizations = []
    index = 0
    authorization = ''
    promote_score = 0
    devices_score = 0
    sign_score = 0
    billing_bandwidth = 0
    devices_msg = []

    # 初始化读取系统配置参数
    def __init__(self):
        if "TT_AUTHORIZATION" in os.environ and os.environ["TT_AUTHORIZATION"]:
            auth = os.environ["TT_AUTHORIZATION"]
            self.authorizations = auth.split('&')
        else:
            print("未检查到TT_AUTHORIZATION参数，请在青龙配置文件中填写：\\n export TT_AUTHORIZATION='你的甜糖客户端抓取的authorization参数，多个账号使用&分隔： 账号1&账号2&账号3，抓包过滤域名【tiantang.mogencloud.com】，或执行 python AutoTTnodeClient.py获取")
            exit()

    # 获取用户信息 ,  使用inactivedPromoteScore参数去收取推广收益
    def get_authorization(self):
        url = "http://tiantang.mogencloud.com/web/api/account/message/loading"
        header = {"Content-Type": "application/json", "authorization": self.authorization}
        res = requests.post(url, headers=header)
        if res and res.status_code == 200:
            text = json.loads(res.text)
            if log:
                print(text)
            if text['errCode'] != 0:
                print("账号：" + str(self.index) + " 已经失效,请重新抓取authorization！")
                self.send("账号：" + str(self.index) + " 已经失效,请重新抓取authorization！\n")
                return False
            else:
                # print("获取推广信息成功")
                return text['data']
        else:
            print("网络连接失败，位置：getAuthorization()，错误码：" + res.status_code)
            return {"inactivedPromoteScore": 0}

    # 获取设备列表
    def get_devices(self):
        url = "http://tiantang.mogencloud.com/api/v1/devices?page=1&type=2&per_page=200"
        header = {"Content-Type": "application/json", "authorization": self.authorization}
        res = requests.get(url, headers=header)
        if res and res.status_code == 200:
            text = json.loads(res.text)
            if log:
                print(text)
            if text['errCode'] != 0:
                print("API错误，错误码: " + res.status_code)
                exit()
            data = text['data']['data']
            if len(data) == 0:
                print("该账号尚未绑定设备，请绑定设备后再运行！")
                self.send("该账号尚未绑定设备，请绑定设备后再运行！\n")
                return []
            print("获取设备列表成功，设备总数：" + str(len(data)))
            return data
        else:
            print("网络连接失败，位置：getDevices()，错误码：" + res.status_code)
            return []

    # 签到
    def sign_in(self):
        url = "http://tiantang.mogencloud.com/web/api/account/sign_in"
        header = {"Content-Type": "application/json", "authorization": self.authorization}
        res = requests.post(url, headers=header)
        if res and (res.status_code == 200 or res.status_code == 201):
            data = json.loads(res.text)
            if log:
                print(data)
            if data['errCode'] != 0:
                print("[签到奖励]: 0-🌟 (失败:" + data['msg'] + ")")
                return 0
            else:
                print("[签到奖励]: " + str(data['data']) + "-🌟")
                return data['data']
        else:
            print("网络连接失败，位置：sign_in()，错误码：" + res.status_code)
            return 0

    # 收集推广星星 data['inactivedPromoteScore']
    def promote_score_logs(self, score):
        if score == 0:
            print("[推广奖励]: 0-🌟")
            return 0
        url = "http://tiantang.mogencloud.com/api/v1/promote/score_logs"
        header = {"Content-Type": "application/json", "authorization": self.authorization}
        body_json = {'score': score}
        encoded_body = json.dumps(body_json).encode('utf-8')
        res = requests.post(url, data=encoded_body, headers=header)
        if res and (res.status_code == 200 or res.status_code == 201):
            data = json.loads(res.text)
            if log:
                print(data)
            if data['errCode'] != 0:
                print("[推广奖励]: 0-🌟(收取异常)")
                return 0
            else:
                print("[推广奖励]: " + str(score) + "-🌟", score)
                # data = data['data']
                return score
        else:
            print("网络连接失败，位置：promote_score()，错误码：" + str(res.status_code))

    # 收取设备星星
    def devices_score_logs(self, devices):
        for device in devices:
            self.billing_bandwidth += device['last_day_billing_bandwidth']
            device_id = device['hardware_id']
            score = device['inactived_score']
            name = device['alias']
            if score == 0:
                print("[" + name + "]: 0-🌟")
                self.devices_msg.append("[" + name + "]: 0-🌟")
                continue
            url = "http://tiantang.mogencloud.com/api/v1/score_logs"
            header = {"Content-Type": "application/json", "authorization": self.authorization}
            body_json = {'device_id': device_id, 'score': score}
            encoded_body = json.dumps(body_json).encode('utf-8')
            res = requests.post(url, data=encoded_body, headers=header)
            if res and (res.status_code == 200 or res.status_code == 201):
                data = json.loads(res.text)
                if log:
                    print(data)

                if data['errCode'] != 0:
                    print("[" + name + "]: 0-🌟(收取异常)")
                    self.devices_msg.append("[" + name + "]: 0-🌟(收取异常)")
                else:
                    data = data['data']
                    self.devices_score += score
                    print("[" + name + "]: " + str(score) + "-🌟")
                    self.devices_msg.append("[" + name + "]: " + str(score) + "-🌟")
            else:
                print("网络连接失败，位置：devices_score_logs()，错误码：" + str(res.status_code))

            time.sleep(random.randint(2, 4))
    # 统计
    def total(self):
        msg = ''
        info = self.get_authorization()
        msg = msg + "*****第" + str(self.index) + "个账号*****\n"
        msg = msg + "[账户昵称]" + info['nickName'] + "\n"
        msg = msg + "[账户星愿]" + str(info['score']) + "-🌟\n"
        bandwidth = round(self.billing_bandwidth/1024, 2)
        msg = msg + "[结算带宽]" + str(bandwidth) + "Mbps\n"
        count = self.sign_score + self.promote_score + self.devices_score
        msg = msg + "[日总收益]" + str(count) + "-🌟\n"
        msg = msg + "|---[签到奖励]： " + str(self.sign_score) + "-🌟\n"
        msg = msg + "|---[推广奖励]： " + str(self.promote_score) + "-🌟\n"
        msg = msg + "|---[设备收益]： " + str(self.devices_score) + "-🌟\n"
        msg = msg + "[设备详细]：\n"
        for d in self.devices_msg:
            msg = msg + "|---" + d + "\n"
        messages.append(msg)

    def com_message(self):
        msg = "[当前时间]" + dt.datetime.now().strftime('%F %T') + "\n\n"
        for m in messages:
            msg = msg + m
            msg = msg + "\n"
        self.send(msg)

    # 发送通知
    def send(self, message):
        try:
            from sendNotify import Send
            message = message + "注意:统计仅供参考，多次运行无数据，一切请以甜糖客户端APP为准。\n原作者【邀请码：123463】！\nBy aibeso改造【邀请码：240390】！"
            msg = Send()
            msg.send("[甜糖星愿]", message)
        except:
            print("发送通知失败！请检查目录下是否存在文件:\n sendNotify.py \n __init__.py")
        print("注意:统计仅供参考，多次运行无数据，一切请以甜糖客户端APP为准。\n|---原作者【邀请码：123463】！\n|---By aibeso改造用于青龙平台并增加多账号功能【邀请码：240390】！\n")

    #  重置参数
    def re(self):
        self.authorization = ''
        self.promote_score = 0
        self.devices_score = 0
        self.sign_score = 0
        self.billing_bandwidth = 0
        self.devices_msg = []

    # 开始
    def start(self):
        print("**********开始**********")
        print("本次运行账号总数： " + str(len(self.authorizations)))
        for i, author in enumerate(self.authorizations):
            self.re()
            self.authorization = author
            self.index = i + 1
            print("***********************开始运行第： " + str(self.index) + "个***********************")
            info = self.get_authorization()
            if info:
                time.sleep(1)
                self.promote_score = self.promote_score_logs(info['inactivedPromoteScore'])
                time.sleep(1)
                self.sign_score = self.sign_in()
                time.sleep(1)
                devices = self.get_devices()
                time.sleep(1)
                self.devices_score_logs(devices)
                self.total()
                time.sleep(random.randint(1, 3))
        self.com_message()

if __name__ == '__main__':
    sleep_time = random.randint(1, 30)
    print("错峰延时执行" + str(sleep_time) + "秒，请耐心等待")
    # time.sleep(sleep_time)
    tt = TTnode()
    tt.start()
