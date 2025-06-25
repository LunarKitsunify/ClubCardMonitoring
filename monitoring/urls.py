from django.urls import path
from .views import db_info

urlpatterns = [
    path('db-check/', db_info),
]
