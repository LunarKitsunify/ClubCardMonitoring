from django.db import models
from django.utils.timezone import now

class CardStats(models.Model):
    name = models.CharField(max_length=255, unique=True)
    card_id = models.IntegerField(null=True, blank=True)
    games = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0.0)
    impact = models.FloatField(default=0.0)

    played_games = models.PositiveIntegerField(default=0)
    played_wins = models.PositiveIntegerField(default=0)

    seen_games = models.PositiveIntegerField(default=0)
    seen_wins = models.PositiveIntegerField(default=0) 

    last_updated = models.DateTimeField(auto_now=True)

    @property
    def played_winrate(self):
        return self.played_wins / self.played_games if self.played_games > 0 else None

    @property
    def seen_winrate(self):
        return self.seen_wins / self.seen_games if self.seen_games > 0 else None

    def __str__(self):
        return self.name
    
class CardStatsLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)  # referrer or User-Agent
    raw_payload = models.JSONField()

    def __str__(self):
        return f"Match log from {self.ip_address or 'unknown'} at {self.timestamp}"