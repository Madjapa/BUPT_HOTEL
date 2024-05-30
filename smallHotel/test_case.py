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

    result = '<table cellspacing="10"><tr><td>时间(min)</td><td>房间1</td><td>房间2</td><td>房间3</td><td>房间4</td><td>房间5</td><td>服务队列</td><td>等待队列</td></tr>'

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

        Hotel.get_instance().scheduler.check_wait_queue()

        output(time)
        result += output(time)

        Hotel.get_instance().time_forward()

    return result + "</table>"


def output(time):
    s = ""
    speed_display = ["低", "中", "高"]
    print(time, end="\t")
    s += "<tr>" + '<td align="center">' + str(time) + "</td>"
    for room_id, room in Hotel.get_instance().rooms.items():
        print(room.temp, room.target_temp, speed_display[room.speed], end="\t")
        s += (
            "<td>"
            + str(room.temp)
            + " "
            + str(room.target_temp)
            + " "
            + speed_display[room.speed]
            + "</td>"
        )
    print(
        "["
        + ",".join([str(i.room_id) for i in Hotel.get_instance().scheduler.serve_queue])
        + "]",
        end="\t",
    )
    s += (
        "<td>"
        + "["
        + ", ".join(
            [str(i.room_id) for i in Hotel.get_instance().scheduler.serve_queue]
        )
        + "]"
        + "</td>"
    )
    print([i.room_id for i in Hotel.get_instance().scheduler.wait_queue])
    s += (
        "<td>"
        + "["
        + ", ".join([str(i.room_id) for i in Hotel.get_instance().scheduler.wait_queue])
        + "]"
        + "</td>"
        + "</tr>"
    )

    return s
