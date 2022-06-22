from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json



class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = "chat_consumer"
        self.room_group_name = "chat_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status' : 'connected from dj channel'}))

    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status' : 'we got you'}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)