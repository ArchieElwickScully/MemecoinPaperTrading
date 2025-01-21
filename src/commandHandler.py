class CommandHandler:
    def __init__(self, wallet):
        self.tokenCommands = {'buy': self.buy, 'sell': 'none', 'p': self.openPosition, 'e': 'none'}
        self.positioncCommand = ['sell']

        self.wallet = wallet
        self.commandDisplay = 'buy - buy the coin\nsell - sell your position\np - check for active positions\ne - exit\n'

    def handleToken(self, ca):
        command = ''

        while command != 'e':
            print(self.commandDisplay)
            command = input('Enter command for token: ')

            if command not in self.tokenCommands:
                print("Command not recognised, please try again\n")
                continue

            self.tokenCommands[command](ca)

    def openPosition(self, ca):
        pos = self.wallet.getPosition(ca)

        if not pos:
            print('position not found\n')
            return

    def buy(self, ca):
        amount = input('Enter sol amount to buy: ')

        final = self.wallet.checkBalance(amount)

        if not final:
            return

        self.wallet.createPosition(ca, final)

        print('position opened')
