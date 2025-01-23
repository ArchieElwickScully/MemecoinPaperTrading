import json

from api2 import fetchCoin


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

    def validateNumber(self, n):
        try:
            float(n)
        except (ValueError, TypeError):
            print('Please enter a valid number')
            return False

        return True

    def chargeFees(self, sol, o):
        if o == 'b':
            fee, tip = self.buyFee, self.buyTip
        else:
            fee, tip = self.sellFee, self.sellTip

        finalAmount = (float(sol) - fee) - tip
        finalAmount = finalAmount - (finalAmount * (self.takePercent / 100))

        return finalAmount


    def checkBalance(self, amount, o):
        if not self.validateNumber(amount):
            return False

        finalAmount = self.chargeFees(amount, o)

        if float(finalAmount) > self.balance:
            print("balance too low")
            return False

        return finalAmount

    def updateBalance(self, balance):
        with open('config.json') as f:
            config = json.load(f)

        config['balance'] = balance

        with open('config.json', 'w') as f:
            json.dump(config, f)

    def getPosition(self, ca):
        for position in self.positions:
            if position['ca'] == ca:
                return position

        return False

    def updatePosition(self, pos, newpos):
        if float(newpos['coins']) == 0:
            self.positions.remove(pos)
        else:
            i = self.positions.index(pos)
            self.positions[i] = newpos

        with open('positions.json', 'w') as f:
            json.dump(self.positions, f)

    def createPosition(self, ca, sol):
        coinData = fetchCoin(ca)
        coinName = coinData[0]
        marketCap = float(coinData[1])
        priceSol = float(coinData[2])

        amount = float(sol) / priceSol

        pos = {'coin': coinName, 'ca': ca, 'mc': marketCap, 'sol' : sol, 'coins': amount}
        self.positions.append(pos)

        self.balance -= sol
        self.updateBalance(self.balance)

        with open('positions.json', 'w') as f:
            json.dump(self.positions, f)

        print(f'\nbought {sol} sol of ${coinName}')

    def sellPosition(self, ca, percent):
        coinData = fetchCoin(ca)
        positionData = self.getPosition(ca)

        marketCap = float(coinData[1])
        priceSol = float(coinData[2])

        posMarketCap = float(positionData['mc'])
        posBalance = float(positionData['coins'])
        posSol = float(positionData['sol'])
        posName = positionData['coin']

        increase = ((marketCap - posMarketCap) / posMarketCap) * 100
        solIncrease = posSol * (increase/100)

        sellCoins = posBalance * (float(percent) / 100)

        posBalance = posBalance - sellCoins
        # when balance falls below 0 remove position add later

        sol = sellCoins * priceSol
        finalSol = self.chargeFees(sol, 's')

        self.balance += finalSol
        self.updateBalance(self.balance)

        pos = {'coin': posName, 'ca': ca, 'mc': marketCap, 'sol' : posSol, 'coins': posBalance}
        self.updatePosition(positionData, pos)

        print(f'\n{sellCoins} ${posName} sold for an increase of {increase}, {solIncrease} sol increase')



''''
when opening position we create an initial sol value
when this position balance falls below 0 we calculate the pnl

add charge fees
'''