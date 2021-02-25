from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.client_name = "client"
        self.group_name = 'ASTS'

        # "ASTS" 그룹에 가입
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print(f"Added {self.channel_name} channel to task")
        print("연결 성공")

    async def disconnect(self, code):
        await async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print(f"Removed {self.channel_name} channel to task")
        print("연결 해제.")

    # "ASTS" 그룹에서 메시지 전송
    async def client_notification(self, event):
        print(event["data"])
        await self.send(json.dumps({
            "type": "websocket.send",
            "data": event["data"]
        }))