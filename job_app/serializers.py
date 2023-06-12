from rest_framework import serializers
from .models import User,Job,Bookmark
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['timestamps']
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['updated_at']
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = ['updated_at']
# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
    




