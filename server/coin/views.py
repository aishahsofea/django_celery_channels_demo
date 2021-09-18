from django.shortcuts import render


def get_market_api(page=1, per_page=100, currency='usd'):
    market_api = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&page={page}&per_page={per_page}&sparkline=true'
    return market_api


@api_view()
def coin_list(request):
    page = request.query_params['page']
    per_page = request.query_params['per_page']
    currency = request.query_params['currency']

    data = requests.get(get_market_api(page, per_page, currency)).json()


    serializer = CoinListSerializer(data=data, many=True)
    serializer.is_valid(True)
    return Response(data=serializer.data)
