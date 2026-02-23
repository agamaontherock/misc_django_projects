import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from chat_app.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket connected")
        self.user = self.scope['user']
        self.id = 1 #self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        # accept connection
        self.accept()


    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print("WebSocket disconnected")

    # receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        print("Received message: " + message)
        # send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))
        print("Sent message: " + message)
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
        'type': 'chat_message',
        'message': message,
        'user': self.user.username,
        'datetime': now.isoformat(),
        }
        )
        self.persist_message(message)

    # receive message from room group
    def chat_message(self, event):
        # send message to WebSocket
        self.send(text_data=json.dumps(event))

    def persist_message(self, message):
        Message.objects.create(
            user=self.user, room=self.id, content=message
        )