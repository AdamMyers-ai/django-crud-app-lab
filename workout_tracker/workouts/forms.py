from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ExerciseEntry


class ExerciseEntryForm(forms.ModelForm):
    class Meta:
        model = ExerciseEntry
        fields = ["name", "sets", "reps", "weight", "rpe", "notes"]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
