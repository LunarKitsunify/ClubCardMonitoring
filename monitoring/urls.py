from django.urls import path

from .views import (
    upload_card_stats,
    card_stats_api,
)

urlpatterns = [
    path('upload-cardstats/', upload_card_stats),   # POST
    path('cardstats/', card_stats_api),  # 🔍 GET-ручка — вывод всей статистики по картам (JSON)
]
