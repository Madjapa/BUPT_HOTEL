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
            Hotel.rooms = [Room(0), Room(1), Room(2), Room(3), Room(4)]
        else:
            return

    @staticmethod
    def get_instance():
        if not Hotel.__instance:
            Hotel()
        return Hotel.__instance


# 顾客类
class Customer:
    def __init__(self, name, num, id):
        self.name = name
        self.num = num  # 房间号?
        self.id = id

    # def use(self):
    #     return


# 前台
class Reception:
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.rooms = Hotel.get_instance().rooms

    # def check_in(self):
    #     return

    # def get_bill(self):
    #     return

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

    def process_payment(
        self, room_id, date_out, total_fee_of_accommodation, total_fee_of_AC
    ):
        pass

    def set_room_state(self, room_id):
        for i in self.rooms:
            if i.id == room_id:
                i.state = False
        # return something


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
    def __init__(self, name, value):
        self.name = name
        self.value = value


# 详单
class DetailRecord:
    def __init__(self, name, value):
        self.name = name
        self.value = value


# 客房
class Room:
    def __init__(self, id, time, temp, target_temp):
        self.id = id
        self.time = time
        self.temp = temp
        self.target_temp = target_temp
        self.speed = 1  # 默认中风速
        self.state = False  # 是否有顾客入住
        self.AC_status = False
        self.scheduler = Hotel.get_instance().scheduler

    def power_on(self, current_room_temp):
        if self.AC_status == False:
            self.AC_status = self.scheduler.request(
                self.id, self.id, self.target_temp, self.speed
            )
        pass

    # def request_number(self, service_number):
    #     pass

    def change_temp(self, room_id, target_temp):
        self.target_temp = target_temp
        self.scheduler.change_target_temp(room_id, target_temp)
        return True  # return isOK
        pass

    def change_speed(self, room_id, speed):
        self.speed = speed
        self.scheduler.change_speed(room_id, speed)
        return True  # return isOK
        pass

    def power_off(self):
        self.scheduler = None
        self.scheduler.clear(id)
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
                i.change_target_temp(room_id, target_temp)
                return

    def change_speed(self, room_id, speed):
        for i in self.wait_queue:
            if i.room_id == room_id:
                i.speed = speed
                return
        for i in self.serve_queue:
            if i.room_id == room_id:
                i.change_speed(room_id, speed)
                return

    def schedule(self, room_id, target_temp, speed):
        contain_inferior = False
        contain_same = False
        for i in self.serve_queue:
            if i.speed < speed:
                contain_inferior = True
                break
            elif i.speed == speed:
                contain_same = True
        if contain_inferior == True:  # 优先级调度
            replace_room_ids = []
            count_inferior = 0
            lowest_speed = 2  # 高风速
            for i in self.serve_queue:
                if i.speed < speed:
                    count_inferior += 1
                    replace_room_ids.append(i.room_id)
                    if i.speed < lowest_speed:
                        lowest_speed = i.speed
                        replace_room_ids = []
                    else:
                        replace_room_ids.append(i.room_id)
            if count_inferior == 1:
                replace_room_id = replace_room_ids[0]
            elif len(replace_room_ids) == 1:
                replace_room_id = replace_room_ids[0]
            else:
                longest_service_time = 0
                for i in self.serve_queue:
                    if (
                        i.room_id in replace_room_ids
                        and i.service_time > longest_service_time
                    ):
                        longest_service_time = i.service_time
                        replace_room_id = i.room_id
            self.cast_serve_to_wait(replace_room_id)
            serve_item = ServeItem(room_id, target_temp, speed)
            self.serve_queue.append(serve_item)
            return True
        elif contain_same == True:  # 时间片调度
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
        pass

    def change_target_temp(self, target_temp):
        self.target_temp = target_temp

    def change_speed(self, speed):
        self.speed = speed

    def generate_detailed_record(self):
        pass
