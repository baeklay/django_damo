from django.urls import re_path
from django.conf.urls import include
from web.views import account, home, project, manage

urlpatterns = [
    re_path(r'^register/$', account.register, name="register"),
    re_path(r'^send/sms/$', account.send_sms, name="send_sms"),
    re_path(r'^login/sms/$', account.login_sms, name='login_sms'),
    re_path(r'^login/$', account.login, name='login'),
    re_path(r'^image/code/$', account.image_code, name='image_code'),
    re_path(r'^logout/$', account.logout, name='logout'),
    re_path(r'^index/$', home.index, name='index'),
    # 项目列表
    re_path(r'^project/list/$', project.project_list, name='project_list'),
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar,
            name='project_unstar'),

    re_path(r'^manage/(?P<project_id>\d+)/', include([
        re_path(r'^dashboard/$', manage.dashboard, name='dashboard'),
        re_path(r'^issues/$', manage.issues, name='issues'),
        re_path(r'^statistics/$', manage.statistics, name='statistics'),
        re_path(r'^file/$', manage.file, name='file'),
        re_path(r'^wiki/$', manage.wiki, name='wiki'),
        re_path(r'^setting/$', manage.setting, name='setting'),
    ], None)),
]
