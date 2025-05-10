from django.contrib import admin
from .models import School, Course, Class, Exercise

admin.site.register([School, Course, Class, Exercise])
