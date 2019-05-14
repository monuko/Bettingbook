from django.shortcuts import render

from.models import Room 
from django.http import JsonResponse
from django.conf import settings

def all_rooms(request): 
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms' : rooms})

def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room' : room})
    
