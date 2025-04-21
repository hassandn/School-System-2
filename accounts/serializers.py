from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model 
from .helpers import UserManager
import re


def check_password_strength(data):#check if the password is strong enough
    
        if len(data['password']) < 8:#check if the password is strong enough
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isdigit() for char in data['password']):#check if the password contains at least one digit 
            raise serializers.ValidationError("Password must contain at least one digit.")     
        
        if not any(char.isupper() for char in data['password']):#check if the password contains at least one uppsercase Letter
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",data['password']):#check if the password contains at least one characters
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        if data['username'].lower() in data['password'].lower():#check if the password not have username in it
            raise serializers.ValidationError("Password must not contain username.")
        
        if data['email'].lower().split('@')[0] in data['password'].lower():#check if the password not have email in it
            raise serializers.ValidationError("Password must not contain email.")
        
        if data['national_id'].lower() in data['password'].lower():#check if the password contains national id
            raise serializers.ValidarionError("password must not contain national id.")
      
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'national_id','first_name', 'last_name', 'groups']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        print(validated_data['groups'])
        user = UserManager(validated_data['username'], validated_data['password'], validated_data['first_name'], validated_data['last_name'], validated_data['national_id'], validated_data['email'] , validated_data['groups'])
        user = user.create_user()
        return user
    
    def validate(self, data):
        
        if get_user_model().objects.filter(username=data['username']).exists():#check if the username is already taken
            raise serializers.ValidationError("Username already exists.")
        
        if get_user_model().objects.filter(email=data['email']).exists():#check if the email is already taken
            raise serializers.ValidationError("Email already exists.")
        check_password_strength(data)
        
        if any(char.isalpha() for char in data['national_id']):#check if national id has characters
            raise serializers.ValidationError("National ID must contain only digits.")
        return data