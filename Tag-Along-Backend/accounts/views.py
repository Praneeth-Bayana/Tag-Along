from django.shortcuts import render
from .serializers import CustomUserSerializer as UserSerializer
from django.contrib.auth import logout
from django.http import JsonResponse

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .decorators import validate_access_token
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

@api_view(['GET'])
@validate_access_token
def get_profile(request):
    
    user_id = request.user_id
    user = CustomUser.objects.get(id=user_id)
    
    # Extract profile details
    profile = {
        "username": user.username,
        "email": user.email,
        # Add more profile details as needed
    }

    # Return the profile details in the response
    return Response(profile)


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        print(user)
        profile = {
                    "username": user.username,
                    "email": user.email,
                    # Add more profile details as needed
                }
        response = JsonResponse({'success': True, 'message': 'User SignedUp successfully','user':profile})
        response.set_cookie("refresh_token", str(refresh), httponly=True, samesite=None, secure=True)
        response.set_cookie("access_token", str(refresh.access_token),samesite=None, secure=True)
        return response


class UserLogin(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Extract tokens from the response
            tokens = response.data
            refresh_token = tokens.get('refresh')
            access_token = tokens.get('access')
            if refresh_token and access_token:
                secret_key = os.environ.get('SECRET_KEY')
                decoded_token = jwt.decode(access_token, secret_key, algorithms=['HS256'])
                
                user_id = decoded_token['user_id']
                user = CustomUser.objects.get(id=user_id)
                
                profile = {
                    "username": user.username,
                    "email": user.email,
                    # Add more profile details as needed
                }
                
                # Create a new response object
                json_response = JsonResponse({'success': True, 'message': 'User Logged IN successfully','user':profile})
                # Set refresh token as HTTP-only cookie
                json_response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='none', secure=True)
                # Set access token as regular cookie
                json_response.set_cookie('access_token', access_token, samesite='none', secure=True)
                return json_response
        else:
            return Response({'success': False, 'message': 'Invalid Credentials'})
        
class UserLogout(APIView):
    def post(self, request):
        # Perform logout for the current user
        logout(request)
        response = Response({"message": "Logout successful"})
        response.set_cookie('access_token','', samesite='None', secure=True)
        response.set_cookie('refresh_token', '',samesite='None',httponly=True, secure=True)
        return response
    
class TokenRefresher(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not refresh_token:
            return Response({'error': 'Invalid Authorization header'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Attempt to refresh the refresh token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # Set the new access token in the response cookies
            response = JsonResponse({'message': 'Token refreshed succesfully'})
            response.set_cookie('access_token', access_token, samesite='None', secure=True)
            return response
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        