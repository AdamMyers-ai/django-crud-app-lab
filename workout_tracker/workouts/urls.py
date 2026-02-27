from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("accounts/signup/", views.SignUp.as_view(), name="signup"),
    path("workouts/", views.WorkoutList.as_view(), name="workouts_index"),
    path("workouts/<int:workout_id>/", views.workouts_detail, name="workouts_detail"),
    path("workouts/create/", views.WorkoutCreate.as_view(), name="workouts_create"),
    path(
        "workouts/<int:pk>/update/",
        views.WorkoutUpdate.as_view(),
        name="workouts_update",
    ),
    path(
        "workouts/<int:pk>/delete/",
        views.WorkoutDelete.as_view(),
        name="workouts_delete",
    ),
    path(
        "workouts/<int:workout_id>/entries/create",
        views.EntryCreate.as_view(),
        name="entries_create",
    ),
    path(
        "entries/<int:pk>/update/", views.EntryUpdate.as_view(), name="entries_update"
    ),
    path(
        "entries/<int:pk>/delete/", views.EntryDelete.as_view(), name="entries_delete"
    ),
    path("tags/", views.TagList.as_view(), name="tags_index"),
    path("tags/<int:tag_id>/", views.tags_detail, name="tags_detail"),
    path("tags/create/", views.TagCreate.as_view(), name="tags_create"),
    path("tags/<int:pk>/update/", views.TagUpdate.as_view(), name="tags_update"),
    path("tags/<int:pk>/delete/", views.TagDelete.as_view(), name="tags_delete"),
    path(
        "workouts/<int:workout_id>/assoc_tag/<int:tag_id>/",
        views.assoc_tag,
        name="assoc_tag",
    ),
    path(
        "workouts/<int:workout_id>/unassoc_tag/<int:tag_id>/",
        views.unassoc_tag,
        name="unassoc_tag",
    ),
]
