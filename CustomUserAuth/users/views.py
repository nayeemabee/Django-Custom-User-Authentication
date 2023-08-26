from django.shortcuts import render

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer

# Create your views here.

# API view register user
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


# API view Login user
class LoginUserAPIView(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)    
        if serializer.is_valid():
            # extract user frpm validated data then assign a token
            user = serializer.Validated_data['user']
            # assigning auth token for User. GET it already present or CREATE it not.
            token = Token.objects.get_or_create(user=user)

            # return Response({'token': token.key}, status=HTTP_200_OK)
            return Response({
                'id':user.pk,
                'name':user.name,
                'email': user.email,
                'token': token.key
            }, status=HTTP_200_OK)

        # if serializer is not valid 
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# API view Logout user
class LogoutUserAPIView(APIView):

    # checking if user has a token and is_authenticated
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        #deleting the user token from database for the current user.
        Token.objects.filter(user=user).delete()
        return Response({'details': 'Succesfully logged out.'})

# API endpoint that allows all the CRUD operation on User model but only for ADMIN.
class UserViewSet(viewsets.ModelViewSet):
    # checking IsAdminuUer, since operations are allowed only for admins
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
