import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = f'chat_1'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
 
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"received {message}")
        
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        # send message to WebSocket
        self.send(text_data=json.dumps(event))