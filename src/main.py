from src.api import fetchCoin
from src.commandHandler import CommandHandler
from src.wallet import Wallet

wallet = Wallet()

def displayCoin(ca):
    coinData = fetchCoin(ca)

    if not coinData:
        print('Coin not found, please try again\n')
        return False

    coinName = coinData[0]
    marketCap = coinData[1]

    priceSol = coinData[2]
    priceUSD = coinData[3]

    print(f'\n\n{coinName}\n{ca}\n\nMarketCap: {marketCap}\nPrice: {priceUSD} USD\n\n')
    return True


def main():
    COMMANDHANDLER = CommandHandler(wallet)

    while True:
        bal = f'Balance: {wallet.balance} Sol'

        print("\n" + "=" * len(bal))
        print(bal)
        print("=" * len(bal) + "\n")

        ca = input('Enter coin address: ')

        if displayCoin(ca):
            COMMANDHANDLER.handleToken(ca)

        print(wallet.positions)

 
if __name__ == '__main__':
    main()



'''
plan

get coin info - done
buy sell conversions and stuff
positions system

positions system
json file
layout

coin : coin
amount : amount
marketcapAtBuy: mc

'''
