import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ModelUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("model_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("model_updates", self.channel_name)

    async def send_model_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
