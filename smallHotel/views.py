from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .system import *
import json
from smallHotel.test_case import *

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

def checkIn(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        id = request.POST.get('id')
        num = request.POST.get('phone_num')
        print(name,id,num)
        Hotel.get_instance().reception.register_customer_info(id,name,num,0)
        return redirect("http://127.0.0.1:8000/smallHotel/rec/spare")
    return render(request,"smallHotel/checkIn.html")

def getSpare(request):
    if request.method == 'POST':
        num = request.POST.get('room_num')
        print(num)
        return redirect("http://127.0.0.1:8000/smallHotel/rec/success")
    data=Hotel.get_instance().reception.check_room_state(0)
    dat={"nums":6,
          "num1":"号房间空闲",
          "num2":2
          }
    return render(request,"smallHotel/spareRoom.html",data)

def checkSuccess(request):
    data={"tips":"syb"}
    return render(request,"smallHotel/success.html",data)

def checkOut(request):
    return render(request,"smallHotel/checkOut.html")

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

def getTargetTemp(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
    temp = Hotel.get_instance().rooms[int(roomid)].target_temp
    response = {
        "targetTemp": temp
    }
    return JsonResponse(response)

def getRoomTemp(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
        print(request.POST)

    temp = Hotel.get_instance().rooms[int(roomid)].temp
    response = {
        "roomTemp": temp
    }
    return JsonResponse(response)

def testCase(request):
    return HttpResponse(test())