import json
from channels.generic.websocket import AsyncWebsocketConsumer


class InventoryConsumer(AsyncWebsocketConsumer):
    """
    Handles one patient's WebSocket connection. Every connected client
    joins a shared "group" called 'inventory_updates' — think of a group
    like a chat room: anyone in it receives any message broadcast to it.

    Later we could make groups per-city or per-medicine for efficiency
    (so a patient in Mumbai doesn't get Hyderabad's updates) — flagged
    here as a known simplification for the MVP.
    """
    GROUP_NAME = 'inventory_updates'

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    # This method name MUST match the "type" key we send in group_send
    # (see billing/signals.py below) — Channels converts "inventory.update"
    # into a call to inventory_update() automatically.
    async def inventory_update(self, event):
        await self.send(text_data=json.dumps(event['data']))