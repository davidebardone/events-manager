from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=250)
    desc = models.CharField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name