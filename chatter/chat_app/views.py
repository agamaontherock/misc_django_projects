from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from chat_app.models import Message


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/chat/room/1/')
            return redirect(next_url)
        else:
            error = 'Invalid username or password.'
    return render(request, 'chat_app/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('chat:login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:chat_room', room_id=1)
    else:
        form = UserCreationForm()
    return render(request, 'chat_app/register.html', {'form': form})


@login_required
def chat_room(request, room_id):
#     latest_messages = course.chat_messages.select_related(
# 'user'
# ).order_by('-id')[:5]
# latest_messages = reversed(latest_messages)
# return render(
# request,
# 'chat/room.html',
# {'course': course, 'latest_messages': latest_messages}
# )
    latest_messages = Message.objects.filter(room=room_id).select_related('user').order_by('-id')[:5]
    latest_messages = reversed(latest_messages)
    return render(request, 'chat_app/chat_room.html', {
        'room_id': room_id,
        'username': request.user.username,
        'latest_messages': latest_messages
    })