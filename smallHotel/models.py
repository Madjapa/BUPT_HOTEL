from django.db import models

# Create your models here.
class CustomerInfo(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=32)
    number = models.IntegerField()


class RoomInfo(models.Model):
    objects = models.Manager()
    room_id = models.IntegerField()
    days = models.IntegerField()
    temp = models.IntegerField()
    target_temp = models.IntegerField()
    speed = models.IntegerField()
    state = models.BooleanField()
    AC_status = models.BooleanField()
    customer_id = models.IntegerField()
    fee_per_day = models.IntegerField()


class BillInfo(models.Model):
    objects = models.Manager()
    tag = models.CharField(max_length=32)
    room_id = models.IntegerField()
    fee = models.FloatField()

class DetailRecordInfo(models.Model):
    objects = models.Manager()
    room_id = models.IntegerField()
    speed = models.IntegerField()
    fee = models.FloatField()
