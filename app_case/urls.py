# -*- coding: utf-8 -*-
# @file: urls.py  
# @time: 2021/2/2 14:04
# @author: 岩滨
from django.urls import path
from app_case import views


urlpatterns = [
    # 用例管理
    path('',views.list_case),
    path('send_req/',views.send_req),
    path('assert_result/',views.assert_result),
    path('get_select_data/', views.get_select_data),
    path('save_case/',views.save_case),
    path('add_case/',views.add_case),
    path('edit_case/<int:cid>/', views.edit_case),
    path('delete_case/', views.delete_case),
    path('get_case_info/', views.get_case_info),



    ]