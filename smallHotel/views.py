from django.shortcuts import render,HttpResponse,redirect
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
    if request.method == 'GET':
        spare_room = ""
        if len(customers) < room_num:
            for i in range(len(rooms)):
                if int(rooms[i].done) == 0:
                    spare_room += rooms[i].id+"   "
                    print(spare_room)
            return render(request, "reception.html", {"tips": spare_room})
        # 显示空闲的房间号,传递给前端
        else:
            return render(request, "reception.html", {"tips": "无空闲的房间"})
    if request.method == 'POST':
        name = request.POST.get('username')
        num = request.POST.get('room_num')
        for i in range(len(rooms)):
            if num == rooms[i].id:
                rooms[i].done = 1
        customers.append(Customer(name,num))
        with open("smallHotel/customers.txt", "a") as f:
            myfile = File(f)
            myfile.write(name + " " + num + "\n")
        #return render(request,"reception.html",{"tips": "成功入住"})
        return redirect("/customer")

#顾客页面
def customer(request):
    on = request.POST.get('current_temp_button')
    add = request.POST.get('add')
    sub = request.POST.get('sub')
    print(on)
    print(sub)
    print(add)
    return render(request, "customer.html")



