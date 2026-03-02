from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tags_detail", kwargs={"tag_id": self.id})


class Workout(models.Model):
    MOOD_CHOICES = [
        ("terrible", "Terrible"),
        ("bad", "Bad"),
        ("ok", "Ok"),
        ("good", "Good"),
        ("great", "Great"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)

    program_name = models.CharField(max_length=100, blank=True)

    duration_minutes = models.PositiveIntegerField(default=0)
    bodyweight = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True
    )
    sleep_hours = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, blank=True)

    is_pr = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})"

    def get_absolute_url(self):
        return reverse("workouts_detail", kwargs={"workout_id": self.id})


class ExerciseEntry(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="entries"
    )
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rpe = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}: {self.sets}x{self.reps} @ {self.weight}"

    def get_absolute_url(self):
        return reverse("workouts_detail", kwargs={"workout_id": self.workout_id})
