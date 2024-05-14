from django.shortcuts import render,HttpResponse


#顾客类
class Customer:
    def __int__(self,name,num):
        self.name = name
        self.num = num #房间号

    def use(self):
        return

#前台
class Reception:
    def __int__(self,name):
        self.name = name
    #办理入住
    def check_in(self):
        return
    def get_bill(self):
        return

#管理员
class Manager:
    def __int__(self,name):
        self.name = name
    def run(self):
        return
    def monitor(self):
        return
    

#账单
class Bill:
    def __int__(self,name,value):
        self.name = name
        self.value =value

#详单
class DetailRecord:
    def __int__(self,name,value):
        self.name = name
        self.value = value

#客房
class Room:
    def __init__(self,id,speed,time,temp):
        self.id = id
        self.speed = speed #风速
        self.time = time
        self.temp = temp #温度

#等待队列
class WaitQueue:
    def __init__(self,queue):
        self.queue =queue

#服务队列
class SeverQueue:
    def __init__(self,queue):
        self.queue =queue

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
        temp = data.get('targetTemp')
    print(request.body)
    print("roomid" + roomid + " temp" + temp )
    response = {'message': 'POST已处理'}
    return JsonResponse(response)
        
# 空调控制面板通信
# 1.房间空调处于服务队列时，计算并向后端更新房间温度
# 2.房间空调处于服务队列时，计算并向后端更新累计费用