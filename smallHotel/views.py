from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .system import *
import json

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


def powerOn(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        roomtemp = data.get('roomtemp')
        Hotel.get_instance().rooms[room__id].power_on(temp)
        return JsonResponse({'status': 'success'})

def powerOff(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        Hotel.get_instance().rooms[room__id].power_off()
        return JsonResponse({'status': 'success'})

def tempSubmit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        temp = data.get('temp')
        Hotel.get_instance().rooms[roomid].temp = temp
        return JsonResponse({'code': '1'})

def flowSubmit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        windspeed = data.get('windspeed')
        Hotel.get_instance().rooms[roomid].speed = windspeed
        return JsonResponse({'status': 'success'})

def getBill(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        #
        return JsonResponse({'status': 'success'})

def getTemp(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        temp = Hotel.get_instance().rooms[roomid].temp
        return JsonResponse({
            "code": 1,
        "roomtemp": temp
        })

# 空调控制面板通信
# 1.房间空调处于服务队列时，计算并向后端更新房间温度
# 2.房间空调处于服务队列时，计算并向后端更新累计费用