from django.urls import path

from . import views

'''
path(route, view, kwargs=None, name=None)
route   : 匹配smallHotel后面跟的后缀
view    : 你的视图function
kwargs  : https://docs.djangoproject.com/zh-hans/4.2/topics/http/urls/#views-extra-options 传递额外选项给视图函数
name    ：https://docs.djangoproject.com/zh-hans/4.2/topics/http/urls/#naming-url-patterns  命名 URL 模式 重定向需要用，因此name不要重复
'''

'''
请为每个视图函数添加一个或多个匹配规则以适应需求,不需要/作为前缀
'''
urlpatterns = [
    path("home/", views.admin, name="homepage"),
    path("rec/",views.reception,name="recept"),
    path("cus/",views.customer,name="customer"),
    path("man/",views.manager,name="manager"),
    path("mon/",views.monitor,name="monitor")
]