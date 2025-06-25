from django.urls import path

from .views import (
    db_info,
    run_migrate,
    submit_stats,
    card_stats_api,
    upload_card_stats,
    index_view,
)

urlpatterns = [
    path('', index_view), # Главная страница (может быть HTML-заглушка или redirect)  
    path('db-check/', db_info),  # Проверка подключения к базе и просмотра таблиц
    path('run-migrate/', run_migrate),  # Тестовая ручка для принудительного выполнения миграций (если нет shell)
    path('submit-stats/', submit_stats),  # ✅ Сюда отправляются данные от аддона (impact, win и т.д.)
    path('cardstats/', card_stats_api),  # 🔍 GET-ручка — вывод всей статистики по картам (JSON)
    path('upload-cardstats/', upload_card_stats),   # POST
]
