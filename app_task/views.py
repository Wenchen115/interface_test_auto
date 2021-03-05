from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_manage.models import Project,Module
from app_case.models import TestCase
from interface_test_auto.common import response
from app_task.models import TestTask
# Create your views here.

def list_task(request):
    """
    任务列表
    :param request:
    :return:
    """
    task = TestTask.objects.all()
    return render(request,'task/list.html',{"task":task})


def task_add(request):
    """
    任务创建
    :param request:
    :return:
    """
    return render(request,'task/add.html')


def case_node(request):
    """
    用例树形结构展示
    :param request:
    :return:
    """
    if request.method == "GET":
        data=[]
        project = Project.objects.all()
        for p in project:
            project_dict = {
                "name":p.name,
                "isParent":True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list=[]
            for m in module:
                module_dict = {
                    "name":m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list =[]
                for c in case:
                    case_dict = {
                        "id":c.id,
                        "name":c.name,
                        "isParent": False
                    }
                    case_list.append(case_dict)
                module_dict["children"]=case_list
                module_list.append(module_dict)
            project_dict["children"]=module_list
            data.append(project_dict)
        return JsonResponse({"code": 10200,
                             "message": "success",
                             "data": data})
    else:
        return JsonResponse({"code": 10100, "message": "请求方法错误"})


@csrf_exempt
def task_save(request):
    """
    保存任务
    :param request:
    :return:
    """
    if request.method == "POST":
        task_name = request.POST.get("name","")
        task_desc = request.POST.get("desc", "")
        task_cases = request.POST.get("cases", "")
        if task_name == "":
            return response(10102,"任务名称为空")

        TestTask.objects.create(name=task_name,describe=task_desc,cases=task_cases)
        return response()

    else:
        return response(10101,"请求方式错误")