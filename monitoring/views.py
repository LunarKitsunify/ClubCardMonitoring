from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.db import connection
from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from .models import CardStats
from django.shortcuts import render
import json

def index_view(request):
    return render(request, 'index.html')

def card_stats_api(request):
    data = list(CardStats.objects.values())
    return JsonResponse(data, safe=False)

@csrf_exempt
def upload_card_stats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            for card in data:
                card_id = card.get('id')
                name = card.get('name')
                score = float(card.get('score', 0))
                win = bool(card.get('win', False))

                obj, created = CardStats.objects.get_or_create(name=name)

                obj.games += 1
                if win:
                    obj.wins += 1
                obj.score += score
                obj.card_id = card_id
                obj.impact = obj.score / obj.games if obj.games > 0 else 0
                obj.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)
