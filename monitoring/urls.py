from django.urls import path
from .views import db_info
from .views import db_info, home
from .views import db_info, run_migrate
from .views import submit_stats
from .views import card_stats_api

urlpatterns = [
    path('', home),
    path('db-check/', db_info),
    path('run-migrate/', run_migrate),
    path("submit-stats/", submit_stats),
    path('cardstats/', card_stats_api),
]
