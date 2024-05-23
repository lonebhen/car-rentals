from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from cloudinary.models import CloudinaryField
# Create your models here.

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username}"


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = CloudinaryField('image')
    image2 = CloudinaryField('image')
    image3 = CloudinaryField('image')
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=20)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.make} - {self.model} - {self.registration_number}"
    


class RentalReservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    return_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.customer} - {self.car} ({self.pickup_date} to {self.return_date})"
    


class RentalRate(models.Model):
    car_type = models.CharField(max_length=50)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.car_type} - Daily: {self.daily_rate}, Weekly: {self.weekly_rate}, Monthly: {self.monthly_rate}"
    


class Payment(models.Model):
    reservation = models.OneToOneField(RentalReservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.reservation}"



    



