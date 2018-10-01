from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Visitor(models.Model):
    visitorid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=200)
    contactno = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    person = models.TextField()
    personid = models.TextField(null=True)


class Visitee(models.Model):
    visiteeid = models.AutoField(primary_key=True)
    visiteename = models.CharField(max_length=50)
    visiteecontact = models.CharField(max_length=10)
    visiteeflatno = models.CharField(max_length=100, null=True)
    # visitee_Dept = models.CharField(max_length=20, null=True)


class Visit(models.Model):
    visitid = models.AutoField(primary_key=True)
    visitorid = models.ForeignKey('Visitor', on_delete=CASCADE)
    visiteeid = models.ForeignKey('Visitee', on_delete=CASCADE)
    purpose = models.CharField(max_length=100)
    vehicleno = models.TextField(null=True)
    checkin = models.TimeField(null=True)
    checkout = models.TimeField(null=True)


class Gate(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=50)
    pswrd = models.CharField(max_length=50)
    contno = models.CharField(max_length=10)