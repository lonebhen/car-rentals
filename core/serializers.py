from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'images', 'year', 'registration_number', 'color', 'availability']

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = [obj.image.url, obj.image2.url, obj.image3.url]
        return images




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        
        
class RentalReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalReservation
        exclude = ('total_cost',)