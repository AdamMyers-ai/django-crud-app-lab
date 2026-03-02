from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Workout, ExerciseEntry, Tag
from .forms import ExerciseEntryForm, SignUpForm, TagForm


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


@login_required
def workouts_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    entry_form = ExerciseEntryForm()

    available_tags = Tag.objects.filter(user=request.user).exclude(
        id__in=workout.tags.all().values_list("id", flat=True)
    )

    return render(
        request,
        "workouts/detail.html",
        {
            "workout": workout,
            "entry_form": entry_form,
            "available_tags": available_tags,
        },
    )


class WorkoutCreate(LoginRequiredMixin, CreateView):
    model = Workout
    fields = [
        "date",
        "title",
        "program_name",
        "duration_minutes",
        "bodyweight",
        "sleep_hours",
        "mood",
        "is_pr",
        "notes",
    ]
    template_name = "workouts/form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdate(LoginRequiredMixin, UpdateView):
    model = Workout
    fields = [
        "date",
        "title",
        "program_name",
        "duration_minutes",
        "bodyweight",
        "sleep_hours",
        "mood",
        "is_pr",
        "notes",
        "tags",
    ]
    template_name = "workouts/form.html"

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["tags"].queryset = Tag.objects.filter(user=self.request.user)
        return form


class WorkoutDelete(LoginRequiredMixin, DeleteView):
    model = Workout
    success_url = "/workouts/"
    template_name = "workouts/confirm_delete.html"

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class EntryCreate(LoginRequiredMixin, CreateView):
    model = ExerciseEntry
    form_class = ExerciseEntryForm
    template_name = "entries/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.workout = get_object_or_404(
            Workout, id=kwargs["workout_id"], user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.workout = self.workout
        return super().form_valid(form)

    def get_success_url(self):
        return self.workout.get_absolute_url()


class EntryUpdate(LoginRequiredMixin, UpdateView):
    model = ExerciseEntry
    form_class = ExerciseEntryForm
    template_name = "entries/form.html"

    def get_queryset(self):
        # only allow editing entries that belong to the user's workouts
        return ExerciseEntry.objects.filter(workout__user=self.request.user)

    def get_success_url(self):
        return self.object.workout.get_absolute_url()


class EntryDelete(LoginRequiredMixin, DeleteView):
    model = ExerciseEntry
    template_name = "entries/confirm_delete.html"

    def get_queryset(self):
        return ExerciseEntry.objects.filter(workout__user=self.request.user)

    def get_success_url(self):
        return self.object.workout.get_absolute_url()


class TagList(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tags/index.html"
    context_object_name = "tags"
    ordering = ["name"]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by("name")


@login_required
def tags_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    return render(request, "tags/detail.html", {"tag": tag})


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/form.html"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = "/tags/"
    template_name = "tags/confirm_delete.html"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


@login_required
@require_POST
def assoc_tag(request, workout_id, tag_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    workout.tags.add(tag)
    return redirect("workouts_detail", workout_id=workout_id)


@login_required
@require_POST
def unassoc_tag(request, workout_id, tag_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    workout.tags.remove(tag)
    return redirect("workouts_detail", workout_id=workout_id)
