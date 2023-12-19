"""
用户账户相关功能：注册、短信、登录、注销
"""
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm


def register(request):
    # 注册
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    # 发送短信
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号：不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    # 短信登录
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})

    form = LoginSMSForm(request.POST)
    if form.is_valid():
        mobile_phone = form.cleaned_data['mobile_phone']

        user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()

        request.session['user_id'] = user_object.id
        request.session['user_name'] = user_object.uername

        return JsonResponse({'status': True, 'data': "/index/"})

    return JsonResponse({'status': False, 'error': form.errors})
