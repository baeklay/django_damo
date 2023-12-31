import datetime
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import redirect
from django.conf import settings


class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 如果用户已登录，则request中赋值
        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 白名单: 没有登录都可以访问的URL
        '''
        1.获取当前用户访问的URL
        2.检查URL是否在白名单中，如果在则可以继续向后访问，如果不在则进行判断是否已登录
        '''
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        if not request.tracer.user:
            return redirect('login')

        # 登录成功后，访问后台管理时，获取当前用户所拥有的额度
        # 获取当前用户最近的交易记录
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        request.tracer.price_policy = _object.price_policy

    def process_view(self, request, view, args, kwargs):

        # 判断URL是否是以manage开头，如果是则判断项目ID是否是我创建 or 参与
        if not request.path_info.startswith('/manage/'):
            return

        project_id = kwargs.get('project_id')
        # 是否是我创建的
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            # 是我创建的项目的话，我就让他通过
            request.tracer.project = project_object
            return

        # 是否是我参与的项目
        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            # 是我参与的项目
            request.tracer.project = project_user_object.project
            return

        return redirect('project_list')
