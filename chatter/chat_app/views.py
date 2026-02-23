from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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


@login_required
def chat_room(request, room_id):
    return render(request, 'chat_app/chat_room.html', {
        'room_id': room_id,
        'username': request.user.username,
    })