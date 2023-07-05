from django.urls import path, re_path

vals = {
    'name': 'by_index',
    'beaver': 'beaver – это бобёр!'
}

# app_name = 'bboard'

# urlpatterns = [
#     re_path(r'^$', index, name='index'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, vals, name='by_rubric'),
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
# ]

from django.urls import path
from .views import IndexView, ByRubricView, DetailView, BbCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:rubric_id>/', ByRubricView.as_view(), name='by_rubric'),
    path('read/<int:pk>/', DetailView.as_view(), name='read'),
    path('add/', BbCreateView.as_view(), name='add'),
]

