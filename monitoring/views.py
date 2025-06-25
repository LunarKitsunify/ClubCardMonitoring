from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.db import connection
from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from .models import CardStats
import json



def home(request):
    return HttpResponse("Welcome to ClubCard Monitoring!")

def db_info(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]
    return JsonResponse({"tables": tables})

def run_migrate(request):
    call_command('migrate')
    return JsonResponse({"status": "migrated"})

@csrf_exempt
def submit_stats(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        cards = data.get("cards", {})
        is_win = data.get("win", False)

        for name, card_data in cards.items():
            impact = float(card_data.get("impact", 0))

            obj, _ = CardStats.objects.get_or_create(name=name)
            obj.games += 1
            if is_win:
                obj.wins += 1
            obj.score += impact
            obj.save()

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def card_stats_api(request):
    data = list(CardStats.objects.values())
    return JsonResponse(data, safe=False)