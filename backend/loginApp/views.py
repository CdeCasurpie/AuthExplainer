from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


# loginApp views

class Login(APIView):
    def post(self, request):
        try:
            password = request.data['password']
            username = request.data['username']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing username or password'})
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                serializer = UserSerializer(user)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'user': serializer.data, 'access_token': access_token}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Incorrect password'})
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'User does not exist'})
        
class Register(APIView):
    def post(self, request):
        try:
            password = request.data['password']
            username = request.data['username']
            email = request.data['email']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing username, password or email'})
        try:
            user = User.objects.get(username=username)
            return Response(status=status.HTTP_409_CONFLICT, data={'error': 'User already exists'})
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
                return Response(status=status.HTTP_409_CONFLICT, data={'error': 'Email already in use'})
            except User.DoesNotExist:
                serializer = UserSerializer(data={
                    'username': username,
                    'email': email,
                    'password' : make_password(password)
                })

                if serializer.is_valid():
                    serializer.save()
                    user = serializer.instance
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({'user': serializer.data, 'access_token': access_token}, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)