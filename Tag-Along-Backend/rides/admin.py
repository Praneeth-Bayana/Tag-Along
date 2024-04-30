from django.contrib import admin
from .models import Car, Ride, RideRequest

# Register your models here.
admin.site.register(Car)
admin.site.register(Ride)
admin.site.register(RideRequest)
