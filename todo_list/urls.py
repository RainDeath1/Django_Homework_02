from django.urls import path, re_path

from . import views
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, comprehension, \
    UserListView, UserDetailView, UserRedirectView, TaskArchiveIndexView, IceCreamListView, product_create_view
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
    path('users/', UserListView.as_view(), name='users'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('user/redirect/', UserRedirectView.as_view(), name='user_redirect'),
    path('tasks/archive/', TaskArchiveIndexView.as_view(), name='task_archive'),
    path('create_icecream/', views.create_icecream, name='create_icecream'),
    path('icecream_list/', IceCreamListView.as_view(), name='icecream_list'),
    #26
    path('create_product/', product_create_view, name='products:create_product')
]

