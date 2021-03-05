# -*- coding: utf-8 -*-
# @file: common.py  
# @time: 2021/3/5 11:53
# @author: 岩滨
from django.http import JsonResponse

def response(status=None, message=None, data=[]):
    if status is None:
        status = 10200
    if message is None:
        message="成功"

    return JsonResponse({"status":status,"message":message,"data":data})
