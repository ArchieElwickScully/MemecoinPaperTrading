import requests
import json

def fetchCoin(token):
    r = requests.get(f'https://api.dexscreener.com/tokens/v1/solana/{token}')

    if len(r.json()) == 0:
        return False

    data = r.json()[0]

    return data['baseToken']['symbol'], data['marketCap'], data['priceNative'], data['priceUsd']


class Wallet:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

            self.balance = float(config['balance'])

            self.buyFee = float(config['fees']['buy']['fee'])
            self.buyTip = float(config['fees']['buy']['tip'])

            self.sellFee = float(config['fees']['sell']['fee'])
            self.sellTip = float(config['fees']['sell']['tip'])
            
        with open('positions.json') as f:
            self.positions = json.load(f)

    def getPosition(self, ca):
        for position in self.positions:
            if position['ca'] == ca:
                return position

        return False

    def createPosition(self, ca, sol):
        coinData = fetchCoin(ca)

        coinName = coinData[0]
        marketCap = float(coinData[1])

        priceSol = float(coinData[2])

        amount = float(sol)/priceSol

        pos = {'coin' : coinName, 'ca' : ca, 'mc' : marketCap, 'coins' : amount}
        self.positions.append(pos)

        wallet.balance -= sol

        with open('positions.json', 'w') as f:
            json.dump(self.positions, f)


wallet = Wallet()

class CommandHandler:
    def __init__(self):
        self.tokenCommands = {'buy' : self.buy, 'sell' : 'none', 'p' : 'none', 'e' : 'none'}
        self.positioncCommand = ['sell']

    def handleToken(self, ca):
        command = ''

        while command != 'e':
            command = input('Enter command for token: ')
            while command not in self.tokenCommands:
                print("Command not recognised, please try again")
                command = input('> ')

            self.tokenCommands[command](ca)

    def buy(self, ca):
        amount = input('Enter sol amount to buy: ')

        try:
            float(amount)
        except (ValueError, TypeError):
            print('Please enter a valid number')
            return

        finalAmount = (float(amount) - wallet.buyFee) - wallet.buyTip

        if float(finalAmount) > wallet.balance:
            print("Amount too low")
            return

        wallet.createPosition(ca, finalAmount)
        print('position opened')


def main():
    COMMANDHANDLER = CommandHandler()

    while True:
        bal = f'Balance: {wallet.balance} Sol'

        print("\n" + "=" * len(bal))
        print(bal)
        print("=" * len(bal) + "\n")

        token = input('Enter Token address: ')

        coinData = fetchCoin(token)

        if coinData == False:
            print('Coin not found, please try again\n')
            continue

        coinName = coinData[0]
        marketCap = coinData[1]

        priceSol = coinData[2]
        priceUSD = coinData[3]

        print(f'\n\n{coinName}\n{token}\n\nMarketCap: {marketCap}\nPrice: {priceUSD} USD\n\n')
        COMMANDHANDLER.handleToken(token)

 
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
