from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def validate_access_token(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return Response({"error": "Access token is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            secret_key = os.environ.get('SECRET_KEY')
            decoded_token = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            request.user_id = decoded_token.get('user_id')  # Store user ID in request for further processing
        except jwt.ExpiredSignatureError:
            return Response({"error": "Access token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid access token"}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(self, request, *args, **kwargs)

    return wrapped_view
