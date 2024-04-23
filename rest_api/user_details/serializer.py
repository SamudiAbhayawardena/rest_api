from rest_framework import serializers
from .models import UserDetails


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDetails
        fields = ['user_res', 'name', 'profile', 'birthday', 'gender', 'height', 'weight', 'diabetics_score', 'veg_status']
