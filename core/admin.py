from django.contrib import admin
from django import forms
import cloudinary.uploader
from natsort import natsorted
from .models import Car

# Register your models here.


admin.site.register(Car)