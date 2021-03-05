# -*- coding: utf-8 -*-
# @file: module_view.py
# @time: 2021/2/1 15:40
# @author: 岩滨
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from app_manage.models import Module
from app_manage.forms import ModuleForm,ModuleEditForm



@login_required
def list_module(request):
    """
       模块管理
       :param request:
       :return:
    """
    module_list = Module.objects.all()

    return render(request, "module/list.html", {"modules": module_list})

@login_required
def add_module(request):
    """
    新增模块
    :param request:
    :return:
    """
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(name=name,describe=describe,project=project)
        return HttpResponseRedirect('/manage/module_list/')

    else:
        form = ModuleForm()

    return render(request, "module/add.html", {"form":form})


def edit_module(request,mid):
    """
    编辑模块
    :param request:
    :param mid:
    :return:
    """
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            module = Module.objects.get(id=mid)
            module.project = project
            module.name = name
            module.describe = describe

            module.save()

        return HttpResponseRedirect('/manage/module_list/')
    else:
        if mid:
            module = Module.objects.get(id = mid)
            form = ModuleEditForm(instance = module)
        else:
            form = ModuleForm()
        return render(request, "module/edit.html", {"form":form, "id":mid})


@login_required
def delete_module(request,mid):
    """
    删除
    :param request:
    :param pid:
    :return:
    """
    if mid:
        module = Module.objects.get(id = mid)
        module.delete()
        return HttpResponseRedirect('/manage/module_list/')
