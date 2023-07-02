from django.urls import path, re_path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, comprehension
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
app_name = 'tasks'

urlpatterns = [
    re_path('^$', TaskListView.as_view(), name='task-list'),
    re_path('^create/$', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('compr/', comprehension, name='comprehension'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='tasks:task-list'), name='logout'),
]

