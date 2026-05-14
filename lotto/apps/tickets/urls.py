from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/', views.buy_ticket, name='buy'),
    path('my/', views.my_tickets, name='my_tickets'),
]
