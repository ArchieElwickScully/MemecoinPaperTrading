import json

from api import fetchCoin


class Wallet:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

            self.balance = float(config['balance'])

            self.takePercent = float(config['fees']['brokerpercent'])

            self.buyFee = float(config['fees']['buy']['fee'])
            self.buyTip = float(config['fees']['buy']['tip'])

            self.sellFee = float(config['fees']['sell']['fee'])
            self.sellTip = float(config['fees']['sell']['tip'])

        with open('positions.json') as f:
            self.positions = json.load(f)

    def checkBalance(self, amount):
        try:
            float(amount)
        except (ValueError, TypeError):
            print('Please enter a valid number')
            return False

        finalAmount = (float(amount) - self.buyFee) - self.buyTip

        if float(finalAmount) > self.balance:
            print("balance too low")
            return False

        return True


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

        amount = float(sol) / priceSol

        pos = {'coin': coinName, 'ca': ca, 'mc': marketCap, 'coins': amount}
        self.positions.append(pos)

        self.balance -= sol

        with open('positions.json', 'w') as f:
            json.dump(self.positions, f)
