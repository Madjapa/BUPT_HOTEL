from smallHotel.models import *

class Hotel:
    __instance = None
    manager = None
    reception = None
    scheduler = None
    rooms = None
    current_time = None

    def __init__(self):
        if Hotel.__instance is None:
            Hotel.__instance = self
            Hotel.manager = Manager("syb")
            Hotel.scheduler = Scheduler()
            Hotel.rooms = {}
            for i in RoomInfo.objects.all():
                Hotel.rooms[i.room_id] = Room(i.room_id, i.temp, i.fee_per_day)
            Hotel.reception = Reception("syb")
            Hotel.current_time = 0
        else:
            return

    @staticmethod
    def get_instance():
        if not Hotel.__instance:
            Hotel()
        return Hotel.__instance

    def time_forward(self):
        Hotel.get_instance().current_time += 1  # 前进1分钟
        for i in Hotel.get_instance().rooms.values():
            if i.AC_status == False and i.temp < i.init_temp:
                i.temp += 0.5  # 回温每分钟0.5℃
                RoomInfo.objects.filter(room_id=i.id).update(temp=i.temp)
        Hotel.get_instance().scheduler.check_serve_queue()
        pass


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
        self.orders = {room_id: [] for room_id in Hotel.get_instance().rooms.keys()}

    def register_customer_info(self, customer_id, customer_name, number, date):
        CustomerInfo.objects.create(name=customer_name,number=number,customer_id=customer_id)
        self.customers.append(Customer(customer_id, customer_name, number))
        return True  # return isOK

    def check_room_state(self, date):
        return {i.room_id: i.state for i in RoomInfo.objects.all()}

    def create_accommodation_order(self, customer_id, room_id):
        # TODO: 处理对已有订单即已入住的房间进行的创建订单操作
        self.orders[int(room_id)].append(Order(customer_id, room_id))
        room = Hotel.get_instance().rooms[int(room_id)]
        room.state = True
        room.customer_id = customer_id
        RoomInfo.objects.filter(room_id=room_id).update(customer_id=customer_id, state=1)

    def deposite(self, amount, room_id):
        self.orders[room_id][-1].deposit = amount
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
        self.orders[room_id][-1].accommodation_bill = accommodation_bill
        self.orders[room_id][-1].AC_bill = AC_bill
        pass
        Reception.set_room_state(room_id)

    def query_fee_records(self, room_id):
        return self.orders[room_id][-1].detailed_records_AC

    @staticmethod
    def calculate_accommodation_fee(days_of_accommodation, fee_of_day):
        return days_of_accommodation * fee_of_day

    @staticmethod
    def calculate_AC_fee(list_of_detail_records):
        return sum(i.fee for i in list_of_detail_records)

    @staticmethod
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

    @staticmethod
    def create_AC_bill(room_id, detailed_records_AC):
        return Bill("AC", room_id, Reception.calculate_AC_fee(detailed_records_AC))

    def create_detailed_records_AC(self, room_id, date_in, date_out):
        pass

    def process_payment(
        self, room_id, date_out, total_fee_of_accommodation, total_fee_of_AC
    ):
        pass

    @staticmethod
    def set_room_state(room_id):
        Hotel.get_instance().rooms[room_id].state = False
        # return something


# 订单
class Order:
    def __init__(self, customer_id, room_id):
        self.customer_id = customer_id
        self.room_id = room_id
        self.detailed_records_AC = []
        self.deposit = None
        self.accommodation_bill = None
        self.AC_bill = None


# 房卡
class Card:
    def __init__(self, card_id):
        self.card_id = card_id
        self.room_id = None
        pass


# 管理员
class Manager:
    def __init__(self, name):
        self.name = name

    # def run(self):
    #     return

    # def monitor(self):
    #     return


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
    def __init__(self, room_id, speed, start_time, request_time):
        self.room_id = room_id
        self.request_time = request_time
        self.service_start_time = start_time
        self.service_end_time = None
        self.service_time = None
        self.speed = speed
        # TODO: 当前费用
        # TODO: 费率
        self.fee = None  # ?

    def store(self):
        DetailRecordInfo(
            room_id=self.room_id,
            speed=self.speed,
            service_start_time=self.service_start_time,
            service_end_time=self.service_end_time,
            service_time=self.service_time,
        ).save()
        pass


