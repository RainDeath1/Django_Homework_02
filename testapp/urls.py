from django.urls import path

from testapp.views import AddSms, ReadSms, SmsList, DeleteSms, UpdateSms

app_name = 'testapp'

urlpatterns = [
    path('addsms/', AddSms.as_view(), name='add_sms'),
    path('readsms/<int:pk>/', ReadSms.as_view(), name='read_sms'),
    path('smslist/', SmsList.as_view(), name='sms_list'),
    path('deletesms/<int:pk>/', DeleteSms.as_view(), name='delete_sms'),
    path('updatesms/<int:pk>/', UpdateSms.as_view(), name="update_sms"),
]
