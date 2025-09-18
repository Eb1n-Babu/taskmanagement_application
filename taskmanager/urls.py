from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from taskmanager.views import (
    # API
    login_view, TaskListView, TaskUpdateView, TaskReportView,
    # Web
    admin_login_view, admin_logout_view, admin_dashboard, user_list, create_user,
    edit_user_role, delete_user, admin_list, task_list, create_task, task_detail,
    update_task , Home
)

urlpatterns = [
    path('',Home,name='welcome'),
    # API
    path('api/auth/login/', login_view, name='api_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:id>/', TaskUpdateView.as_view(), name='task-update'),
    path('api/tasks/<int:id>/report/', TaskReportView.as_view(), name='task-report'),
    # Admin Panel
    path('admin-panel/login/', admin_login_view, name='admin_login'),#admin_login_view
    path('admin-panel/logout/', admin_logout_view, name='admin_logout'),#admin_logout_view
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),#admin_dashboard
    path('admin-panel/users/', user_list, name='user_list'),#user_list
    path('admin-panel/users/create/', create_user, name='create_user'),#create_user
    path('admin-panel/users/<int:pk>/edit-role/', edit_user_role, name='edit_user'),#edit_user_role
    path('admin-panel/users/<int:pk>/delete/', delete_user, name='delete_user'),#delete_user
    path('admin-panel/admins/', admin_list, name='admin_list'),#admin_list
    path('admin-panel/tasks/', task_list, name='task_list'),#task_list
    path('admin-panel/tasks/create/', create_task, name='create_task'),#create_task
    path('admin-panel/tasks/<int:pk>/', task_detail, name='task_detail'),#task_detail
    path('admin-panel/tasks/<int:pk>/update/', update_task, name='update_task'),#update_task
]