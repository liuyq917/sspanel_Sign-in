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
        self.base_url = [input()]
        # 登录信息
        self.email = ['vx1999@163.com','vx1999@163.com','liuyq917@gmail.com','liuyq917@gmail.com','liuyq917@gmail.com']
        self.password = ['Xxkjb2005','QAZwsx123789','amy070712','amy070712','amy070712']
        # Server酱推送（可空）
        self.sckey = ''
        # 酷推qq推送（可空）
        self.ktkey = ''

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



#我爱破解签到（cookies版）
cookie= 'Hm_lvt_46d556462595ed05e05f009cdafff31a=1578708851; htVD_2132_saltkey=R9JzvMYH; htVD_2132_lastvisit=1578705254; htVD_2132_ulastactivity=1578708892%7C0; htVD_2132_auth=3f67GtHpIkfYL%2BEjVY0nRcx5ZrnpARnNE12ecjvKurhmyoYuBF%2FNkVYMfbaenxPZWfPaPxvMKTVnmW9kSuqoEFHEXtc; htVD_2132_lip=115.171.83.85%2C1578708892; htVD_2132_connect_is_bind=0; htVD_2132_seccode=1347768.0d02af85bff8ce59e3; htVD_2132_nofavfid=1; htVD_2132_ttask=853307%7C20200111; htVD_2132_lastact=1578709369%09home.php%09spacecp; htVD_2132_lastcheckfeed=853307%7C1578709369; htVD_2132_checkfollow=1; htVD_2132_checkpm=1; Hm_lpvt_46d556462595ed05e05f009cdafff31a=1578709373'
cookies={}#初始化cookies字典变量  
for line in cookie.split(';'):   #按照字符：进行划分读取  
    #其设置为1就会把字符串拆分成2份  
    name,value=line.strip().split('=',1)  
    cookies[name]=value  #为字典cookies添加内容  
s = requests.Session()
r = s.get("https://www.52pojie.cn/home.php?mod=task&do=apply&id=2",cookies=cookies)
r = s.get("https://www.52pojie.cn/home.php?mod=task&do=draw&id=2",cookies=cookies)
