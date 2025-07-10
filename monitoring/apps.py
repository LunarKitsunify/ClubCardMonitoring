from django.apps import AppConfig
import os
from django.conf import settings


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'


    def ready(self):
        from monitoring.utils.export_stats import export_cardstats_to_json

        path = os.path.join(settings.BASE_DIR, "static", "stats.json")
        if not os.path.exists(path):
            try:
                export_cardstats_to_json()
                print("✅ stats.json created.")
            except Exception as e:
                print(f"⚠️ Error when stats.json: {e}")