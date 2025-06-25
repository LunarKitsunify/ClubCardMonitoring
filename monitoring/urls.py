from django.urls import path
from .views import db_info
from .views import db_info, home
from .views import db_info, run_migrate

urlpatterns = [
    path('', home),
    path('db-check/', db_info),
    path('run-migrate/', run_migrate),
]
