from django.urls import path
from .views import AddVehicle, MyRideRequests, MyRides,RideList, RideRequestList, RideCreate, RideRequestCreate, AcceptRideRequest, RideUpdate, RideRequestWithdraw, RideRequestDecline, RideRequestUpdate

urlpatterns = [
    path('add_vehicle/',AddVehicle.as_view(), name='add-vehicle'),
    path('rides_list/', RideList.as_view(), name='ride-list'),
    path('myrides_list/', MyRides.as_view(), name='myride-list'),
    path('ride_requests/', RideRequestList.as_view(), name='ride-request-list'),
    path('create/', RideCreate.as_view(), name='ride-create'),
    path('ride_requests/create/', RideRequestCreate.as_view(), name='ride-request-create'),
    path('ride_requests/accept/', AcceptRideRequest.as_view(), name='accept-ride-request'),
    path('update/', RideUpdate.as_view(), name='ride-update'),
    path('ride_requests/myrequests/',MyRideRequests.as_view(), name='my-ride-requests'),
    path('ride_requests/update/', RideRequestUpdate.as_view(), name='ride-request-update'),
    path('ride_requests/withdraw/', RideRequestWithdraw.as_view(), name='ride-request-withdraw'),
    path('ride_requests/decline/', RideRequestDecline.as_view(), name='ride-request-decline'),
]




