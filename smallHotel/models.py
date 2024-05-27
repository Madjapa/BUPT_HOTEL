from django.db import models

# Create your models here.
class CustomerInfo(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=32)
    number = models.IntegerField()


class RoomInfo(models.Model):
    objects = models.Manager()
    room_id = models.IntegerField()
    days = models.IntegerField(default=0)
    temp = models.FloatField()
    target_temp = models.FloatField(default=25)
    speed = models.IntegerField(default=1)
    state = models.BooleanField(default=False)
    AC_status = models.BooleanField(default=False)
    AC_running = models.BooleanField(default=False)
    customer_id = models.IntegerField()
    fee_per_day = models.FloatField()


class BillInfo(models.Model):
    objects = models.Manager()
    tag = models.CharField(max_length=32)
    room_id = models.IntegerField()
    fee = models.FloatField()

class DetailRecordInfo(models.Model):
    objects = models.Manager()
    room_id = models.IntegerField()
    service_start_time = models.IntegerField()
    service_end_time = models.IntegerField()
    service_time = models.IntegerField()
    speed = models.IntegerField()
    fee = models.FloatField()
