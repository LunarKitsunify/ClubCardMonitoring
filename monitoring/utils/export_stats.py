import os
import json
from django.conf import settings
from monitoring.models import CardStats

def export_cardstats_to_json():
    stats = list(CardStats.objects.all().values(
        "name", "card_id", "games", "wins",
        "played_games", "played_wins",
        "seen_games", "seen_wins",
        "score", "impact"
    ))

    for card in stats:
        card["winrate"] = round(card["wins"] / card["games"], 4) if card["games"] else 0
        card["played_wr"] = round(card["played_wins"] / card["played_games"], 4) if card["played_games"] else 0
        card["seen_wr"] = round(card["seen_wins"] / card["seen_games"], 4) if card["seen_games"] else 0

    output_path = os.path.join(settings.BASE_DIR, "static", "stats.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)