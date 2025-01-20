import requests


def main():
    token = input('Enter Token address: ')

    r = requests.get(f'https://api.dexscreener.com/tokens/v1/solana/{token}')
    data = r.json()[0]

    coinName = data['baseToken']['symbol']
    marketCap = data['marketCap']

    priceSol = data['priceNative']
    priceUSD = data['priceUsd']

    print(f'\n\n{coinName}\n{token}\n\nMarketCap: {marketCap}\nPrice: {priceUSD}')
    
 
if __name__ == '__main__':
    main()
