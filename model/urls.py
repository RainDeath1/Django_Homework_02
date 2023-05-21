from django.urls import path
from .views import (
    IceCreamListView,
    IceCreamDetailView,
    IceCreamCreateView,
    IceCreamUpdateView,
    IceCreamDeleteView,
)

urlpatterns = [
    path('', IceCreamListView.as_view(), name='home'),
    path('icecream_list/', IceCreamListView.as_view(), name='icecream_list'),
    path('icecream_detail/<int:ice_cream_id>/', IceCreamDetailView.as_view(), name='icecream_detail'),
    path('icecream_new/', IceCreamCreateView.as_view(), name='icecream_new'),
    path('icecream_edit/<int:ice_cream_id>/', IceCreamUpdateView.as_view(), name='icecream_edit'),
    path('icecream_delete/<int:ice_cream_id>/', IceCreamDeleteView.as_view(), name='icecream_delete'),
]
