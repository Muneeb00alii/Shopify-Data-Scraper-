from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cancel_download/', views.cancel_download, name='cancel_download'),
]