# 客房
class Room:
    def __init__(self, id, temp, fee_per_day):
        self.id = id
        self.days = 0
        self.temp = temp
        self.target_temp = 25  # 制冷目标温度默认为25℃
        self.speed = 1  # 默认中风速
        self.state = False  # 是否有顾客入住
        self.AC_status = False
        self.AC_running = False
        self.scheduler = None
        self.customer_id = None
        self.fee_per_day = fee_per_day
        self.init_temp = temp

    def power_on(self, current_room_temp):
        if self.AC_status == False:
            self.AC_status = True
            self.scheduler = Hotel.get_instance().scheduler
            self.AC_running = self.scheduler.request(
                self.id, self.target_temp, self.speed
            )
            self.days += 1
            RoomInfo.objects.filter(room_id=self.id).update(AC_status=1)
            RoomInfo.objects.filter(room_id=self.id).update(AC_running=self.AC_running)
        pass

    # def request_number(self, service_number):
    #     pass

    def change_temp(self, room_id, target_temp):
        self.target_temp = target_temp
        self.scheduler.change_target_temp(self.id, target_temp)
        RoomInfo.objects.filter(room_id=self.id).update(target_temp=target_temp)
        return True  # return isOK
        pass

    def change_speed(self, room_id, speed):
        self.speed = speed
        self.scheduler.change_speed(self.id, speed)
        RoomInfo.objects.filter(room_id=self.id).update(speed=speed)
        return True  # return isOK
        pass

    def power_off(self):
        self.scheduler.clear(self.id)
        self.scheduler = None
        self.AC_status = False
        self.AC_running = False
        RoomInfo.objects.filter(room_id=self.id).update(AC_status=0)
        RoomInfo.objects.filter(room_id=self.id).update(AC_running=0)
        pass

    def stop_running(self):
        self.scheduler.clear(self.id)
        self.AC_running = False
        RoomInfo.objects.filter(room_id=self.id).update(AC_running=0)

    # def request_state(self, room_id):
    #     pass


# 调度
class Scheduler:
    def __init__(self):
        self.wait_queue = []
        self.serve_queue = []

    def request(self, room_id, target_temp, speed):
        if len(self.serve_queue) < 3:
            serve_item = ServeItem(
                room_id, target_temp, speed, Hotel.get_instance().current_time
            )
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
                i.detail_record.service_end_time = Hotel.get_instance().current_time
                i.detail_record.service_time = (
                    i.detail_record.service_end_time
                    - i.detail_record.service_start_time
                )
                Hotel.get_instance().reception.orders[int(i.room_id)][
                    -1
                ].detailed_records_AC.append(i.detail_record)
                i.detail_record.store()
                self.serve_queue.remove(i)
                self.cast_wait_to_serve()
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
                    key=lambda serve_item: (
                        Hotel.get_instance().current_time - serve_item.serve_start_time
                    ),
                ).room_id
            self.cast_serve_to_wait(replace_room_id)
            self.serve_queue.append(
                ServeItem(
                    room_id, target_temp, speed, Hotel.get_instance().current_time
                )
            )
            return True
        elif len([i for i in self.serve_queue if i.speed == speed]) != 0:  # 时间片调度
            self.wait_queue.append(
                WaitItem(room_id, target_temp, speed, Hotel.get_instance().current_time)
            )
            return False
        else:  # 等待
            wait_item = WaitItem(
                room_id, target_temp, speed, Hotel.get_instance().current_time
            )
            self.wait_queue.append(wait_item)
            return False
        pass

    def cast_serve_to_wait(self, room_id=None, *, speed=None):
        if room_id is not None:
            for i in self.serve_queue:
                if i.room_id == room_id:
                    cast_to_wait_serve_item = i
                    break
        else:
            if min([i.speed for i in self.serve_queue]) > speed:
                return False
            cast_items = [
                i
                for i in self.serve_queue
                if i.speed == min([i.speed for i in self.serve_queue])
                and Hotel.get_instance().current_time - i.serve_start_time != 0
            ]
            cast_to_wait_serve_item = min(
                cast_items,
                key=lambda serve_item: serve_item.serve_start_time,
            )
        self.serve_queue.remove(cast_to_wait_serve_item)
        self.wait_queue.append(
            WaitItem(
                cast_to_wait_serve_item.room_id,
                cast_to_wait_serve_item.target_temp,
                cast_to_wait_serve_item.speed,
                cast_to_wait_serve_item.request_time,
            )
        )
        Hotel.get_instance().rooms[cast_to_wait_serve_item.room_id].AC_running = False
        RoomInfo.objects.filter(room_id=cast_to_wait_serve_item.room_id).update(
            AC_running=0
        )

    def check_serve_queue(self):
        for i in self.serve_queue[:]:
            if (
                Hotel.get_instance().rooms[i.room_id].temp
                <= Hotel.get_instance().rooms[i.room_id].target_temp
            ):
                Hotel.get_instance().rooms[i.room_id].stop_running()
                continue
            match i.speed:
                case 0:  # 低风速
                    Hotel.get_instance().rooms[i.room_id].temp = (
                        round(Hotel.get_instance().rooms[i.room_id].temp - 1 / 3, 4)
                        if (Hotel.get_instance().rooms[i.room_id].temp - 1 / 3) % 0.1
                        > 1e-4
                        else round(
                            Hotel.get_instance().rooms[i.room_id].temp - 1 / 3, 1
                        )
                    )
                case 1:  # 中风速
                    Hotel.get_instance().rooms[i.room_id].temp -= 0.5
                case 2:  # 高风速
                    Hotel.get_instance().rooms[i.room_id].temp -= 1
            RoomInfo.objects.filter(room_id=i.room_id).update(temp=Hotel.get_instance().rooms[i.room_id].temp)
            if (
                Hotel.get_instance().rooms[i.room_id].temp
                <= Hotel.get_instance().rooms[i.room_id].target_temp
            ):
                Hotel.get_instance().rooms[i.room_id].temp = (
                    Hotel.get_instance().rooms[i.room_id].target_temp
                )
                Hotel.get_instance().rooms[i.room_id].stop_running()

    def check_wait_queue(self):
        cast_items = [
            i
            for i in self.wait_queue
            if Hotel.get_instance().current_time - i.wait_start_time >= i.wait_time
        ]
        cast_items.sort(key=lambda wait_item: wait_item.wait_start_time)
        for i in cast_items:
            if (
                min(
                    [
                        (Hotel.get_instance().current_time - i.serve_start_time)
                        for i in self.serve_queue
                    ]
                )
                == 0
            ):
                break
            if self.cast_serve_to_wait(speed=i.speed) == False:
                i.wait_time += 2
            else:
                self.cast_wait_to_serve(i.room_id)
        pass

    def cast_wait_to_serve(self, room_id=None):
        if room_id is None:
            cast_items = [
                i
                for i in self.wait_queue
                if i.speed == max([i.speed for i in self.wait_queue])
            ]
            if len(cast_items) == 0:
                return
            cast_to_serve_wait_item = min(
                cast_items,
                key=lambda wait_item: wait_item.wait_start_time,
            )
        else:
            for i in self.wait_queue:
                if i.room_id == room_id:
                    cast_to_serve_wait_item = i
                    break
        self.wait_queue.remove(cast_to_serve_wait_item)
        self.serve_queue.append(
            ServeItem(
                cast_to_serve_wait_item.room_id,
                cast_to_serve_wait_item.target_temp,
                cast_to_serve_wait_item.speed,
                cast_to_serve_wait_item.request_time,
            )
        )
        Hotel.get_instance().rooms[cast_to_serve_wait_item.room_id].AC_running = True
        RoomInfo.objects.filter(room_id=cast_to_serve_wait_item.room_id).update(
            AC_running=1
        )


