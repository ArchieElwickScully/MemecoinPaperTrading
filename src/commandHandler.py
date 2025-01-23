from api2 import fetchCoin


class CommandHandler:
    def __init__(self, wallet):
        self.tokenCommands = {'b': self.buy, 's': 'none', 'p': self.handlePosition, 'e': 'none'}
        self.positioncCommands = {'s' : self.sell, 'e' : 'none'}

        self.wallet = wallet
        self.commandDisplay = 'buy - buy the coin\nsell - sell your position\np - check for active positions\ne - exit\n'


    def displayPosition(self, ca, pos):
        #get tokens current mc etc
        coinData = fetchCoin(ca)

        if not coinData:
            print('Coin data could not be retreived, this should not happen unless the api is down '
                  'or you manually edited the ca in the positions file, if you manage to see this '
                  'good job i suck at coding\n')
            return False

        coinName = coinData[0]
        marketCap = float(coinData[1])
        priceSol = float(coinData[2])
        priceUSD = float(coinData[3])

        coins = float(pos['coins'])
        mcAtBuy = float(pos['mc'])
        boughtSol = float(pos['sol'])

        increase = ((marketCap - mcAtBuy) / mcAtBuy) * 100
        solIncrease = boughtSol * (increase/100)

        worthusd = coins * priceUSD
        worthsol = coins* priceSol

        print('\n' + '=' * 20)
        print(f'{coins} ${coinName}')
        print(f'marketcap bought: {mcAtBuy}')
        print(f'marketcap current: {marketCap}\n')
        print(f'increase: {increase}% (+{solIncrease} Sol)')
        print(f'worth: ${worthusd}')
        print(f'worth: {worthsol} Sol')
        print(f'bought: {boughtSol}')
        print('=' * 20 + '\n')

    def handleToken(self, ca):
        while True:
            #print(self.commandDisplay)
            command = input('\nEnter command for token: ')

            if command not in self.tokenCommands:
                print("Command not recognised, please try again\n")
                continue

            if command == 'e':
                break

            self.tokenCommands[command](ca)

    def handlePosition(self, ca):
        pos = self.wallet.getPosition(ca)

        if not pos:
            print('position not found\n')
            return

        self.displayPosition(ca, pos)

        while True:
            command = input('\nEnter command for position: ')

            if command not in self.positioncCommands:
                self.displayPosition(ca, pos)
                continue

            if command == 'e':
                break

            self.positioncCommands[command](ca)

    def buy(self, ca):
        amount = input('Enter sol amount to buy: ')

        final = self.wallet.checkBalance(amount, 'b')

        if not final:
            return

        self.wallet.createPosition(ca, final)

        print('position opened')

    def sell(self, ca):
        percent = input('Enter percent of position to sell: ')

        if not self.wallet.validateNumber(percent):
            return

        self.wallet.sellPosition(ca, percent)
