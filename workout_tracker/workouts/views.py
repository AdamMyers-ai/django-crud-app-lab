from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Workout, ExerciseEntry, Tag
from .forms import ExerciseEntryForm, SignUpForm


class Home(TemplateView):
    template_name = "home.html"


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = "/workouts/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class WorkoutList(LoginRequiredMixin, ListView):
    model = Workout
    template_name = "workouts/index.html"
    context_object_name = "workouts"
    ordering = ["-date"]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by("-date")