# 等待对象?
class WaitItem:
    def __init__(self, room_id, target_temp, speed, request_time, wait_time=2):
        self.room_id = room_id
        self.target_temp = target_temp
        self.speed = speed
        self.wait_time = wait_time
        self.wait_start_time = Hotel.get_instance().current_time
        self.request_time = request_time
        pass


# 服务对象
class ServeItem:
    def __init__(self, room_id, target_temp, speed, request_time):
        self.room_id = room_id
        self.target_temp = target_temp
        self.speed = speed
        self.serve_start_time = Hotel.get_instance().current_time
        self.detail_record = DetailRecord(
            room_id, speed, Hotel.get_instance().current_time, request_time
        )
        self.request_time = request_time
        pass

    def change_target_temp(self, target_temp):
        self.target_temp = target_temp

    def change_speed(self, speed):
        self.speed = speed
        self.detail_record.service_end_time = Hotel.get_instance().current_time
        self.detail_record.service_time = (
            self.detail_record.service_end_time - self.detail_record.service_start_time
        )
        Hotel.get_instance().reception.orders[self.room_id][
            -1
        ].detailed_records_AC.append(self.detail_record)
        self.detail_record.store()
        self.detail_record = DetailRecord(
            self.room_id, speed, Hotel.get_instance().current_time, self.request_time
        )

    def generate_detailed_record(self):
        pass
    
    def create_csv(self):
        import csv

        data =[[Order.customer_id ,Order.room_id ,Order.detailed_records_AC , Order.deposit ,Order.accommodation_bill ,Order.AC_bill],
               [Bill.tag ,Bill.room_id ,Bill.fee ],
               [DetailRecord.room_id ,DetailRecord.request_time ,DetailRecord.service_start_time ,DetailRecord.service_end_time ,DetailRecord.service_time ,DetailRecord.speed ]]

        with open('output.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
         
