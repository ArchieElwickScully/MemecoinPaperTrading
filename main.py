import requests
import json

def fetchCoin(token):
    r = requests.get(f'https://api.dexscreener.com/tokens/v1/solana/{token}')

    if len(r.json()) == 0:
        return False
    
    data = r.json()[0]

    return data['baseToken']['symbol'], data['marketCap'], data['priceNative'], data['priceUsd']

def main():
    while True:
        token = input('Enter Token address: ')

        coinData = fetchCoin(token)

        if coinData == False:
            print("Coin not found, please try again\n")
            continue

        coinName = coinData[0]
        marketCap = coinData[1]

        priceSol = coinData[2]
        priceUSD = coinData[3]

        print(f'\n\n{coinName}\n{token}\n\nMarketCap: {marketCap}\nPrice: {priceUSD} USD\n\n')

 
if __name__ == '__main__':
    main()



"""
plan

get coin info - done
buy sell conversions and stuff
positions system

"""
