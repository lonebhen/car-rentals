from django.shortcuts import render, get_object_or_404
from .models import Car, RentalReservation, Customer
from .serializers import CarSerializer, RentalReservationSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import Http404
from datetime import datetime
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


class CarView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        available_only = request.query_params.get('available', None)
        
        if available_only is not None and available_only.lower() == 'true':
            cars = Car.objects.filter(availability=True)
        else:
            cars = Car.objects.all()
        
        serializer = CarSerializer(cars, many=True)
        return Response({"cars":serializer.data}, status=status.HTTP_200_OK)
    
    
    
class CarDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            raise Http404
        
        
    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response({"car": serializer.data}, status=status.HTTP_200_OK)
    
    
    
    
class CarSearchAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = Car.objects.all()
        make = self.request.query_params.get('make')
        model = self.request.query_params.get('model')
        year = self.request.query_params.get('year')
        availability = self.request.query_params.get('availability')

        if make:
            queryset = queryset.filter(make__icontains=make)
        if model:
            queryset = queryset.filter(model__icontains=model)
        if year:
            queryset = queryset.filter(year=year)
        if availability:
            queryset = queryset.filter(availability=availability)

        return queryset
    
    
class UserRentalBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_rental_bookings = RentalReservation.objects.filter(customer=request.user)
        serializer = RentalReservationSerializer(user_rental_bookings, many=True)
        return Response({"user_booking": serializer.data})
    
    
class ApprovedUserRentalBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        approved_user_rental_bookings = RentalReservation.objects.filter(customer=request.user, approved=True)
        serializer = RentalReservationSerializer(approved_user_rental_bookings, many=True)
        return Response({"approved_bookings": serializer.data})
        
        




class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

class BookCarAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Get the authenticated user
        user = request.user
        print(user)
        # Retrieve the associated Customer object
        
        try:
            print(f"User id is {user.id}")
            print(type(user.id))
            customer = User.objects.get(pk=user.id)
            
            print(f"Customer id is {customer.pk}")
            print(f"Customer is {customer}")
        except User.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        

        
        # Add customer to the request data
        request.data['customer'] = customer.id
        
        serializer = RentalReservationSerializer(data=request.data)
        
        if serializer.is_valid():
            print("here")
            print(f"Serialized data is {serializer.validated_data}")
            car_id = serializer.validated_data.get('car')
            print(f"Car id is {car_id}")
            car = get_object_or_404(Car, id=car_id.id)
            
            print(f"Car: {car}")
            print(f"Car id is {car.id}")
            
            if not car.availability:
                return Response({"message": "Car is not available for booking"}, status=status.HTTP_400_BAD_REQUEST)
            
            pickup_date = serializer.validated_data.get('pickup_date')
            return_date = serializer.validated_data.get('return_date')
            
            if return_date <= pickup_date or pickup_date < datetime.today().date():
                return Response({"message": "Invalid pickup or return date"}, status=status.HTTP_400_BAD_REQUEST)
            
            total_cost = self.calculate_total_cost(pickup_date, return_date, car.daily_rate)
            serializer.save(total_cost=total_cost)
            
            car.availability = False
            car.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_total_cost(self, pickup_date, return_date, daily_rate):
        duration = (return_date - pickup_date).days
        total_cost = daily_rate * duration
        return total_cost
