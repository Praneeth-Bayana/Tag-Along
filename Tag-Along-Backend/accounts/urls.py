from django.urls import path
from .views import CustomUserList, TokenRefresher, UserLogin, UserRegistration, UserLogout, get_profile

urlpatterns = [
    path('listusers/', CustomUserList.as_view(), name='user-list'),
    path('createuser/', UserRegistration.as_view() , name='user-create'),
    path('loginuser/', UserLogin.as_view() , name='user-login'),
    path('logoutuser/', UserLogout.as_view() , name='user-logout'),
    path('getuserprofile/', get_profile , name='get-user-profile'),
    path('refresh-token/', TokenRefresher.as_view() , name='refresh-token'),

]  
