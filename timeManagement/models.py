from django.db import models
from django.utils import timezone


class TimeItem(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    estimated_hour = models.FloatField()
    spent_hour = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)

    def update(self, add_hour):
        self.spent_hour = self.spent_hour + add_hour
        self.percentage = self.spent_hour / self.estimated_hour
        self.updated_date = timezone.now()
        self.save()

    def complete(self):
        self.is_complete = True
        self.percentage = 1.0
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title