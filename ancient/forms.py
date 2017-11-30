from django.contrib.auth.models import User
from django import forms
from .models import Submit
from .models import Identity


class UserForm(forms.ModelForm): #user table
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']


class SubmitForm(forms.ModelForm):# submit table
    submit_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Submit
        fields = ('homework_number', 'submit_content',)


class IdentityForm(forms.ModelForm):#identity table
    class Meta:
        model = Identity
        fields = ('identity',)
