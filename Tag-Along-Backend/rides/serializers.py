from rest_framework import serializers
from .models import Ride,RideRequest, Car
from accounts.serializers import CustomUserSerializer

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['owner', 'model', 'license_plate', 'seats_available', 'mileage', 'color', 'car_type']
        
class RideSerializer(serializers.ModelSerializer):
    driver = CustomUserSerializer()
    car = CarSerializer()
    passengers = CustomUserSerializer(many=True)
    class Meta:
        model = Ride
        fields = '__all__'

class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = '__all__'

class RideRequestListSerializer(serializers.ModelSerializer):
    requested_by = CustomUserSerializer()
    class Meta:
        model = RideRequest
        fields = '__all__'

class RideUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['starting_point', 'destination', 'date', 'starttime', 'endtime', 'price_per_head', 'available_seats', 'ride_status']


class MyRideRequestsSerializer(serializers.ModelSerializer):
    ride = RideSerializer()
    class Meta:
        model = RideRequest
        fields = '__all__'