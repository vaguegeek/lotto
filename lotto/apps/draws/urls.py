from django.urls import path
from . import views

app_name = 'draws'

urlpatterns = [
    path('', views.draw_list, name='list'),
    path('<int:round_number>/', views.draw_detail, name='detail'),
    path('admin/draw/<int:round_number>/', views.do_draw, name='do_draw'),
]
