from django.db import models
from django.core import validators


class Event(models.Model):
    name = models.CharField(max_length=250)
    desc = models.CharField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()
    max_capacity = models.IntegerField(
        default=1,
        validators=[
            validators.MinValueValidator(1)
        ]
    )
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        # registrations cannot be duplicated
        unique_together = (("event", "attendee"),)

    def __str__(self) -> str:
        return f"{self.event.name} - Attendee: {self.attendee.first_name} {self.attendee.last_name}"