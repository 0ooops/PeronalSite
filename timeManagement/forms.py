from django import forms
from .models import TimeItem
from .models import TimeSpentItem

class NewTimeItemForm(forms.ModelForm):

    class Meta:
        model = TimeItem
        fields = ('author', 'title', 'description', 'estimated_hour',)


class EditTimeItemForm(forms.ModelForm):

    class Meta:
        model = TimeItem
        fields = ('author', 'title', 'description', 'estimated_hour', 'is_complete', 'spent_hour', 'percentage',)


class NewTimeSpentItemForm(forms.ModelForm):

    class Meta:
        model = TimeSpentItem
        fields = ('author', 'time_item', 'task_description', 'remained_hour', 'priority',)


class EditTimeSpentItemForm(forms.ModelForm):

    class Meta:
        model = TimeSpentItem
        fields = ('completed_hour', 'remained_hour', 'priority',)