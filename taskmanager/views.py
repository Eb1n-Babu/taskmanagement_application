from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAdminOrSuperAdmin, IsTaskOwnerOrAdmin
from .forms import UserCreationFormExtended, UserRoleForm, TaskForm
from django.contrib.auth.models import User, Group

# API Views
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwnerOrAdmin]
    lookup_field = 'id'
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        # Force partial=True for PUT to allow updating only status/report/hours
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    lookup_field = 'id'
    queryset = Task.objects.filter(status='completed')

# Web Views for Admin Panel (unchanged)
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid login or insufficient permissions.')
    return render(request, 'admin_panel/login.html')

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

def superadmin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='SuperAdmin').exists():
            messages.error(request, 'SuperAdmin only.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            messages.error(request, 'Admin/SuperAdmin only.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

@login_required
@superadmin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin_panel/users/list.html', {'users': users})

@login_required
@superadmin_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreationFormExtended(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created.')
            return redirect('user_list')
    else:
        form = UserCreationFormExtended()
    return render(request, 'admin_panel/users/form.html', {'form': form})

@login_required
@superadmin_required
def edit_user_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            user.groups.clear()
            for group in form.cleaned_data['groups']:
                user.groups.add(group)
            user.save()
            messages.success(request, 'Role updated.')
            return redirect('user_list')
    else:
        form = UserRoleForm(instance=user)
    return render(request, 'admin_panel/users/role_form.html', {'form': form, 'user': user})

@login_required
@superadmin_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('user_list')
    return render(request, 'admin_panel/users/confirm_delete.html', {'user': user})

@login_required
@superadmin_required
def admin_list(request):
    admins = User.objects.filter(groups__name='Admin')
    return render(request, 'admin_panel/admins/list.html', {'admins': admins})

@login_required
@admin_required
def task_list(request):
    if request.user.groups.filter(name='SuperAdmin').exists():
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to__groups__name='User')
    return render(request, 'admin_panel/tasks/list.html', {'tasks': tasks})

@login_required
@admin_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Task created.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'admin_panel/tasks/form.html', {'form': form})

@login_required
@admin_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    report = task.completion_report if task.status == 'completed' else None
    hours = task.worked_hours if task.status == 'completed' else None
    return render(request, 'admin_panel/tasks/detail.html', {
        'task': task, 'report': report, 'hours': hours
    })

@login_required
@admin_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'admin_panel/tasks/form.html', {'form': form})