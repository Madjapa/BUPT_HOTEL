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
