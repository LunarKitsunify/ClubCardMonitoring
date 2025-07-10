from django.urls import path
from .views import card_stats_json

from .views import (
    upload_card_stats,
    card_stats_api,
)

urlpatterns = [
    path('upload-cardstats/', upload_card_stats),
    path('cardstats/', card_stats_json, name="card_stats_json"),
]