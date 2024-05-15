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
    #path('admin/', admin.site.urls),
    path('admin/', views.admin),
    path('reception/',views.reception),
    path('cus/',views.customer),
    path('cus/poweron/',views.powerOn),
    path('cus/poweroff/',views.powerOff),
    path('cus/temperature/',views.tempSubmit),
    path('cus/flowsubmit/',views.flowSubmit),
    path('cus/getbill/',views.getBill),
    path('cus/gettemp/',views.getTemp),
    #path('user/list',views.user_list)
]