import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render
from django.db import transaction
from .models import CardStats
from .models import CardStatsLog

def real_ip_key(group, request):
    return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))

# def real_ip_key(group, request):
#     ip_raw = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
#     return ip_raw.split(",")[0].strip() if ip_raw else None

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

            #=====log raw data
            ip_raw = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
            ip = ip_raw.split(",")[0].strip() if ip_raw else None

            source = request.META.get("HTTP_REFERER") or request.META.get("HTTP_USER_AGENT")
            CardStatsLog.objects.create(
                ip_address=ip,
                source=source,
                raw_payload=data
            )
            #=====

            for card in data:
                name = card.get('name')
                card_id = card.get('id')
                win = bool(card.get('win', False))
                raw_score = float(card.get('score', 0))
                score = raw_score if win else -raw_score
                played = raw_score == 1.0
                seen = raw_score >= 0.5

                with transaction.atomic():
                    obj, created = CardStats.objects.select_for_update().get_or_create(name=name)

                    obj.games += 1
                    if win:
                        obj.wins += 1
                    obj.score += score
                    obj.card_id = card_id
                    obj.impact = obj.score / obj.games if obj.games > 0 else 0

                    if played:
                        obj.played_games += 1
                        if win:
                            obj.played_wins += 1
                    elif seen:
                        obj.seen_games += 1
                        if win:
                            obj.seen_wins += 1
                    obj.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

