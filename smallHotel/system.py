from smallHotel.models import *

class Hotel:
    __instance = None
    manager = None
    reception = None
    scheduler = None
    rooms = None

    def __init__(self):
        if Hotel.__instance is None:
            Hotel.__instance = self
            Hotel.manager = Manager("syb")
            Hotel.reception = Reception("syb")
            Hotel.scheduler = Scheduler()
            Hotel.rooms = {}
            for i in RoomInfo.objects.all():
                Hotel.rooms[i.id] = Room(i.id, i.temp, i.fee_per_day)
        else:
            return

    @staticmethod
    def get_instance():
        if not Hotel.__instance:
            Hotel()
        return Hotel.__instance


# 顾客
class Customer:
    def __init__(self, id, name, num):
        self.id = id
        self.name = name
        self.num = num  # ?

    # def use(self):
    #     return


# 前台
class Reception:
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.orders = {}

    def register_customer_info(self, customer_id, customer_name, number, date):
        self.customers.append(Customer(customer_id, customer_name, number))
        return True  # return isOK

    def check_room_state(self, date):
        return {i.id: i.state for i in Hotel.get_instance().rooms.values()}

    def create_accommodation_order(self, customer_id, room_id):
        # TODO: 处理对已有订单即已入住的房间进行的创建订单操作
        self.orders[room_id] = Order(customer_id, room_id)
        room = Hotel.get_instance().rooms[room_id]
        room.state = True
        room.customer_id = customer_id

    def deposite(self, amount):
        pass

    def create_door_card(self, room_id, date):
        pass

    def process_checkout(self, room_id):
        # TODO: 处理对没有订单即没有入住的房间进行的结账操作
        detailed_records_AC = self.query_fee_records(room_id)
        accommodation_bill = Reception.create_accommodation_bill(room_id)
        AC_bill = Reception.create_AC_bill(
            room_id,
            detailed_records_AC,
        )
        pass
        Reception.set_room_state(room_id)

    def query_fee_records(self, room_id):
        return self.orders[room_id].detailed_records_AC

    def calculate_accommodation_fee(days_of_accommodation, fee_of_day):
        return days_of_accommodation * fee_of_day

    def calculate_AC_fee(list_of_detail_records):
        return sum(i.fee for i in list_of_detail_records)

    def create_accommodation_bill(room_id):
        room = Hotel.get_instance().rooms[room_id]
        return Bill(
            "accommodation",
            room_id,
            Reception.calculate_accommodation_fee(
                room.days,
                room.fee_per_day,
            ),
        )

    def create_AC_bill(room_id, detailed_records_AC):
        return Bill("AC", room_id, Reception.calculate_AC_fee(detailed_records_AC))

    def create_detailed_records_AC(self, room_id, date_in, date_out):
        pass

    def process_payment(
        self, room_id, date_out, total_fee_of_accommodation, total_fee_of_AC
    ):
        pass

    def set_room_state(room_id):
        Hotel.get_instance().rooms[room_id].state = False
        # return something


# 订单
class Order:
    def __init__(self, customer_id, room_id):
        self.customer_id = customer_id
        self.room_id = room_id
        self.detailed_records_AC = []


# 管理员
class Manager:
    def __init__(self, name):
        self.name = name

    def run(self):
        return

    def monitor(self):
        return


# 账单
class Bill:
    def __init__(self, tag, room_id, fee):
        self.tag = tag
        self.room_id = room_id
        self.fee = fee
        # TODO: 入住时间
        # TODO: 离开时间


# 详单
class DetailRecord:
    def __init__(self, room_id, speed):
        self.room_id = room_id
        # TODO: 请求时间
        # TODO: 服务开始时间
        # TODO: 服务结束时间
        # TODO: 服务时长
        self.speed = speed
        # TODO: 当前费用
        # TODO: 费率
        self.fee = None  # ?


