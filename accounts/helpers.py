from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()
def create_user(username, password, first_name, last_name, national_id, email, group_name):
    try:
        print(password)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            national_id=national_id,
            registration_status=False,
            email=email,
        )
        user.set_password(password)
        group = Group.objects.get(name=str(group_name))
        group.user_set.add(user)
        user.save() 
        return user
    except group.DoesNotExist:
        raise ValidationError(f"Group '{group_name}' does not exist.")
    except Exception as e:
        raise ValidationError(f"Error creating user: {str(e)}")