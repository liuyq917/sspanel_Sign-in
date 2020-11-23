#Time : 2020/9/17 9:52
#Auth : Ne-21
#Des : sspanel自动每日签到脚本
#File :sspanel_qd.py
#IDE :PyCharm
#Motto:Another me.
#sspanel自动每日签到脚本，基于项目https://github.com/zhjc1124/ssr_autocheckin修改

import requests
import re

requests.packages.urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self):
        # 机场地址
        self.base_url = input()
        print(self.base_url)
        # 登录信息
        self.email = input()
        print(self.email)
        self.password = input()
        print(self.password)
        # Server酱推送（可空）
        self.sckey = ''
        # 酷推qq推送（可空）
        self.ktkey = ''

    def checkin(self):
       # msgall = ''
      #  for i in range(len(self.base_url)):

            email = self.email.split('@')
            email = email[0] + '%40' + email[1]
            password = self.password

            session = requests.session()

            session.get(self.base_url, verify=False)

            login_url = self.base_url + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = 'email=' + email + '&passwd=' + password + '&code='
            post_data = post_data.encode()
            response = session.post(login_url, post_data, headers=headers, verify=False)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': self.base_url + '/user'
            }

            response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
            msg = (response.json()).get('msg')
            
            #msgall = msgall + self.base_url + '\n\n' + msg + '\n\n'
            print(msg)
            

            info_url = self.base_url + '/user'
            response = session.get(info_url, verify=False)
            """
            以下只适配了editXY主题

            try:
                level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
                day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
                rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
                msg = "- 今日签到信息："+str(msg)+"\n- 用户等级："+str(level)+"\n- 到期时间："+str(day)+"\n- 剩余流量："+str(rest)
                print(msg)
             except:
                print(msg)
            """
            return msg
        #return msgall
        
    # Server酱推送
    def server_send(self, msg):
        if self.sckey == '':
            return
        server_url = "https://sc.ftqq.com/" + str(self.sckey) + ".send"
        data = {
                'text': "签到完成，点击查看详细信息~",
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

# 云函数入口
def main_handler(event, context):
    run = SspanelQd()
    run.main()

if __name__ == '__main__':
    run = SspanelQd()
    run.main()



