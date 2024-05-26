from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from time import sleep
from .system import *
import json


def getExp(request):
    if request.method == 'GET':
        #data = json.loads(request.body.decode('utf-8'))
        response = {'code' : 1,'expenses' : '30'}
        return JsonResponse(response)
def getroomtemp(request):
    if request.method == 'GET':
    #data = json.loads(request.body.decode('utf-8'))
        response = {'code' : 1,'roomtemp': '27'}
        return JsonResponse(response)
def test(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        response = {'code': 1}
        return JsonResponse(response)
def boot(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sleep(3)
        response = {'code': 1}
        return JsonResponse(response)
def test(request):
    return render(request,"smallHotel/test.html")
# 空调控制面板通信
# 1.房间空调处于服务队列时，计算并向后端更新房间温度
# 2.房间空调处于服务队列时，计算并向后端更新累计费用