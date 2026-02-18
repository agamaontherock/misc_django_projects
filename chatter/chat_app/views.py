from django.shortcuts import render

# Create your views here.
def chat_room(request, room_id):
    return render(request, "chat_app/chat_room.html", {"room_id":room_id})