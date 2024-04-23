from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=['email', 'password']


    def validate(self, attrs):
        password = attrs.get('password', '')
        if password == "":
            raise serializers.ValidationError('passwords not matched')

        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data.get('email'),
            password = validated_data.get('password'),
        )
        
        return user
    
class LoginSerielizer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=60, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields = ['email', 'password', 'access_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('invalid data')
        access_token = RefreshToken.for_user(user=user)

        return {
            'email' : user.email,
            'id' : user.id,
            'access_token' : str(access_token.access_token),
        }