from django.urls import path
from . import views

app_name = 'ctp'

urlpatterns = [
    path('', views.ctp_list, name='list'),
    path('create/', views.ctp_create, name='create'),
    path('<int:pk>/edit/', views.ctp_edit, name='edit'),
]
