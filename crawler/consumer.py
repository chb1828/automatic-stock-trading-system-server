from channels.generic.websocket import WebsocketConsumer
import json


class ClientConsumer(WebsocketConsumer):
    async def connect(self):
        print("연결 성공")
        self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        print(text_data,"찍힘")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message':message
        }))