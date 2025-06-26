from django.db import models

class CardStats(models.Model):
    name = models.CharField(max_length=255, unique=True)
    card_id = models.IntegerField(null=True, blank=True)
    games = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0.0)
    impact = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name