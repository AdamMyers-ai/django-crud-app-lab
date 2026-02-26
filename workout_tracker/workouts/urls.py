from django.urls import path
from . import views

urlpatterns = [
    # auth
    path("", views.Home.as_view(), name="home"),
    # workouts
    path("accounts/signup/", views.SignUp.as_view(), name="signup"),
    path("workouts/", views.WorkoutList.as_view(), name="workouts_index"),
]
