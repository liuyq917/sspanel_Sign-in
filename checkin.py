import requests
import re
import os

requests.packages.urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self):
        # 机场地址
        weblist = os.environ['web']
        self.base_url = weblist.split(',')
        # 登录信息
        userlist = os.environ['user']
        self.email = userlist.split(',')
        passlist = os.environ['pwd']
        self.password = passlist.split(',')
        # Server酱推送（可空）
        self.sckey = os.environ['sckey']
        # 酷推qq推送（可空）
        self.ktkey = os.environ['ktkey']
        #push
        self.push= os.environ['push']

    def checkin(self):
        msgall = ''
        for i in range(len(self.base_url)):

            email = self.email[i].split('@')
            email = email[0] + '%40' + email[1]
            password = self.password[i]

            session = requests.session()

            try:
                #以下except都是用来捕获当requests请求出现异常时，
                # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                session.get(self.base_url[i], verify=False)  

            except requests.exceptions.ConnectionError:
                msg = self.base_url[i] + '\n\n' + '网络不通'
                msgall = msgall + self.base_url[i] + '\n\n' + msg + '\n\n'
                print(msg)
                continue
            except requests.exceptions.ChunkedEncodingError:
                msg = self.base_url[i] + '\n\n' + '分块编码错误'
                msgall = msgall + self.base_url[i] + '\n\n' + msg + '\n\n'
                print(msg)
                continue   
            except:
                msg = self.base_url[i] + '\n\n' + '未知错误'
                msgall = msgall + self.base_url[i] + '\n\n' + msg + '\n\n'
                print(msg)
                continue

            login_url = self.base_url[i] + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = 'email=' + email + '&passwd=' + password + '&code='
            post_data = post_data.encode()
            response = session.post(login_url, post_data, headers=headers, verify=False)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': self.base_url[i] + '/user'
            }

            response = session.post(self.base_url[i] + '/user/checkin', headers=headers, verify=False)
            msg = (response.json()).get('msg')
            
            msgall = msgall + self.base_url[i] + '\n\n' + msg + '\n\n'
            print(msg)

            info_url = self.base_url[i] + '/user'
            response = session.get(info_url, verify=False)

        return msgall
        
    # Server酱推送
    def server_send(self, msg):
        if self.sckey == '':
            return
        server_url = "https://sctapi.ftqq.com/" + str(self.sckey) + ".send"
        data = {
                'text': "机场签到完成，点击查看详细信息~",
                'desp': msg
            }
        requests.post(server_url, data=data)

    # 酷推QQ推送
    def kt_send(self, msg):
        if self.ktkey == '':
            return
        kt_url = 'https://push.xuthus.cc/send/'+str(self.ktkey)
        data = ('签到完成，点击查看详细信息~\n'+str(msg)).encode("utf-8")
        requests.post(kt_url, data=data)

    def main(self):
        msg = self.checkin()
        self.server_send(msg)
        self.kt_send(msg)
        
     #PUSHPLSH推送
    def push_send(self, msg):
         if not PUSH:
              # print("pushplus推送的PUSHPLUS未设置!!\n取消推送")
              return
         push_plus_url = "http://www.pushplus.plus/send"
         params = {
              "token": PUSH,
              "title": self,
              "content": msg,
              "template": "markdown"
         }
    res = requests.post(url=push_plus_url, params=params)
    if res.status_code == 200:
        print("pushplus推送成功!")
    else:
        print("pushplus推送失败!")


            
            
            
            
            
# 云函数入口
def main_handler(event, context):
    run = SspanelQd()
    run.main()

if __name__ == '__main__':
    run = SspanelQd()
    run.main()
