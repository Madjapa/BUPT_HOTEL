from django.shortcuts import render,HttpResponse

from .system import *


# Create your views here.
#主页
def admin(request):
    return render(request,"smallHotel/homepage.html")

#接待员页面
def reception(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        num = request.POST.get('room_num')
        print(name,num)
    return render(request,"smallHotel/reception.html")

#顾客页面
def customer(request):
    return render(request, "smallHotel/customer.html")

#酒店管理员
def manager(request):
    return render(request,"smallHotel/manager.html")

def monitor(request):
    return render(request,"smallHotel/monitor")

import json
from django.http import JsonResponse


def test(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        temp = data.get('temp')
    print(request.body)
    print("roomid " + str(roomid) + " temp " + str(temp) )
    response = {'message': 'POST已处理'}
    return JsonResponse(response)
def boot(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        roomtemp = data.get('roomtemp')
    print(request.body)
    print("roomid " + str(roomid) + " temp " + str(roomtemp) )
    response = {'message': 'POST已处理'}
    return JsonResponse(response)
# 空调控制面板通信
# 1.房间空调处于服务队列时，计算并向后端更新房间温度
# 2.房间空调处于服务队列时，计算并向后端更新累计费用