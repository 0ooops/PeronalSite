from django.shortcuts import render
from .models import TimeItem
from .models import TimeSpentItem
from datetime import datetime, timedelta, time


def all_items(request):
    items = TimeItem.objects.all().order_by('-percentage')
    return render(request, 'timeManagement/all_items.html', {'items': items})

def today_items(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    today_items = TimeSpentItem.objects.filter(created_date__lte=today_end, created_date__gte=today_start).order_by('priority')

    return render(request, 'timeManagement/today_items.html', {'today_items': today_items})