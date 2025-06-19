from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return self.date >= timezone.now()

    def registration_count(self):
        return self.registration_set.count()


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        unique_together = ('event', 'email')  # Validation: only 1 registration per email per event

    def __str__(self):
        return f"{self.name} - {self.event.title}"
