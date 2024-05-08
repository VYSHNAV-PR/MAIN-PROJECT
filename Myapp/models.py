from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    type=models.CharField(max_length=30)
class Shop(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    shop_name=models.CharField(max_length=30)
    shop_place=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    shop_phone=models.CharField(max_length=30)
    owner_name=models.CharField(max_length=30,default="")
    shop_license_no=models.CharField(max_length=30)
    photo=models.CharField(max_length=250,default="")
    post=models.CharField(max_length=30)
    pin=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    status=models.CharField(max_length=30,default="")
class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    pin=models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    photo = models.CharField(max_length=250, default="")
    gender=models.CharField(max_length=30)
class Staff(models.Model):
    SHOP=models.ForeignKey(Shop,on_delete=models.CASCADE)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)
    aadhar_no=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    pin=models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    photo=models.CharField(max_length=250,default="")
    type=models.CharField(max_length=30)
class Device(models.Model):
    SHOP=models.ForeignKey(Shop,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    brand=models.CharField(max_length=30,default="")
    photo=models.CharField(max_length=250,default="")
    description=models.CharField(max_length=30)
    rent_amount=models.CharField(max_length=30)
class Complaint(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=30)
    date=models.DateField()
    status=models.CharField(max_length=30)
    reply=models.CharField(max_length=30)
class Feedback(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=30)
    date=models.DateField()

class Booking(models.Model):
    DEVICE = models.ForeignKey(Device, on_delete=models.CASCADE,default='')
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=30)
    date=models.DateField()

class BookingSub(models.Model):
    DEVICE = models.ForeignKey(Device, on_delete=models.CASCADE,default='')


class Allocation(models.Model):
    Booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(Staff,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=30)
class Payment(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    Booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=30)
class location(models.Model):
    Login=models.ForeignKey(Login,on_delete=models.CASCADE)
    lattitude=models.CharField(max_length=30)
    longitude=models.CharField(max_length=30)



