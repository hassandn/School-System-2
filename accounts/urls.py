from django.urls import path
from .views import StudentCreateView

urlpatterns = [
    path('create-student/', StudentCreateView.as_view(), name='student_create'),
    
]
