from django.contrib import admin
from .models import School, Course, Class, Exercise, ExerciseAnswer, Announcement

admin.site.register([School, Course, Class, Exercise, ExerciseAnswer, Announcement])
