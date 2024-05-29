from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from time import sleep
from .system import *
import json


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
def getroomtemp(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1':
            response = {'roomTemp' : '10'}
        elif roomid == '2':
            response = {'roomTemp' : '20'}
        else:
            response = {'roomTemp' : '30'}
        return JsonResponse(response)
def targetTemp(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1':
            response = {'targetTemp': '1'}
        elif roomid == '2':
            response = {'targetTemp': '2'}
        else:
            response = {'targetTemp': '27'}
        return JsonResponse(response)
def roomTemp(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1':
            response = {'roomTemp': '1'}
        elif roomid == '2':
            response = {'roomTemp': '2'}
        else:
            response = {'roomTemp': '27'}
        return JsonResponse(response)
def test(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        response = {'code': 1}
        return JsonResponse(response)
def boot(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Hotel.get_instance().rooms[1].power_on(32)
        response = {'code': 1}
        return JsonResponse(response)
def shutdown(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Hotel.get_instance().rooms[1].power_off()
        response = {'code': 1}
        return JsonResponse(response)
def test(request):
    return render(request,"smallHotel/test.html")
def getSpeed(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1':
            response = {'windSpeed': 0}
        elif roomid == '2':
            response = {'windSpeed': 1}
        else:
            response = {'windSpeed': 2}
    return JsonResponse(response)
def getStatus(request):
    if request.method == 'GET':
        roomid = request.GET['roomid']
        if roomid == '1' or roomid == '3' or roomid == '5':
            response = {'status': 1}
        elif roomid == '2' or roomid == '4' or roomid == '6':
            response = {'status': 0}
    return JsonResponse(response)
# 空调控制面板通信
# 1.房间空调处于服务队列时，计算并向后端更新房间温度
# 2.房间空调处于服务队列时，计算并向后端更新累计费用