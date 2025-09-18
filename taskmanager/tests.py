from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task = Task.objects.create(
            title='Test Task', description='Desc', assigned_to=self.user,
            due_date='2025-10-01', status='pending'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.status, 'pending')

    def test_completion_fields_blank(self):
        self.assertIsNone(self.task.completion_report)
        self.assertIsNone(self.task.worked_hours)


class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.task = Task.objects.create(
            title='Test', description='Desc', assigned_to=self.user,
            due_date='2025-10-01', status='pending'
        )

    def test_valid_completion(self):
        data = {'status': 'completed', 'completion_report': 'Done', 'worked_hours': 5.0}
        serializer = TaskSerializer(self.task, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

    def test_invalid_completion(self):
        data = {'status': 'completed', 'completion_report': '', 'worked_hours': 0}
        serializer = TaskSerializer(self.task, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('completion_report', serializer.errors)


class TaskAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Ensure groups exist
        self.user_group, _ = Group.objects.get_or_create(name='User')
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.superadmin_group, _ = Group.objects.get_or_create(name='SuperAdmin')

        self.user = User.objects.create_user(username='user', password='pass')
        self.user.groups.add(self.user_group)
        self.admin = User.objects.create_user(username='admin', password='pass')
        self.admin.groups.add(self.admin_group)
        self.task = Task.objects.create(
            title='API Task', description='Desc', assigned_to=self.user,
            due_date='2025-10-01', status='pending'
        )

    def test_login(self):
        response = self.client.post('/api/auth/login/', {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_tasks(self):
        # Get token
        login_resp = self.client.post('/api/auth/login/', {'username': 'user', 'password': 'pass'}, format='json')
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_completed(self):
        login_resp = self.client.post('/api/auth/login/', {'username': 'user', 'password': 'pass'}, format='json')
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {'status': 'completed', 'completion_report': 'Done', 'worked_hours': 3.0}
        response = self.client.put(f'/api/tasks/{self.task.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_report_view_admin_only(self):
        # First complete task
        self.task.status = 'completed'
        self.task.completion_report = 'Test'
        self.task.worked_hours = 3.0
        self.task.save()
        # Admin login
        login_resp = self.client.post('/api/auth/login/', {'username': 'admin', 'password': 'pass'}, format='json')
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(f'/api/tasks/{self.task.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminPanelTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure groups
        self.superadmin_group, _ = Group.objects.get_or_create(name='SuperAdmin')
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.user_group, _ = Group.objects.get_or_create(name='User')

        self.superadmin = User.objects.create_user(username='super', password='pass')
        self.superadmin.groups.add(self.superadmin_group)
        self.admin = User.objects.create_user(username='admin', password='pass')
        self.admin.groups.add(self.admin_group)
        self.client.force_login(self.superadmin)

    def test_user_list_superadmin(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/users/list.html')

    def test_create_user(self):
        # Force login (already done in setUp)
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'newpass',
            'password2': 'newpass',
            'role': self.user_group.id
        }
        # Fetch CSRF token
        response = self.client.get(reverse('create_user'))
        csrftoken = response.cookies.get('csrftoken').value
        data['csrfmiddlewaretoken'] = csrftoken
        # Post
        response = self.client.post(reverse('create_user'), data, follow=True)
        self.assertEqual(response.status_code, 200)  # Follow redirects to 200
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_task_list_admin(self):
        self.client.logout()
        self.client.force_login(self.admin)
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)