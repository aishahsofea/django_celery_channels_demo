import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .tasks import get_coin_list


class CoinListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('coin_list', self.channel_name)
        await self.accept()
        await self.send(json.dumps({'message': 'hey im server'}))

    @sync_to_async
    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        currency = text_data_json['currency']
        get_coin_list.delay(currency)

        schedule = IntervalSchedule.objects.create(every=10, period=IntervalSchedule.SECONDS)

        try:
            data = PeriodicTask.objects.get(name='Get coin list')
        except PeriodicTask.DoesNotExist:
            data = None

        if data is None:
            PeriodicTask.objects.create(
                interval=schedule,                
                name='Get coin list',          
                task='coin.tasks.get_coin_list', 
                args=json.dumps([currency]),
            )
        else:
            PeriodicTask.objects.filter(name='Get coin list').update(args=json.dumps([currency]))

    async def disconnect(self):
        await self.channel_layer.group_discard('coin_list', self.channel_name)

    async def send_coin_list(self, event):
        coin_list = event['coin_list']
        await self.send(json.dumps({'coin_list': coin_list}))
