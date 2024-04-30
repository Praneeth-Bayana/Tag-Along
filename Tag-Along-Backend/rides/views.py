from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ride, RideRequest
from .serializers import CarSerializer, CreateRideSerializer, MyRideRequestsSerializer, RideRequestListSerializer, RideSerializer, RideRequestSerializer, RideUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .decorators import validate_access_token


class AddVehicle(APIView):

    @validate_access_token
    def post(self, request, format=None):
        # Get the current user's ID
        print(request.user_id)
        current_user = request.user_id
        # Add the current user's ID to the request data before creating the serializer
        request.data['owner'] = current_user
        
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RideList(APIView):
    
    @validate_access_token
    def get(self, request):                                  
        rides = Ride.objects.all()                           
        serializer = RideSerializer(rides, many=True)        
        return Response(serializer.data)      

class MyRides(APIView):
    
    @validate_access_token
    def get(self, request, format=None):
        # Assuming user_id is passed as a parameter in the URL
        user_id = request.user_id
        # Retrieve rides offered by the user using queryset filtering
        rides_offered = Ride.objects.filter(driver_id=user_id)
        
        # Serialize the queryset data
        serializer = RideSerializer(rides_offered, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)



class RideRequestList(APIView):
    
    @validate_access_token
    def post(self, request):
        print(request.data)
        ride_id = request.data['ride_id']
        
        ride_requests = RideRequest.objects.filter(ride_id=ride_id)
        serializer = RideRequestListSerializer(ride_requests, many=True)
        return Response(serializer.data)               

class RideCreate(APIView):
    
    @validate_access_token
    def post(self, request):
        driver_id = request.user_id
        request.data['driver'] = driver_id

        serializer = CreateRideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideRequestCreate(APIView):

    @validate_access_token
    def post(self, request):
        requester = request.user_id
        request.data['requested_by'] = requester
        serializer = RideRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptRideRequest(APIView):
    
    @validate_access_token
    def post(self, request):
        try:
            request_id = request.data["req_id"]
            ride_request = RideRequest.objects.get(pk=request_id)
        except RideRequest.DoesNotExist:
            return Response({"message": "Ride request does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if ride_request.request_status == "Approved":
            return Response({"message": "Ride request has already been approved"}, status=status.HTTP_400_BAD_REQUEST)

        # Change the request status to Approved
        ride_request.request_status = "Approved"
        ride_request.save()

        # Add the passenger to the ride
        ride = ride_request.ride
        ride.passengers.add(ride_request.requested_by)
        ride.save()

        serializer = RideRequestSerializer(ride_request)
        return Response(serializer.data)

class RideUpdate(APIView):
    
    @validate_access_token
    def patch(self, request):
        try:
            ride_id = request.data["ride_id"]
            ride = Ride.objects.get(pk=ride_id)
        except Ride.DoesNotExist:
            return Response({"message": "Ride does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RideUpdateSerializer(ride, data=request.data["update"], partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RideRequestUpdate(APIView):
    
    @validate_access_token
    def patch(self, request):
        try:
            request_id = request.data['ride_request_id']
            ride_request = RideRequest.objects.get(pk=request_id)
        except RideRequest.DoesNotExist:
            return Response({"message": "Ride request does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RideRequestSerializer(ride_request, data=request.data['update'], partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideRequestWithdraw(APIView):
    
    @validate_access_token
    def patch(self, request):
        try:
            request_id = request.data['ride_request_id']
            ride_request = RideRequest.objects.get(pk=request_id)
        except RideRequest.DoesNotExist:
            return Response({"message": "Ride request does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RideRequestSerializer(ride_request, data=request.data['update'], partial=True)
        if serializer.is_valid():
            serializer.save()
        
        return Response({"message": "Ride request withdrawn successfully"}, status=status.HTTP_204_NO_CONTENT)

class RideRequestDecline(APIView):
    
    @validate_access_token
    def post(self, request):
        try:
            request_id = request.data["req_id"]
            ride_request = RideRequest.objects.get(pk=request_id)
        except RideRequest.DoesNotExist:
            return Response({"message": "Ride request does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if ride_request.request_status == "Declined":
            return Response({"message": "Ride request has already been declined"}, status=status.HTTP_400_BAD_REQUEST)

        # Change the request status to Declined
        ride_request.request_status = "Declined"
        ride_request.save()

        # Add the passenger to the ride
        ride = ride_request.ride
        ride.passengers.add(ride_request.requested_by)
        ride.save()

        serializer = RideRequestSerializer(ride_request)
        return Response(serializer.data)


class MyRideRequests(APIView):
    
    @validate_access_token
    def get(self, request):
        user = request.user_id  # Assuming you have user information in request
        my_ride_requests = RideRequest.objects.filter(requested_by=user)
        serializer = MyRideRequestsSerializer(my_ride_requests, many=True)
        return Response(serializer.data)