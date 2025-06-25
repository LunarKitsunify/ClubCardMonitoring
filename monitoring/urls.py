from django.urls import path
from .views import db_info
from .views import db_info, home

urlpatterns = [
    path('', home),
    path('db-check/', db_info),
]
