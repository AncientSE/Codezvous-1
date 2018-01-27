from random import Random
from django.core.mail import send_mail  #发送邮件模块
from ancient.models import EmailVerifyRecord
from mysite.settings import EMAIL_FROM

def random_str(randomlength=8):
    """生成随机字符串"""
    str = ''
    chars = 'AaBbCcDdEdFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)  # 16位长度的字符串
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save() #保存

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email]) # 发送邮件
        if send_status:
            pass