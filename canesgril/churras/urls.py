from django.urls import path
from .views import churrasco

urlpatterns = [
    path('churrasco', churrasco, name='churrasco'),
]
