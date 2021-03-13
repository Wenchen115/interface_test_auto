# -*- coding: utf-8 -*-
# @file: urls.py  
# @time: 2021/3/1 15:15
# @author: 岩滨
from django.urls import path
from app_task import views


urlpatterns = [
    # 用例管理
    path('',views.list_task),
    path('add/',views.task_add),

    path('edit/<int:tid>/',views.task_edit),
    # 获取用例的树形节点（结构）
    path('case_node/', views.case_node),
    path('save_task/', views.task_save),

    ]