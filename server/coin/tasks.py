import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def get_market_api(page=1, per_page=100, currency='usd'):
    market_api = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&page={page}&per_page={per_page}'
    return market_api


@shared_task
def get_coin_list(currency='usd'):
    data = requests.get(get_market_api(1, 100, currency)).json()

    async_to_sync(channel_layer.group_send)(
        'coin_list', {
            'type': 'send_coin_list', 
            'coin_list': data
        }
    )
