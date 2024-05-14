#顾客类
class Customer:
    def __init__(self, name, num, id):
        self.name = name
        self.num = num #房间号
        self.id = id

    def use(self):
        return

#前台
class Reception:
    def __init__(self,name):
        self.name = name
        self.customers = []
        self.rooms = [Room(), Room(), Room(), Room(), Room()]

    #办理入住
    def check_in(self):
        return
    def get_bill(self):
        return

    def register_customer_info(self, customer_id, customer_name, number, date):
        self.customers.append(Customer(customer_name, number, customer_id))
        return True  # return isOK

    def check_room_state(self, date):
        return [[i.id, i.state] for i in self.rooms]

    def create_accommodation_order(self, customer_id, room__id):
        pass
    def deposite(self, amount):
        pass
    def create_door_card(self, room_id, date):
        pass

    def process_checkout(self, room_id):
        pass
    def query_fee_records(self, room_id, date_out):
        pass
    def calculate_accommodation_fee(self, days_of_accommodation, fee_of_day):
        pass
    def calculate_AC_fee(self, list_of_detail_records):
        pass
    def create_accommodation_bill(self, room_id, date):
        pass
    def create_AC_bill(self, room_id, date):
        pass
    def create_detailed_records_AC(self, room_id, date_in, date_out):
        pass
    def process_payment(self, room_id, date_out, total_fee_of_accommodation, total_fee_of_AC):
        pass
    def set_room_state(self, room_id):
        for i in self.rooms:
            if i.id == room_id:
                i.state = False

#管理员
class Manager:
    def __init__(self,name):
        self.name = name
    def run(self):
        return
    def monitor(self):
        return

#账单
class Bill:
    def __init__(self,name,value):
        self.name = name
        self.value =value

#详单
class DetailRecord:
    def __init__(self,name,value):
        self.name = name
        self.value = value

#客房
class Room:
    def __init__(self, id, speed, time, temp, state, schedule):
        self.id = id
        self.speed = speed #风速
        self.time = time
        self.temp = temp #温度
        self.state = state
        self.schedule = schedule

    def power_on(self, room_id, current_room_temp, schedule):
        self.request.request(room_id)
        pass

    # def request_number(self, service_number):
    #     pass
    def change_temp(self, room_id, target_temp):
        for i in self.schedule.wait_queue:
            if i.room_id == id:
                pass
        pass
    def change_speed(self, room_id, speed):
        pass
    def power_off(self, room_id):
        pass
    def request_state(self, room_id):
        pass

class Schedule:
    def __init__(self, room_id, current_room_temp):
        # self.room_id = room_id
        self.target_temp
        self.current_room_temp = current_room_temp
        self.wait_queue = []
        self.serve_queue = []

    def request(self, room_id):
        if len(self.serve_queue) < 3:
            serve_item = ServeItem(room_id)
            self.serve_queue.append(serve_item)
        else:
            wait_item = WaitItem(room_id)
            self.wait_queue.append(wait_item)
        pass

class ServeItem:
    def __init__(self, room_id):
        self.room_id = room_id
        pass

class WaitItem:
    def __init__(self, room_id):
        self.room_id = room_id
        pass
