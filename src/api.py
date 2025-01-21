import requests


def fetchCoin(token):
    r = requests.get(f'https://api.dexscreener.com/tokens/v1/solana/{token}')

    if len(r.json()) == 0:
        return False

    data = r.json()[0]

    return data['baseToken']['symbol'], data['marketCap'], data['priceNative'], data['priceUsd']
