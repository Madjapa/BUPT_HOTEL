from django.shortcuts import render,HttpResponse

# Create your views here.
#主页
def admin(request):
    return render(request,"homepage.html")

#登录成功页面
def login(request):
    return render(request,"login.html")

def user_list(request):
    return HttpResponse("酒店空调管理系统")

