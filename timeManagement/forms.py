from django import forms
from .models import TimeItem
from .models import TimeSpentItem

class NewTimeItemForm(forms.ModelForm):

    class Meta:
        model = TimeItem
        fields = ('title', 'description', 'estimated_hour',)


class EditTimeItemForm(forms.ModelForm):

    class Meta:
        model = TimeItem
        fields = ('title', 'description', 'estimated_hour', 'is_complete', 'spent_hour', 'percentage',)


class NewTimeSpentItemForm(forms.ModelForm):

    class Meta:
        model = TimeSpentItem
        fields = ('time_item', 'task_description', 'remained_hour', 'priority', 'created_date',)
    
    def __init__(self, user, *args, **kwargs):
        super(NewTimeSpentItemForm, self).__init__(*args, **kwargs)
        self.fields['time_item'].queryset = TimeItem.objects.filter(author=user, is_complete=False)


class EditTimeSpentItemForm(forms.ModelForm):

    class Meta:
        model = TimeSpentItem
        fields = ('completed_hour', 'remained_hour', 'priority', 'created_date',)