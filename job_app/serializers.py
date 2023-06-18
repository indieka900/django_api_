from rest_framework import serializers
from .models import User,Job,Bookmark
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password, check_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['timestamps']
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['created_at']
class BookmarkSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    class Meta:
        model = Bookmark
        exclude = ['updated_at']
# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    # def validate(self, data):
    #     username = data.get('username')
    #     password = data.get('password')

    #     # Retrieve the user from the database based on the username or email
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError('Invalid username')

    #     # Compare the entered password with the stored password
    #     if not check_password(password, user.password):
    #         raise serializers.ValidationError('Invalid password')

    #     # return data



