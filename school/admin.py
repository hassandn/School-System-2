from django.contrib import admin
from .models import School, Course, Class

admin.site.register([School, Course, Class])
