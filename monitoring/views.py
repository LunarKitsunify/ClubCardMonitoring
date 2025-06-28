from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from .models import CardStats
from django.shortcuts import render
from django.db import transaction
import json

def real_ip_key(group, request):
    return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))

def index_view(request):
    return render(request, 'index.html')

def card_stats_api(request):
    data = list(CardStats.objects.values())
    return JsonResponse(data, safe=False)

@ratelimit(key=real_ip_key, method='POST', rate='1/60s', block=True)
@csrf_exempt
def upload_card_stats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            for card in data:
                name = card.get('name')
                card_id = card.get('id')
                score = float(card.get('score', 0))
                win = bool(card.get('win', False))

                with transaction.atomic():
                    obj, created = CardStats.objects.select_for_update().get_or_create(name=name)

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

