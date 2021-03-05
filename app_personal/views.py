from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect  # 重定向302
from django.contrib.auth.decorators import login_required


# Create your views here.

def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return render(request, "login.html", {
                "error": "用户名或密码为空"
            })
        # authenticate传递账户和凭据(与数据库互联)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user) # 记录用户的登陆状态
            return HttpResponseRedirect("/manage/") # 重定向到manage页面
        else:
            return render(request, "login.html", {
                "error": "用户名或密码错误"
            })


@login_required
def logout(request):
    """
    退出
    :param request:
    :return:
    """
    auth.logout(request) # 退出清除当前登陆账号的session
    return HttpResponseRedirect("/")