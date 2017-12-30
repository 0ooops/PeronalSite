from django.contrib import admin
from .models import TimeItem
from .models import TimeSpentItem

admin.site.register(TimeItem)
admin.site.register(TimeSpentItem)
