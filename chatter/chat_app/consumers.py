import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            self.close()
            return

        self.room_group_name = "chat_1"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.user.username,
                "time": datetime.now().strftime("%H:%M"),
                "sender_id": self.user.id,
            },
        )

    def chat_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "time": event["time"],
                    "sender_id": event["sender_id"],
                }
            )
        )
