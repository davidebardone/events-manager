from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=250)
    desc = models.CharField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.name} - Attendee: {self.attendee.first_name} {self.attendee.last_name}"