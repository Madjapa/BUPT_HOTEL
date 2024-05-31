from django.urls import path

from . import views,testAC

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
    path("test/",testAC.test,name="test"),
    path("home/", views.admin, name="homepage"),
    path("rec/",views.reception,name="recept"),
    path("rec/checkin",views.checkIn,name="recept2"),
    path("rec/checkout",views.checkOut,name="recept3"),
    path("rec/detail/<int:roomid>",views.getDetail),
    path("rec/spare",views.getSpare,name="recept4"),
    path("rec/success",views.checkSuccess,name="recept5"),
    path("mon/",views.monitor,name="monitor"),
    path("mon/getSpeed/",testAC.getSpeed,name="speeds"),
    path("mon/getStatus/",testAC.getStatus,name="status"),
    path("mon/targetTemp/", views.getTargetTemp, name='yyy'),
    path("mon/roomTemp/", views.getRoomTemp, name='yyyy'),
    path("cus/<int:roomid>", views.customer, name="customer"),
    path("cus/boot/",views.powerOn,name="boot"),
    path("cus/shutdown/",views.powerOff,name="syb"),
    path("cus/getExpenses/",views.getExp,name="xx"),
    path("cus/roomTemp/",views.getRoomTemp,name='yy'),
    path("cus/temperature/",views.tempSubmit,name='sgd'),
    path("cus/windSpeed/",views.flowSubmit,name='xjj'),
    path("timer",views.getTimer,name='yyyyy'),
    path("test_case/",views.testCase),
]