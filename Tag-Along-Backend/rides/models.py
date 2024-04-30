from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Car(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cars_owned')
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    seats_available = models.PositiveIntegerField()
    mileage = models.DecimalField(max_digits=8, decimal_places=2)
    color = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.model} ({self.license_plate})"
    
class Ride(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rides_offered')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rides')
    starting_point = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    price_per_head = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    ride_status = models.CharField(max_length=50, default='Yet to Start')
    passengers = models.ManyToManyField(CustomUser, related_name='rides_joined', blank=True)

    def __str__(self):
        return f"Ride from {self.starting_point} to {self.destination} on {self.date}"


class RideRequest(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ride_requests')
    request_status = models.CharField(max_length=50)
    seats_requested = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True)  # Add a TextField for comments

    def __str__(self):
        return f"Request for ride from {self.ride.starting_point} to {self.ride.destination} on {self.ride.date} by {self.requested_by}"
    