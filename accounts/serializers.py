from traceback import print_tb

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.fields import return_None
from rest_framework import serializers
from .helpers import UserManager
import re


class UserSerializer(serializers.ModelSerializer):
    """serilizer for validate show and create user"""
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'national_id','first_name', 'last_name', 'groups']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = UserManager(validated_data['username'], validated_data['password'], validated_data['first_name'], validated_data['last_name'], validated_data['national_id'], validated_data['email'] , validated_data['groups'])
        user = user.create_user()
        return user

    def validate_national_id(self, value):
        if any(char.isalpha() for char in value):  # check if national id has characters
            raise serializers.ValidationError("National ID must contain only digits.")
        return value

    def validate_password(self, value):# check if the password is strong enough
        if len(value) < 8:  # check if the password is strong enough
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        if not any(char.isdigit() for char in value):  # check if the password contains at least one digit
            raise serializers.ValidationError("Password must contain at least one digit.")

        if not any(char.isupper() for char in value):  # check if the password contains at least one uppsercase Letter
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):  # check if the password contains at least one characters
            raise serializers.ValidationError("Password must contain at least one special character.")

        if 'username' in self.initial_data:
            if self.initial_data['username'].lower() in value.lower():  # check if the password not have username in it
                raise serializers.ValidationError("Password must not contain username.")
        else:
            raise serializers.ValidationError("you didn't fill usename")

        if 'email' in self.initial_data:
            if self.initial_data['email'].lower().split('@')[0] in value.lower():  # check if the password not have email in it
                raise serializers.ValidationError("Password must not contain email.")
        else:
            raise serializers.ValidationError("you didn't fill email")

        if 'national_id' in self.initial_data:
            if self.initial_data['national_id'].lower() in value.lower():  # check if the password contains national id
                raise serializers.ValidationError("password must not contain national id.")
        else:
            raise serializers.ValidationError("you didn't fill national id")
        return value

    def to_representation(self, instance):
        return UserManager.to_representation(user=super().to_representation(instance))
    
    
class UserDetailSerializer(serializers.ModelSerializer):
    """serilizer for user detail view"""
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'national_id', 'first_name', 'last_name', 'groups', 'biography', 'location', 'registration_status', 'date_joined', 'last_login']

    def to_representation(self, instance):
        return UserManager.to_representation(user=super().to_representation(instance))   


class UserUpdateSerializer(serializers.ModelSerializer):
    """serilizer for updting users"""
    class Meta:
        model = get_user_model()
        exclude = ['password', 'registration_status', 'user_permissions','is_staff', 'is_active', 'is_superuser', 'id', 'last_login', 'date_joined']
        
    def to_representation(self, instance):
        user = super().to_representation(instance)
        user['groups']=UserManager.get_groups_name(user)
        return user
        
    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)  
        instance = super().update(instance, validated_data) 
        if groups is not None:
            instance.groups.set(groups)  
        instance.save()
        return instance
        