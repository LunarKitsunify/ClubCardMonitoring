from django.urls import path

from .views import (
    upload_card_stats,
    card_stats_api,
)

urlpatterns = [
    path('upload-cardstats/', upload_card_stats),
    path('cardstats/', card_stats_api),
]
