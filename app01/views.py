from django.shortcuts import render

# Create your views here.

from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
    # 修改页面默认form
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


def register(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {'form': form})


from django_redis import get_redis_connection
from django.shortcuts import HttpResponse


def index(request):
    conn = get_redis_connection("default")
    conn.set('nickname', 'lay', ex=10)
    value = conn.get('nickname')
    print(value)

    return HttpResponse("ok")
