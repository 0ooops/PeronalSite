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


class TimeSpentItem(models.Model):
    author = models.ForeignKey('auth.User')
    time_item = models.ForeignKey(TimeItem)
    task_description = models.CharField(max_length=200)
    remained_hour = models.FloatField()
    completed_hour = models.FloatField(default=0.0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=7)

    def update(self, add_hour):
        self.completed_hour = self.completed_hour + add_hour
        if self.remained_hour < add_hour:
            self.remained_hour = 0
        else:
            self.remained_hour = self.remained_hour - add_hour
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.time_item) + ": " + str(self.task_description)