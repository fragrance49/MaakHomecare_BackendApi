from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Each task is owned by one user
    description = models.CharField(max_length=150) #Each task has a description of what needs to be done
    due = models.DateField() #Each task has a due date, which is a Python datetime.date

class Members(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    birthday = models.CharField(max_length=150)
    gender = models.CharField(max_length=150)
    phonenumber = models.CharField(max_length=150)

class Services(models.Model):
    title = models.CharField(max_length=150)
    imageurl = models.CharField(max_length=150)
    price = models.CharField(max_length=50)
    description = models.TextField()
    phonenumber = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

class Booking(models.Model):
    userid = models.IntegerField(max_length=11)
    serviceid = models.IntegerField(max_length=11)
    bookingaddress = models.CharField(max_length=150)
    bookingdate = models.CharField(max_length=150)
