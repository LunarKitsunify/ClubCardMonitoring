import os
import json
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.conf import settings

PROCESSING_FILE = os.path.join(settings.BASE_DIR, "static", "processing_meta.json")
PROCESS_INTERVAL = timedelta(hours=3)
# PROCESS_INTERVAL = timedelta(minutes=5)

def read_next_processing_time():
    if not os.path.exists(PROCESSING_FILE):
        return None

    try:
        with open(PROCESSING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            value = data.get("next_processing_at")
            if value:
                return datetime.fromisoformat(value)
    except Exception:
        return None

    return None

def write_next_processing_time():
    next_time = now() + PROCESS_INTERVAL
    data = {
        "next_processing_at": next_time.isoformat()
    }

    with open(PROCESSING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[LOG] Writing next processing time to {PROCESSING_FILE}: {data['next_processing_at']}")

    return next_time

def is_processing_due():
    next_time = read_next_processing_time()
    now_time = now()
    due = not next_time or now_time >= next_time

    if due:
        print(f"[LOG] Processing check — Is due: True")
    else:
        delta = next_time - now_time
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"[LOG] Processing check — Is due: False (next in {hours:02}:{minutes:02}:{seconds:02})")

    return due