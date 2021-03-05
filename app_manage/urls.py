# -*- coding: utf-8 -*-
# @file: urls.py  
# @time: 2021/1/29 16:29
# @author: 岩滨
from django.urls import path
from app_manage.views import project_view, module_view


urlpatterns = [
    # 项目管理
    path('',project_view.list_project),
    path('project_list/',project_view.list_project),
    path('project_add/',project_view.add_project),
    path('project_edit/<int:pid>/',project_view.edit_project),
    path('project_delete/<int:pid>/',project_view.delete_project),


    # 模块管理
    path('module_list/',module_view.list_module),
    path('module_add/',module_view.add_module),
    path('module_edit/<int:mid>/',module_view.edit_module),
    path('module_delete/<int:mid>/',module_view.delete_module),

]
