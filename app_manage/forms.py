# -*- coding: utf-8 -*-
# @file: forms.py  
# @time: 2021/1/30 11:14
# @author: 岩滨
from django import forms
from django.forms import widgets
from app_manage.models import Project,Module
# forms.Form 和forms.ModelForm 等价
class ProjectForm(forms.Form):
    """
    新增项目
    """
    name = forms.CharField(label="名称", max_length=100,widget=widgets.TextInput(attrs={"class":"form-control"}))
    describe = forms.CharField(label="描述",
                               widget=widgets.Textarea(attrs={"class":"form-control"}))
    status = forms.BooleanField(label="状态",required=False,widget=widgets.CheckboxInput())


class ProjectEditForm(forms.ModelForm):
    """
    编辑项目
    """

    class Meta:
        model = Project
        fields = ['name','describe','status']



class ModuleForm(forms.ModelForm):
    """
    新增模块
    """
    class Meta:
        model = Module
        fields = ['project','name','describe']


class ModuleEditForm(forms.ModelForm):
    """
    编辑模块
    """
    class Meta:
        model = Module
        fields = ['project','name','describe']