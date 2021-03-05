from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from app_manage.models import Project,Module
from app_case.models import TestCase
# Create your views here.


def list_case(request):
    """
    用例列表
    :param request:
    :return:
    """
    cases = TestCase.objects.all()
    p = Paginator(cases,10)

    page = request.GET.get("page","")
    if page=="":
        page = 1
    try:
        page_cases = p.page(page)
    except PageNotAnInteger:
        page_cases = p.page(1)
    except EmptyPage:
        page_cases = p.page(p.num_pages)

    return render(request,"case/list.html",{"case":page_cases})

def add_case(request):
    """
    添加用例
    :param request:
    :return:
    """
    return render(request,"case/debug.html")

def edit_case(request,cid):
    """
    编辑用例
    :param request:
    :return:
    """
    return render(request,"case/edit.html")

def send_req(request):
    """
    发送
    :param request:
       url: req_url,
        method: req_method,
        header: req_header_str,
        per_type: req_type,
        per_value: req_parameter_str,
    :return:
    """
    if request.method == "GET":
        url = request.GET.get("url")
        method = request.GET.get("method")
        header = request.GET.get("header")
        per_type = request.GET.get("per_type")
        per_value = request.GET.get("per_value")
        # 将header和per_value转换成json格式
        try:
            header = json.loads(header)
            print(type(header))
        except json.decoder.JSONDecodeError:
            return JsonResponse({"status": 10101, "message": "header格式错误,header格式应为标准的json格式"},
                                json_dumps_params={'ensure_ascii': False})
        try:
            per_value = json.loads(per_value)
            print(type(per_value))
        except json.decoder.JSONDecodeError:
            return JsonResponse({"status": 10101, "message": "参数格式应为标准的json格式"},
                                json_dumps_params={'ensure_ascii': False})

        # get和post请求，传参格式：form-date、json
        if method == "get":
            r = requests.get(url,params=per_value,headers=header)
        if method == "post":
            if per_type == "form":
                r = requests.post(url,data = per_value,headers=header)
            if per_type == "json":
                r = requests.post(url,json = per_value,headers=header)

        return JsonResponse({"status":10200,"message":"success","data":r.text},
                            json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def assert_result(request):
    """
    断言
    :param request:
    :return:
    """
    if request.method == "POST":
        result_text = request.POST.get("result_text")
        assert_text = request.POST.get("assert_text")
        assert_type = request.POST.get("assert_type")
        if result_text == "" or assert_text == "":
            return JsonResponse({"status":10101,"message":"断言参数与结果不能为空"},
                                json_dumps_params={'ensure_ascii': False})
        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"status":10200,"message":"断言成功，断言参数存在于返回结果中"},
                                    json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({"status":10102,"message":"断言失败，断言参数在返回结果中未找到"},
                                    json_dumps_params={'ensure_ascii': False})
        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"status":10200,"message":"断言成功，断言参数与返回结果相等"},
                                    json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({"status":10103,"message":"断言失败，断言参数与返回结果不相等"},
                                    json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"status":10104,"message":"失败，请重试！"},json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({"status":10105,"message":"请求方式错误"},json_dumps_params={'ensure_ascii': False})

def get_select_data(request):
    """
    获取select下拉框需要项目/模块数据
    :param request:
    :return:
    """
    if request.method == "GET":
        project = Project.objects.all()
        data_list = []
        for p in project:
            project_dict = dict(id=p.id,name=p.name)
            modules = Module.objects.filter(project_id=p)
            module_list = []
            for m in modules:
                modules_dict = dict(id=m.id,name=m.name)
                module_list.append(modules_dict)
            project_dict["moduleList"] = module_list
            data_list.append(project_dict)
        return JsonResponse({"code":10200,"message":"success","data":data_list})

@csrf_exempt
def save_case(request):
    """
    用例保存
    :param request:
    :return:
    """
    if request.method == "POST":
        case_id = request.POST.get("cid", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        header = request.POST.get("header", "")
        per_type = request.POST.get("per_type", "")
        per_value = request.POST.get("per_value", "")
        result_text = request.POST.get("result_text", "")
        variable = request.POST.get("variable", "")
        assert_text = request.POST.get("assert_text", "")
        assert_type = request.POST.get("assert_type", "")
        module_id = request.POST.get("module_id", "")
        case_name = request.POST.get("case_name", "")

        if method == "get":
            method_int = 1
        elif method == "post":
            method_int = 2
        else:
            return JsonResponse({"code":10101,"message":"请求方式错误"},json_dumps_params={'ensure_ascii': False})

        if per_type == "form":
            per_type_int = 1
        elif per_type == "json":
            per_type_int = 2
        else:
            return JsonResponse({"code":10101,"message":"参数格式错误"},json_dumps_params={'ensure_ascii': False})

        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code":10101,"message":"断言类型错误"},json_dumps_params={'ensure_ascii': False})

        if case_id == '':
            TestCase.objects.create(module_id=module_id,
                                    url=url,
                                    name=case_name,
                                    method=method_int,
                                    header=header,
                                    per_type=per_type_int,
                                    per_value=per_value,
                                    result=result_text,
                                    assert_text=assert_text,
                                    assert_type=assert_type_int,
                                    )
            return JsonResponse({"code":10200,"message":"保存成功"},json_dumps_params={'ensure_ascii': False})
        else:
            case = TestCase.objects.get(id=int(case_id))
            case.url = url
            case.module_id = module_id
            case.name = case_name
            case.method = method_int
            case.header = header
            case.parameter_type = per_type_int
            case.parameter_body = per_value
            case.result = result_text
            case.assert_text = assert_text
            case.assert_type = assert_type_int
            case.save()
            return JsonResponse({"code": 10200, "message": "save success"})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})

@csrf_exempt
def get_case_info(request):
    """获取接口数据"""
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module_id)
        case_info = model_to_dict(case)
        case_info["project"] = module.project_id
        return JsonResponse({"code": 10200,
                             "message": "success",
                             "data": case_info})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})


@csrf_exempt
def delete_case(request):
    """删除用例"""
    if request.method == "POST":
        cid = request.POST.get("cid", "")
        case = TestCase.objects.get(id=cid)
        case.delete()
        return JsonResponse({"code": 10200, "message": "删除成功"})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})



