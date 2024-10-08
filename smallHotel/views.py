import random
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse,FileResponse
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
        customer_id = Hotel.get_instance().reception.customers[-1].id
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
    if request.method == 'POST':
        roomid = int(request.POST.get('room_id'))
        return redirect("http://127.0.0.1:8000/smallHotel/rec/detail/"+str(roomid))
    return render(request,"smallHotel/checkOut.html")

def getDetail(request, roomid):
    Hotel.get_instance().reception.process_checkout(roomid)
    AC_fee = Hotel.get_instance().reception.orders[roomid][-1].AC_bill.fee
    accommodation_fee = Hotel.get_instance().reception.orders[roomid][-1].accommodation_bill.fee
    data={
        "a":AC_fee,
        "b":accommodation_fee,
        "c":AC_fee + accommodation_fee,
    }
    return render(request,"smallHotel/detail.html",data)

def AC_bill(request):
    return FileResponse(open("smallHotel/static/smallHotel/AC_bill.csv", "rb"))

def accommodation_bill(request):
    return FileResponse(open("smallHotel/static/smallHotel/accommodation_bill.csv", "rb"))

def detailRecord(request):
    return FileResponse(open("smallHotel/static/smallHotel/detailRecord.csv", "rb"))

#顾客页面
def customer(request,roomid):
    return render(request, "smallHotel/customer.html",{"roomid":roomid})

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

def getExp(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
    exp = Hotel.get_instance().rooms[int(roomid)].AC_fee
    response = {
        "expenses": exp
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

def tempSubmit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        temp = data.get('temp')
        Hotel.get_instance().rooms[roomid].change_temp(roomid,temp)
        return JsonResponse({'code': '1'})

def flowSubmit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        roomid = data.get('roomid')
        speed = data.get('windspeed')
        Hotel.get_instance().rooms[roomid].change_speed(roomid,speed)
    response = {'code': 1}
    return JsonResponse(response)

#监控界面
def monitor(request):
    return render(request,"smallHotel/monitor.html")

def getSpeed(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
    speed = Hotel.get_instance().rooms[int(roomid)].speed
    response = {
        "windSpeed": speed
    }
    return JsonResponse(response)

def getStatus(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
    AC_running = Hotel.get_instance().rooms[int(roomid)].AC_running
    response = {
        "status": AC_running
    }
    return JsonResponse(response)

def getACStatus(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
    AC_status = Hotel.get_instance().rooms[int(roomid)].AC_status
    response = {
        "status": AC_status
    }
    return JsonResponse(response)

def getTargetTemp(request):
    if request.method == 'GET':
        roomid = request.GET.get('roomid',"")
    temp = Hotel.get_instance().rooms[int(roomid)].target_temp
    response = {
        "targetTemp": temp
    }
    return JsonResponse(response)

def getTimer(request):
    if request.method == 'POST':
        Hotel.get_instance().scheduler.check_wait_queue()
        Hotel.get_instance().time_forward()
    return render(request,"smallHotel/timer.html")

def testCase(request):
    return HttpResponse(test())

def initRoom(request):
    init_rooms()
    return HttpResponse()
