from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


# Serializer class for register user
class CreateUserSerializer(serializers.ModelSerializer):
    # serializing password field explicitly so that it will only be used for input
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'dob', 'mobile_number', 'address']

    # function to create a user using MyUser Model.
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            dob=validated_data["dob"],
            mobile_number=validated_data["mobile_number"],
            address=validated_data["address"],
        )
        return user


# Serializer class for Login User
class LoginUserSerializer(serializers.Serializer):

    """extracting email and password fields explicitly bcz serializer needs to
    perform validation and authentication based on these fields.
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})


    """This function checks if the provided credentials are valid and returns 
    a user object if authentication is successful."""
    def validate(self, data):
        #data parameter refers to the dictionary that contains the input data being
        email = data.get("email")
        password = data.get("password")

        if email and password:
            # using the authenticate() method from django.contrib.auth
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email and password')
        else:
            raise serializers.ValidationError('Must have both an email and a password.')

        # Finally, the validated user object is added to the data dictionary and returned.
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User Model - defined to GET all the users present in the database.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'dob', 'mobile_number', 'address']

        
