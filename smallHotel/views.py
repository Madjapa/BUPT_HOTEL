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
    return render(request,"smallHotel/monitor.html")


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
        roomtemp = data.get('roomtemp')
    print(request.body)
    print("roomid " + str(roomid) + " temp " + str(roomtemp) )
    response = {'code': 1}
    return JsonResponse(response)