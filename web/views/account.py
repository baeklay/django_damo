from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    # 校验手机号:不能为空和格式是否正确
    if form.is_valid():
        return JsonResponse({'status':True})

    return JsonResponse({'status':False,'error':form.errors})
