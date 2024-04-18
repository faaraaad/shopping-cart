from django.urls import path
from .views import CreateUserAPIView

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
]
