from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
import datetime, json


def get_token(request, id, date):
    try:
        doctor = Doctor.objects.get(id=id)
        tokens = Token.objects.filter(doctor=doctor, date=date)
        next_token = 1 if tokens is None else len(tokens) + 1
        return JsonResponse({'next_token': next_token})
    except (ValueError, Doctor.DoesNotExist):
        return JsonResponse({'error': 'Invalid data provided'}, status=400)


