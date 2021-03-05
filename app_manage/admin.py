from django.contrib import admin
from app_manage.models import Project
from app_manage.models import Module


# Register your models here.
# admin后台注册项目管理
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'describe','status','update_time',"create_time")


admin.site.register(Project, ProjectAdmin)


# admin后台注册模块管理
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'describe','update_time',"create_time","project")


admin.site.register(Module, ModuleAdmin)