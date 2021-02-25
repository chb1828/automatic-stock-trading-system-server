from django.shortcuts import render


def index(request):
    return render(request, 'client/index.html',{})


def room(request, room_name):
    return render(request, 'client/room.html',{
        'room_name': room_name
    })