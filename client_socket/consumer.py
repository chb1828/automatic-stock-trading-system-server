from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ClientConsumer(WebsocketConsumer):
    def connect(self):

        self.client_name = "client"
        self.group_name = 'ASTS'

        # "room" 그룹에 가입
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        print("연결 성공")
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print("연결 해제.")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # "room" 그룹에서 메시지 전송

    def chat_message(self, event):
        message = event['message']

        # 웹 소켓으로 메시지 전송
        self.send(text_data=json.dumps({
            'message': message
        }))