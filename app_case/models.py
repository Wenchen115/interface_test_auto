from django.db import models
from app_manage.models import Module
# Create your models here.

class TestCase(models.Model):
    """
    用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称",max_length=100,null=False,default="")
    url = models.TextField("URL",null=False)
    method = models.IntegerField("请求方法",null=False) # 1:get 2:post 3:delete 4:put
    header = models.TextField("请求头",null=False)
    per_type = models.IntegerField("参数类型",null=False) # 1:form-data  2:json
    per_value = models.TextField("参数内容", null=False)
    result = models.TextField("结果", null=False)
    assert_text = models.TextField("断言结果", null=False)
    assert_type = models.IntegerField("断言类型", null=False) # 1:包含  2：匹配
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        # 给项目表加特征字段
        return self.name