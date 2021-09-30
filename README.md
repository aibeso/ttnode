甜糖自动收星愿  
说明：未申请原大佬许可，介意勿用。[原大佬](https://github.com/744287383/AutoTTnodeClient)  
内容：1基于青龙平台 2新增多账号功能  
qinglong 拉库命令：  
```
ql repo https://github.com/aibeso/ttnode.git "TT" "" "__init__|sendNotify|requirements" ""  
```
文件依赖(否则无法通知)  
* \_\_init__.py  
* sendNotify.py  

容器内安装依赖包(依赖可能不全,尝试运行后再安装缺失依赖，使用：pip3 install 依赖包名 )  
```
pip3 install -r requirements.txt
```
默认定时参数(自行修改定时参数, 可以避免请求量过大很导致运行失败)
```
50 9 * * *
```
环境设置 参数 
``` 
export TT_AUTHORIZATION='你的甜糖客户端抓取的authorization参数，多个账号使用&分隔： 账号1&账号2&账号3' # 抓包过滤域名【tiantang.mogencloud.com】，或运行AutoTTnodeClient.py获取
``` 
环境设置 通知服务  
``` 
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
```