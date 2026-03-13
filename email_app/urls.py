from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('archive/', views.archive, name='archive'),
    path('trash/', views.trash, name='trash'),
    path('email/<int:pk>/', views.detail, name='detail'),
    path('compose/', views.compose, name='compose'),
    path('move/<int:pk>/', views.move, name='move'),
    path('delete/<int:pk>/', views.delete_permanent, name='delete_permanent'),
]