import random
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
        customer_id = Hotel.get_instance().reception.customers[-1].id
        print(customer_id)
        Hotel.get_instance().reception.create_accommodation_order(customer_id,num)
        return redirect("http://127.0.0.1:8000/smallHotel/rec/success")
    data=Hotel.get_instance().reception.check_room_state(0)
    for i in range(1,6):
        if data[i] == False:
            data[i] = "号房间空闲"
        else:
            data[i] = "号房间不空闲"
    state = {
        "room1":data[1],
        "room2":data[2],
        "room3":data[3],
        "room4":data[4],
        "room5":data[5],
    }
    return render(request,"smallHotel/spareRoom.html",state)

def checkSuccess(request):
    num = random.Random().randint(1000,1999)
    data={"tips":num}
    return render(request,"smallHotel/success.html",data)

def checkOut(request):
    return render(request,"smallHotel/checkOut.html")

#顾客页面
def customer(request,roomid):
    return render(request, "smallHotel/customer.html",{"roomid":roomid})

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
        Hotel.get_instance().rooms[roomid].power_on(roomtemp)
        return JsonResponse({'code': 1})

def powerOff(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        Hotel.get_instance().rooms[roomid].power_off()
        return JsonResponse({'code': 1})

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

def getExp(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1':
            response = {'expenses' : '10'}
        elif roomid == '2':
            response = {'expenses' : '20'}
        else:
            response = {'expenses' : '30'}

        return JsonResponse(response)

def getTimer(request):
    if request.method == 'POST':
        Hotel.get_instance().scheduler.check_wait_queue()
        Hotel.get_instance().time_forward()
    return render(request,"smallHotel/timer.html")

def testCase(request):
    return HttpResponse(test())