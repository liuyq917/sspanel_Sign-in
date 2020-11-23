# Sign-in
每日机场自动签到

根据 https://github.com/ne-21/sspanel-automaticcheckin 代码修改，不支持登陆需要人机验证的机场。

首先fork本项目到自己的仓库

进入自己fork的仓库，点击 Settings-> Secrets-> New Secrets 添加以下5个Secrets。

WEB     签到机场网址,多个网址用英文逗号分割。

USER    签到机场登陆邮箱,与网站对应,多个用户用英文逗号分割。

PWD     签到机场登陆密码,与网站对应,多个用户用英文逗号分割。

SCKEY   微信推送SCKEY码，详情参见http://sc.ftqq.com/

KTKEY   QQ推送Skey码，详情参见https://cp.xuthus.cc/
