from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class UserCreationFormExtended(UserCreationForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'groups': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        if status == 'completed':
            report = cleaned_data.get('completion_report')
            hours = cleaned_data.get('worked_hours')
            if not report or not hours or hours <= 0:
                raise forms.ValidationError("Completion requires report and positive hours.")
        return cleaned_data