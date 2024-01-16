
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name = 'home'),
    path('refresh_data/', views.refresh_data, name='refresh_data'),
]
