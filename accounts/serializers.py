from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .helpers import create_user
import re

User = get_user_model()
def check_password_strength(data):#cheks many conditions for the password to be strong

        # check if the password is strong enough
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        #check if the password contains at least one digit 
        if not any(char.isdigit() for char in data['password']):
            raise serializers.ValidationError("Password must contain at least one digit.")     
        #check if the password contains at least one uppsercase Letter
        if not any(char.isupper() for char in data['password']):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        #check if the password contains at least one characters
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",data['password']):
            raise serializers.ValidationError("Password must contain at least one special character.")
        #check if the password not have username in it
        if data['username'].lower() in data['password'].lower():
            raise serializers.ValidationError("Password must not contain username.")
        #check if the password not have email in it
        if data['email'].lower().split('@')[0] in data['password'].lower():
            raise serializers.ValidationError("Password must not contain email.")
      
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'national_id','first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = create_user(validated_data['username'], validated_data['password'], validated_data['first_name'], validated_data['last_name'], validated_data['national_id'], validated_data['email'] , 'Student')
        return user
    
    def validate(self, data):
        #check if the username is already taken
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        #check if the email is already taken
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        check_password_strength(data)
        #check if national id has characters
        if any(char.isalpha() for char in data['national_id']):
            raise serializers.ValidationError("National ID must contain only digits.")
        return data