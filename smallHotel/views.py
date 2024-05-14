from django.shortcuts import render,HttpResponse
from django.core.files import File
from .new import *
# Create your views here.
#主页


def admin(request):
    return render(request,"homepage.html")

#接待员页面
def reception(request):
    customers = []
    rooms = []
    room_num = 5  # 房间总数
    with open('smallHotel/customers.txt', 'r', encoding='utf-8') as f:
        file = File(f)
        # 逐行读取文件内容
        for line in file.readlines():
            data = line.strip().split()
            customers.append(Customer(data[0], data[1]))
    with open('smallHotel/room.txt', 'r', encoding='utf-8') as f:
        file = File(f)
        # 逐行读取文件内容
        for line in file.readlines():
            data = line.strip().split()
            rooms.append(Room(data[0], 0, 0, 0, data[1]))

    # 办理入住,查询空闲房间

    if len(customers) < room_num:
        for i in range(len(rooms)):
            if int(rooms[i].done) == 0:
                print(rooms[i].id)
                return HttpResponse(rooms[i].id)
    # 显示空闲的房间号,传递给前端
    else:
        print("你完了")

    # 从前端获取顾客输入的信息
    name = "syb"
    room_num = "02"
    if request.method == 'GET':
        return render(request,"reception.html",{"tips": "sssss"})
    if request.method == 'POST':
        name = request.POST.get('username')
        num = request.POST.get('room_num')
        print(name,num)
    return render(request,"reception.html")

#顾客页面
def customer(request):
    return render(request, "customer.html")



