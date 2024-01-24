from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username}"


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=20)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    



    



