import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django.utils import timezone
from django.shortcuts import render
from django.db import transaction
from .models import CardStats, CardStatsLog, ProcessingState


def real_ip_key(group, request):
    """
    Returns the IP address to be used as a rate-limiting key.
    Prioritizes X-Forwarded-For, falls back to REMOTE_ADDR.
    """
    # ip_raw = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
    # return ip_raw.split(",")[0].strip() if ip_raw else None
    return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))

def index_view(request):
    """
    Renders the default index.html template.
    """
    return render(request, 'index.html')

def card_stats_api(request):
    """
    Returns all card statistics as a JSON response.
    """
    data = list(CardStats.objects.values())
    return JsonResponse(data, safe=False)

@ratelimit(key=real_ip_key, method='POST', rate='1/60s', block=True)
@csrf_exempt
def upload_card_stats(request):
    """
    Accepts POST requests from clients containing card stats.
    Logs the payload to CardStatsLog and optionally triggers batch processing
    if thresholds are met (volume or time-based).
    """
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

            maybe_process_cardstats_logs();

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def process_cardstats_logs():
    """
    Processes a batch of unprocessed log entries from CardStatsLog.
    Updates aggregated statistics in CardStats and marks logs as processed.
    """
    logs = CardStatsLog.objects.filter(is_processed=False).order_by('timestamp')

    for log in logs:
        data = log.raw_payload

        if not log.raw_payload:
            log.is_processed = True
            log.result = "empty or invalid"
            log.save(update_fields=['is_processed', 'result'])
            continue

        try:
            with transaction.atomic():
                for card in data:
                    name = card.get('name')
                    card_id = card.get('id')
                    win = bool(card.get('win', False))
                    raw_score = float(card.get('score', 0))
                    score = raw_score if win else -raw_score
                    played = raw_score == 1.0
                    seen = raw_score >= 0.5

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
            
            log.is_processed = True
            log.result = "success"
            log.save(update_fields=['is_processed', 'result'])

        except Exception as e:
            log.is_processed = True
            log.result = f"error: {str(e)}"
            log.save(update_fields=['is_processed', 'result'])



def maybe_process_cardstats_logs():
    """
    Conditionally triggers batch processing of logs if either:
    - There are more than 50 unprocessed entries
    - More than 5 minutes have passed since the last processing
    """
    unprocessed_count = CardStatsLog.objects.filter(is_processed=False).count()
    state, _ = ProcessingState.objects.get_or_create(key='cardstats')

    too_many = unprocessed_count >= 50
    too_old = timezone.now() - state.last_processed_at > timezone.timedelta(minutes=5)

    if too_many or too_old:
        process_cardstats_logs()
        state.last_processed_at = timezone.now()
        state.save(update_fields=['last_processed_at'])
