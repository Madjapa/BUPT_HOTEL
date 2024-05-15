from django.db import models

# Create your models here.
# 在MySQL中创建对应的一个表
class CustomerInfo(models.Model):
    # 创建字段
    objects = models.Manager()
    name = models.CharField(max_length=32)
    number = models.IntegerField()
