from django.contrib.auth.models import User
from django import forms
from .models import Submit
from .models import Identity
from captcha.fields import CaptchaField

class UserForm(forms.Form): #user table
    '''
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']
    '''
    username=forms.CharField(widget=forms.TextInput(attrs={'id':'username','placeholder':u'用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'密码'}))
    password_test=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'密码确认'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':u'邮件输入'}))
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class SubmitForm(forms.ModelForm):# submit table
    submit_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Submit
        fields = ('homework_number', 'submit_content',)


class IdentityForm(forms.ModelForm):#identity table
    class Meta:
        model = Identity
        fields = ('identity',)


class loginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'id':'username','placeholder':u'用户名'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'id':'password','placeholder':u'密码'}))