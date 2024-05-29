from smallHotel.system import *


test_case = [
    ["开机", "", "", "", ""],
    ["18", "开机", "", "", "开机"],
    ["", "", "开机", "", ""],
    ["", "19", "", "开机", ""],
    ["", "", "", "", "22"],
    ["高", "", "", "", ""],
    ["", "关机", "", "", ""],
    ["", "开机", "", "", "高"],
    ["", "", "", "", ""],
    ["22", "", "", "18,高", ""],
    ["", "", "", "", ""],
    ["", "22", "", "", ""],
    ["", "", "", "", "低"],
    ["", "", "", "", ""],
    ["关机", "", "24,低", "", ""],
    ["", "", "", "", "20,高"],
    ["", "关机", "", "", ""],
    ["", "", "高", "", ""],
    ["开机", "", "", "20,中", ""],
    ["", "开机", "", "", ""],
    ["", "", "", "", "25"],
    ["", "", "", "", ""],
    ["", "", "关机", "", ""],
    ["", "", "", "", "关机"],
    ["关机", "", "", "", ""],
    ["", "关机", "", "关机", ""],
]


def test():
    RoomInfo.objects.all().delete()
    RoomInfo(room_id=1, temp=32, fee_per_day=100).save()
    RoomInfo(room_id=2, temp=28, fee_per_day=125).save()
    RoomInfo(room_id=3, temp=30, fee_per_day=150).save()
    RoomInfo(room_id=4, temp=29, fee_per_day=200).save()
    RoomInfo(room_id=5, temp=35, fee_per_day=100).save()

    for i in range(1, 1 + 5):
        Hotel.get_instance().reception.create_accommodation_order(-1, i)

    for time in range(len(test_case)):
        for j in range(5):
            room_id = j + 1
            operations = test_case[time][j].split(",")
            for operation in operations:
                match operation:
                    case "开机":
                        Hotel.get_instance().rooms[room_id].power_on(-1)
                    case "关机":
                        Hotel.get_instance().rooms[room_id].power_off()
                    case "高":
                        Hotel.get_instance().rooms[room_id].change_speed(-1, 2)
                    case "中":
                        Hotel.get_instance().rooms[room_id].change_speed(-1, 1)
                    case "低":
                        Hotel.get_instance().rooms[room_id].change_speed(-1, 0)
                    case "":
                        pass
                    case _:
                        Hotel.get_instance().rooms[room_id].change_temp(
                            -1, float(operation)
                        )
        Hotel.get_instance().time_forward()
