from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.db import connection
from django.http import HttpResponse
from django.core.management import call_command

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
