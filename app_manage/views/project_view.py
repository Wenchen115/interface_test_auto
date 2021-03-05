from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from app_manage.models import Project
from app_manage.forms import ProjectForm,ProjectEditForm

# Create your views here.

@login_required  # @login_required装饰器，用来判断用户是否登陆，若用户已登录则可以访问此页面，若用户未登录，则跳转默认页面(‘/accounts/login’)。
def list_project(request):
    """
    接口管理
    :param request:
    :return:
    """
    project_list = Project.objects.all()

    return render(request, "project/list.html", {"projects":project_list})


@login_required
def add_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name,describe=describe,status=status)
        return HttpResponseRedirect('/manage/')

    else:
        form = ProjectForm()

    return render(request, "project/add.html", {"form":form})


@login_required
def edit_project(request,pid):
    """
    编辑项目
    :param request:
    :return:
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            project = Project.objects.get(id=pid)
            project.name = name
            project.describe = describe
            project.status = status
            project.save()

        return HttpResponseRedirect('/manage/')
    else:
        if pid:
            project = Project.objects.get(id = pid)
            form = ProjectEditForm(instance = project)
        else:
            form = ProjectForm()
        return render(request, "project/edit.html", {"form":form, "id":pid})


@login_required
def delete_project(request,pid):
    """
    删除
    :param request:
    :param pid:
    :return:
    """
    if pid:
        project = Project.objects.get(id = pid)
        project.delete()
        return HttpResponseRedirect('/manage/')
