from web import models
from web.forms.bootstrap import BootStrapForm
from django import forms
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc':forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_name(self):
        # 项目校验
        name = self.cleaned_data['name']
        # 当前用户是否已创建过此项目
        exists = models.Project.objects.filter(name=name,creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目名已存在')

        # 判断当前用户是否还有额度创建新项目
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count>=self.request.tracer.price_policy.project_num:
            raise ValidationError('项目个数超出限制')

        return name