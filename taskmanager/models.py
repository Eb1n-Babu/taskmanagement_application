#from django.db import models
# Create your models here.

from django.db import models
from django.contrib.auth.models import User, Group


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"


from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'taskmanager':
        Group.objects.get_or_create(name='SuperAdmin')
        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='User')