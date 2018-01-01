from django.shortcuts import render, get_object_or_404, redirect
from .models import TimeItem, TimeSpentItem
from datetime import datetime, timedelta, time
from .forms import NewTimeSpentItemForm, EditTimeSpentItemForm, NewTimeItemForm, EditTimeItemForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())


@login_required(login_url='/login')
def all_items(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
    return render(request, 'timeManagement/all_items.html', {'items': format_percentage(items), 'current_user': current_user})

@login_required(login_url='/login')
def all_items_new(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    if request.method == "POST":
        form = NewTimeItemForm(request.POST)
        if form.is_valid():
            time_item = form.save(commit=False)
            time_item.author = request.user
            time_item.created_date = timezone.now()
            time_item.save()
            items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
            return redirect('../all_items', {'items': format_percentage(items), 'current_user': current_user})
    else:
        form = NewTimeItemForm()
    return render(request, 'timeManagement/all_items_new.html', {'form': form, 'current_user': current_user})

@login_required(login_url='/login')
def all_items_edit(request, pk):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    time_item = get_object_or_404(TimeItem, pk=pk)
    if request.method == "POST":
        form = EditTimeItemForm(request.POST, instance=time_item)
        if form.is_valid():
            time_item = form.save(commit=False)
            time_item.updated_date = timezone.now()
            if time_item.is_complete:
                time_item.percentage = 1.0
            else:
                time_item.percentage = time_item.spent_hour / time_item.estimated_hour        
            time_item.save()
            items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
            return redirect('../../all_items', {'items': format_percentage(items), 'current_user': current_user})
    else:
        form = EditTimeItemForm(instance=time_item)
    return render(request, 'timeManagement/all_items_edit.html', {'form': form, 'current_user': current_user})

@login_required(login_url='/login')
def today_items(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
    today_items = TimeSpentItem.objects.filter(created_date__lte=today_end, created_date__gte=today_start, author=request.user).order_by('priority')
    return render(request, 'timeManagement/today_items.html', 
    {'today_items': today_items, 'items': format_percentage(items), 'chart': format_chart(today_items), 'current_user': current_user})

@login_required(login_url='/login')
def today_items_new(request):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    if request.method == "POST":
        form = NewTimeSpentItemForm(request.POST)
        if form.is_valid():
            time_spent_item = form.save(commit=False)
            time_spent_item.author = request.user
            time_spent_item.created_date = timezone.now()
            time_spent_item.save()
            items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
            today_items = TimeSpentItem.objects.filter(created_date__lte=today_end, created_date__gte=today_start, author=request.user).order_by('priority')
            return redirect('../today_items', {'today_items': today_items, 'items': format_percentage(items), 'current_user': current_user})
    else:
        form = NewTimeSpentItemForm()
    return render(request, 'timeManagement/today_items_new.html', {'form': form, 'current_user': current_user})

@login_required(login_url='/login')
def today_items_edit(request, pk):
    current_user = "Visitor"
    if request.user.is_authenticated:
        current_user = request.user
    today_item = get_object_or_404(TimeSpentItem, pk=pk)
    if request.method == "POST":
        form = EditTimeSpentItemForm(request.POST, instance=today_item)
        if form.is_valid():
            today_item = form.save(commit=False)
            today_item.updated_date = timezone.now()
            today_item.save()

            # update the main item each time completed a daily item
            if today_item.remained_hour <= 0:
                time_item = today_item.time_item
                time_item.update(today_item.completed_hour)

            items = TimeItem.objects.filter(author=request.user).order_by('-percentage')
            today_items = TimeSpentItem.objects.filter(created_date__lte=today_end, created_date__gte=today_start, author=request.user).order_by('priority')
            return redirect('../../today_items', {'today_items': today_items, 'items': format_percentage(items), 'current_user': current_user})
    else:
        form = EditTimeSpentItemForm(instance=today_item)
    return render(request, 'timeManagement/today_items_edit.html', {'form': form, 'current_user': current_user})

def format_percentage(items):
    for item in items:
        item.percentage = '{:.2%}'.format(item.percentage)
    return items

def format_chart(today_items):
    chart_data = []
    for today_item in today_items:
        pair = [today_item.time_item.title, today_item.completed_hour]
        chart_data.append(pair)
    return chart_data