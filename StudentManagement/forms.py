from django import forms
from .models import Task, Group, Student, Announcement
from django.forms.widgets import DateInput


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['taskName', 'completed']
        widgets = {
            'taskName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Name'}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupName', 'students']  # Allow selecting group name and students

    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), widget=forms.CheckboxSelectMultiple)  # List all students with checkboxes


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['announce', 'enddate', 'group']
        widgets = {
            'enddate': forms.TextInput(attrs={'class': 'datepicker'}),  # Custom class for JavaScript date picker
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        if teacher:
            self.fields['group'].queryset = Group.objects.filter(teacher=teacher)