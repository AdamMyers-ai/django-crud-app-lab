from django.contrib import admin
from .models import Workout, ExerciseEntry, Tag

# Register your models here.
admin.site.register(Workout)
admin.site.register(ExerciseEntry)
admin.site.register(Tag)
