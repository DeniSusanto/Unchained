from django.db import models
import uuid
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import base64
import os
from django.db.models import Q
from math import sin, cos, atan2, sqrt, pi
# Create your models here.
class Clinic(models.Model):
    name=models.CharField(max_length=300, unique=True)
    lat=models.FloatField()
    longitude=models.FloatField()
    alt=models.IntegerField()

    def __str__(self):
        return str(self.name)
    
    def calc_dist(self, target):
        if InterDistance.objects.filter(Q(clinic1=self) & Q(clinic2=target)).count() > 0:
            obj=InterDistance.objects.get(clinic1=self , clinic2=target)
            return obj.distance
        else:
            obj=InterDistance.objects.get(clinic1=target , clinic2=self)
            return obj.distance

class InterDistance(models.Model):
    clinic1=models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic1')
    clinic2=models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic2')
    distance=models.FloatField()
    def __str__(self):
        return self.clinic1.name + " - " + self.clinic2.name + ": " + str(self.distance) + " km"

class ItemCategory(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class ItemCatalogue(models.Model):
    name=models.CharField(max_length=100)
    weight=models.FloatField()
    category= models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="item/")
    description=models.TextField(blank=True, null=True)

    def __str__(self):
        return str("ID: " + str(self.id) + " " + self.name)

    def get_name(self):
        return str(self.name)

class UserRecord(models.Model):
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    username=models.CharField(max_length=250, unique=True)
    password=models.CharField(max_length=100)
    email=models.EmailField(max_length=254, unique=True)
    image=models.ImageField(upload_to="profilePic/", blank=True, null=True, default='profilePic/noUserPic.png')

    class Meta:
        abstract=True

    def fullName(self):
        return self.firstName + " " + self.lastName       

class ClinicManager(UserRecord):
    locationID=models.OneToOneField(Clinic, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.firstName+" " + self.lastName + " from clinic " + self.locationID.name)



class WarehousePersonnel(UserRecord):
    pass

    def __str__(self):
        return str(self.firstName+" " + self.lastName)

class Dispatcher(UserRecord):
    pass

    def __str__(self):
        return str(self.firstName+" " + self.lastName)

class HospitalAuthority(UserRecord):
    pass

    def __str__(self):
        return str(self.firstName+" " + self.lastName)

class Cart(models.Model):
    clinicID= models.OneToOneField(ClinicManager, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.clinicID.firstName+" "+ self.clinicID.lastName+"'s cart")

    def getWeight(self):
        itemList=ItemsInCart.objects.filter(cartID=self)
        weight=float(0)
        for item in itemList:
            weight=weight+(item.itemID.weight * item.quantity)
        
        return weight
    
    def getQuantity(self):
        itemList=ItemsInCart.objects.filter(cartID=self)
        num=0
        for item in itemList:
            num+=item.quantity
        
        return num

    def emptyCart(self):
        itemList=ItemsInCart.objects.filter(cartID=self)
        for item in itemList:
            item.delete()

class ItemsInCart(models.Model):
    cartID=models.ForeignKey(Cart, on_delete=models.CASCADE)
    itemID=models.ForeignKey(ItemCatalogue, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.cartID.clinicID.firstName + " " + self.cartID.clinicID.lastName + "'s cart: " + self.itemID.name)
    
    def itemWeight(self):
        itemObj=ItemCatalogue.objects.get(pk=self.itemID)
        weight=itemObj.weight * self.quantity
        return weight

class Token(models.Model):
    def id_generator():
        return get_random_string(length=6)
    email=models.EmailField(max_length=254, unique=True)
    role=models.IntegerField()
    token=models.CharField(max_length=10,default=id_generator,editable=False)

    '''def getEmail(self):
        ret_email=Token.objects.filter(token=self)
        return ret_email'''

    def __str__(self):
      return str(self.email + ": "+self.token)

class Order(models.Model):
    clinicID=models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    weight=models.FloatField()
    status=models.IntegerField()
    priority=models.IntegerField()
    orderDateTime=models.DateTimeField()
    file=models.FileField(upload_to='orderLabel/', null=True, blank=True)

    def __str__(self):
        return str("Order id:" + str(self.id) + " belong to " + self.clinicID.fullName())

    def priorityString(self):
        n=self.priority
        if n == 1:
            return "High"
        elif n == 2:
            return "Medium"
        else:
            return "Low"

    def str_status(self):
        if self.status == 1:
            return "Queued for Processing"
        elif self.status == 2:
            return "Processing by Warehouse"
        elif self.status == 3:
            return "Queued for Dispatch"
        elif self.status == 4:
            return "Dispatched"
        else:
            return "Delivered"

    def weightRound(self):
        return format(self.weight,'.2f') 
    
    def getItemQuantity(self, itemID):
        if ItemsInOrder.objects.filter(Q(itemID=itemID) & Q(orderID=self.id)).count()==1:
            return ItemsInOrder.objects.get(itemID=itemID, orderID=self.id).quantity

class ItemsInOrder(models.Model):
    orderID=models.ForeignKey(Order, on_delete=models.CASCADE)
    itemID=models.ForeignKey(ItemCatalogue, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.orderID.clinicID.firstName + " " + self.orderID.clinicID.lastName + "'s order: " + self.itemID.name)


class OrderRecord(models.Model):
    orderID=models.ForeignKey(Order, on_delete=models.CASCADE)
    dispatchedDateTime=models.DateTimeField()
    deliveredDateTime=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str("Order record of order " + str(self.orderID.id))

