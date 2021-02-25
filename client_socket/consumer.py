from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ClientConsumer(WebsocketConsumer):
    def connect(self):

        self.client_name = "client"
        self.group_name = 'ASTS'

        self.accept()
        # "ASTS" 그룹에 가입
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        print(f"Added {self.channel_name} channel to task")
        print("연결 성공")

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print(f"Removed {self.channel_name} channel to task")
        print("연결 해제.")

    # "ASTS" 그룹에서 메시지 전송
    def client_notification(self, event):
        self.send_json(event["data"])