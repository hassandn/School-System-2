from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

class UserManager:
    def __init__(self, username, password, first_name, last_name, national_id, email, group_names):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.email = email
        self.group_names = group_names
        
    def create_user(self):
        try:
            user = get_user_model().objects.create_user(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                national_id=self.national_id,
                registration_status='pending',
                email=self.email,
            )
            user.set_password(self.password)
            for user_group in self.group_names:
                group = Group.objects.get(name=str(user_group))
                # group = Group.objects.get(name=str(self.group_names))
                group.user_set.add(user)
            
            user.save() 
            return user
        except Group.DoesNotExist:
            raise ValidationError(f"Group '{self.group_names}' does not exist.")
        except Exception as e:
            raise ValidationError(f"Error creating user: {str(e)}")
        
    def update_user(self):
        try:
            get_user_model().objects.update(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                location=self.location,
                email=self.email,
            )
        except Exception as e:
            pass
        
    @classmethod
    def user_list(Cls):
        get_user_model().objects.all()
            
             
