import requests


def fetchCoin(token):
    r = requests.get(f'https://meme-api.openocean.finance/market/token/detail?address={token}')

    if r.json()['data'] is None:
        return False

    data = r.json()

    return data['data']['symbol'], data['data']['marketCap'], data['data']['priceSol'], data['data']['price']