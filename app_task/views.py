from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app_manage.models import Project,Module
from app_case.models import TestCase
from interface_test_auto.common import response
from app_task.models import TestTask
from app_task.models import TestResult
from app_task.extend.task_thread import TaskThread
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


def task_edit(request,tid):
    """
    编辑任务
    :param request:
    :return:
    """
    return render(request,"task/edit.html")


@csrf_exempt
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
        return response(10200, "success", data)
    elif request.method == "POST":
        task_id = request.POST.get("tid", "")
        task = TestTask.objects.get(id= task_id)
        case_list = task.cases[1:-1].split(",")
        case_list_int = []
        for c in case_list:
            case_list_int.append(int(c))

        task_data = {
            "taskName": task.name,
            "taskDesc": task.describe,
        }

        data = []
        project = Project.objects.all()

        for p in project:
            project_dict = {
                "name": p.name,
                "isParent": True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name": m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    print("", c.id, type(c.id))
                    if c.id in case_list_int:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": True
                        }
                    else:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": False
                        }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data.append(project_dict)

        task_data["data"] = data
        return response(10200, "success", task_data)

    else:
        return response(10100, "请求方法错误")


@csrf_exempt
def task_save(request):
    """
    保存任务
    :param request:
    :return:
    """
    if request.method == "POST":
        task_id = request.POST.get("tid","")
        task_name = request.POST.get("name","")
        task_desc = request.POST.get("desc", "")
        task_cases = request.POST.get("cases", "")
        if task_name == "":
            return response(10102,"任务名称为空")
        if task_id == "0":

            TestTask.objects.create(name=task_name,describe=task_desc,cases=task_cases)

        else:
            task = TestTask.objects.get(id=task_id)
            task.name = task_name
            task.describe = task_desc
            task.cases = task_cases
            task.save()

        return response()

    else:
        return response(10101,"请求方式错误")


def run_task(request,tid):
    """
    运行任务
    unittest + ddt + 线程
    :param request:
    :return:
    """
    task = TaskThread(tid)
    task.run()
    return HttpResponseRedirect("/task/")


def log_list(request, tid):
    """
    获取某一任务的历史结果
    """
    result = TestResult.objects.filter(task_id=tid)
    return render(request, "task/logs.html", {"result": result})


def get_log(request):
    """
    获取某一任务的历史结果
    """
    if request.method == "POST":
        rid = request.POST.get("rid", "")
        result = TestResult.objects.get(id=rid)
        return response(data=result.result)
    else:
        return response(10101, "请求方法错误")

