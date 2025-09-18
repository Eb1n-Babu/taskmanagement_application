from django import forms
from django.contrib.auth.models import User, Group
from .models import Task

class UserCreationFormExtended(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, empty_label="Select Role")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        if self.cleaned_data.get('role'):
            user.groups.add(self.cleaned_data['role'])
        return user

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