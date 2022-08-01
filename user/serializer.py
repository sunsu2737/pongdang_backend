from email.policy import default
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(default='')
    profile_image = serializers.CharField(default='default_image.png')
    name = serializers.CharField(default='')
    birth = serializers.CharField(default='')
    region = serializers.CharField(default='')