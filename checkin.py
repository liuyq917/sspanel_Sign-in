import requests
import re

requests.packages.urllib3.disable_warnings()


class SspanelQd(object):
    def __init__(self):
        # 机场地址
        str = input()
        self.base_url = str.split(',')
        # 登录信息
        str = input()
        self.email = str.split(',')
        str = input()
        self.password = str.split(',')
        # Server酱推送（可空）
        self.sckey = input()
        # 酷推qq推送（可空）
        self.ktkey = input()

    def checkin(self):
        msgall = ''
        for i in range(len(self.base_url)):

            email = self.email[i].split('@')
            email = email[0] + '%40' + email[1]
            password = self.password[i]

            session = requests.session()

            session.get(self.base_url[i], verify=False)

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
