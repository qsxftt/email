from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('trash/', views.trash, name='trash'),
    path('archive', views.archive, name='archive'),
    path('email/<int:email_id>/', views.detail_email, name='detail_email'),
    path('send', views.send_email, name='send_email'),
    path('select', views.select_user, name='select_user'),
]