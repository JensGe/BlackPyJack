class Game(self):






    def pay(self, player):
        player.bankroll += player.bet
        print 'Bankroll increased by %s to %s' % (player.bet, player.bankroll)
        player.bet = 0








