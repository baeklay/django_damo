"""
用户账户相关功能：注册、短信、登录、注销
"""
import datetime
import uuid
from io import BytesIO

from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from utils.image_code import check_code


def register(request):
    # 注册
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 用户表中新建一条数据（注册）
        instance = form.save()

        # 创建交易记录
        policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
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
        request.session.set_expiry(60 * 60 * 24 * 14)

        return JsonResponse({'status': True, 'data': "/index/"})

    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    # 用户名和密码登录
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')
