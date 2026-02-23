from django.urls import path
from . import views

app_name = 'chat_app'

urlpatterns = [
    path('chat/room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
