#-*-coding:utf-8-*-

#===============================================================================
# ����smtplib��MIMEText
#===============================================================================
from email.mime.text import MIMEText
import smtplib

#===============================================================================
# Ҫ����˭�����﷢��2����
#===============================================================================
mailto_list=["842310899@qq.com"]
subject="���gg"
content="��ʲô��gg"
#===============================================================================
# ���÷��������û����������Լ�����ĺ�׺
#===============================================================================
mail_host="smtp.sina.com"
mail_user="iherb12368"
mail_pass="li1315521"
mail_postfix="sina.com"

#===============================================================================
# �����ʼ�
#===============================================================================
def send_mail(to_list,sub,content):
    '''''
    to_list:����˭
    sub:����
    content:����
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':

        if send_mail(mailto_list,subject,content):
            print "���ͳɹ�"
        else:
            print "����ʧ��"



