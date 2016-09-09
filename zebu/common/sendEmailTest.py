# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
# mail_host="SMTP.spreadtrum.com"  #设置服务器
# mail_user="zebu"    #用户名
# mail_pass="ZBzb@0804"   #口令
# sender = 'zebu@spreadtrum.com'

#spreadst 第三方 SMTP 服务
mail_host="mail.spreadst.com"  #设置服务器
mail_user="fanxh"    #用户名
mail_pass="fanxh123"    #口令
sender = 'fanxh@spreadst.com'

'''
receivers = ['ellen.yang@spreadtrum.com']
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
'''

def send_mail(sub,content,to_list):
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = sender
    msg['To'] = ";".join(to_list)
    try:
        #smtpObj = smtplib.SMTP()
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)    # SMTP 端口号
        #smtpObj.starttls()
        #smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, to_list, msg.as_string())
        return True
    except Exception,ex:
        print 'Exception', ':', ex
        return False