# 客房
class Room:
    def __init__(self, id, temp, fee_per_day):
        self.id = id
        self.days = 0
        self.temp = temp
        self.target_temp = None
        self.speed = 1  # 默认中风速
        self.state = False  # 是否有顾客入住
        self.AC_status = False
        self.scheduler = None
        self.customer_id = None
        self.fee_per_day = fee_per_day

    def power_on(self, current_room_temp):
        if self.AC_status == False:
            self.scheduler = Hotel.get_instance().scheduler
            self.AC_status = self.scheduler.request(
                self.id, self.target_temp, self.speed
            )
            if self.AC_status == True:
                self.days += 1
            RoomInfo.objects.filter(room_id=self.id).update(AC_status=1)
        pass

    # def request_number(self, service_number):
    #     pass

    def change_temp(self, room_id, target_temp):
        self.target_temp = target_temp
        self.scheduler.change_target_temp(self.id, target_temp)
        return True  # return isOK
        pass

    def change_speed(self, room_id, speed):
        self.speed = speed
        self.scheduler.change_speed(self.id, speed)
        return True  # return isOK
        pass

    def power_off(self):
        self.scheduler.clear(self.id)
        self.scheduler = None
        self.AC_status = False
        RoomInfo.objects.filter(room_id=self.id).update(AC_status=0)
        pass

    def request_state(self, room_id):
        pass


# 调度
class Scheduler:
    def __init__(self):
        self.wait_queue = []
        self.serve_queue = []

    def request(self, room_id, target_temp, speed):
        if len(self.serve_queue) < 3:
            serve_item = ServeItem(room_id, target_temp, speed)
            self.serve_queue.append(serve_item)
            return True
        else:
            return self.schedule(room_id, target_temp, speed)

    def clear(self, room_id):
        for i in self.wait_queue:
            if i.room_id == room_id:
                self.wait_queue.remove(i)
                return
        for i in self.serve_queue:
            if i.room_id == room_id:
                Hotel.get_instance().reception.orders[
                    i.room_id
                ].detailed_records_AC.append(i.detail_record)
                self.serve_queue.remove(i)
                return
        pass

    def change_target_temp(self, room_id, target_temp):
        for i in self.wait_queue:
            if i.room_id == room_id:
                i.target_temp = target_temp
                return
        for i in self.serve_queue:
            if i.room_id == room_id:
                i.change_target_temp(target_temp)
                return

    def change_speed(self, room_id, speed):
        for i in self.wait_queue:
            if i.room_id == room_id:
                i.speed = speed
                return
        for i in self.serve_queue:
            if i.room_id == room_id:
                i.change_speed(speed)
                return

    def schedule(self, room_id, target_temp, speed):
        if len([i for i in self.serve_queue if i.speed < speed]) != 0:  # 优先级调度
            replace_room_ids = [
                i.room_id
                for i in self.serve_queue
                if i.speed
                == (
                    min(
                        [i for i in self.serve_queue if i.speed < speed],
                        key=lambda serve_item: serve_item.speed,
                    ).speed
                )
            ]
            if len(replace_room_ids) == 1:
                replace_room_id = replace_room_ids[0]
            else:
                replace_room_id = max(
                    [i for i in self.serve_queue if i.room_id in replace_room_ids],
                    key=lambda serve_item: serve_item.service_time,
                ).room_id
            self.cast_serve_to_wait(replace_room_id)
            serve_item = ServeItem(room_id, target_temp, speed)
            self.serve_queue.append(serve_item)
            return True
        elif len([i for i in self.serve_queue if i.speed == speed]) != 0:  # 时间片调度
            pass
        else:  # 等待
            wait_item = WaitItem(room_id, target_temp, speed)
            self.wait_queue.append(wait_item)
            return False
        pass

    def cast_serve_to_wait(self, room_id):
        for i in self.serve_queue:
            if i.room_id == room_id:
                self.serve_queue.remove(i)
                wait_item = WaitItem(i.room_id, i.target_temp, i.speed)
                self.wait_queue.append(wait_item)
                return


# 等待对象?
class WaitItem:
    def __init__(self, room_id, target_temp, speed, wait_time=2):
        self.room_id = room_id
        self.target_temp = target_temp
        self.speed = speed
        self.wait_time = wait_time
        pass


# 服务对象
class ServeItem:
    def __init__(self, room_id, target_temp, speed):
        self.room_id = room_id
        self.target_temp = target_temp
        self.speed = speed
        self.service_time = 0
        self.detail_record = DetailRecord(room_id, speed)
        pass

    def change_target_temp(self, target_temp):
        self.target_temp = target_temp

    def change_speed(self, speed):
        self.speed = speed
        Hotel.get_instance().reception.orders[self.room_id].detailed_records_AC.append(
            self.detail_record
        )
        self.detail_record = DetailRecord(self.room_id, speed)

    def generate_detailed_record(self):
        pass
