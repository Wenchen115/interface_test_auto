from django.db import models

# Create your models here.

class Project(models.Model):
    """
    项目表
    """
    name = models.CharField("名称",max_length=100,null=False,default="")
    describe = models.TextField("描述",default="")
    status = models.BooleanField("状态",default=True)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        # 给项目表加特征字段
        return self.name


class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # 制定与项目表对应的外键，on_delete如果删掉所属于项目，这个模块是否要删除；CASCADE关联删除
    name = models.CharField("名称",max_length=100,null=False,default="")
    describe = models.TextField("描述",default="")
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.name