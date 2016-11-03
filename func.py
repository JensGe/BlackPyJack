import random

# Classes


class Player(object):
    def __init__(self, name, bankroll=100, isdealer=False):
        self.bankroll = bankroll
        self.name = name
        self.isdealer = isdealer
        self.hand = []
        self.handvalue = 0
        self.bet = 0
        if isdealer:
            print '%s created' % self.name
        else:
            print 'Player %s created with Bankroll %s' % (self.name, self.bankroll)

    def bet(self, amount):
        self.bankroll -= amount
        self.bet = amount

    def show_hand(self):
        print 'You look at your hand, you see: '
        fillword = ''
        printstring = ''
        for item in self.hand:
            article = 'a '
            if item[0].startswith('E') or item[0].startswith('A'):
                article = 'an '
            printstring += fillword + article + item[0]
            fillword = ', '
        print printstring
        return

    def check_hand_value(self):
        self.handvalue = 0
        for item in self.hand:
            self.handvalue += item[1]
        return

class CardDeck(object):
    # class object attributes
    content = [('Two of Diamonds', 2), ('Three of Diamonds', 3),
               ('Four of Diamonds', 4), ('Five of Diamonds', 5),
               ('Six of Diamonds', 6), ('Seven of Diamonds', 7),
               ('Eight of Diamonds', 8), ('Nine of Diamonds', 9),
               ('Ten of Diamonds', 10), ('Jack of Diamonds', 10),
               ('Queen of Diamonds', 10), ('King of Diamonds', 10),
               ('Ace of Diamonds', 11), ('Two of Hearts', 2),
               ('Three of Hearts', 3), ('Four of Hearts', 4),
               ('Five of Hearts', 5), ('Six of Hearts', 6),
               ('Seven of Hearts', 7), ('Eight of Hearts', 8),
               ('Nine of Hearts', 9), ('Ten of Hearts', 10),
               ('Jack of Hearts', 10), ('Queen of Hearts', 10),
               ('King of Hearts', 10), ('Ace of Hearts', 11),
               ('Two of Clubs', 2), ('Three of Clubs', 3),
               ('Four of Clubs', 4), ('Five of Clubs', 5),
               ('Six of Clubs', 6), ('Seven of Clubs', 7),
               ('Eight of Clubs', 8), ('Nine of Clubs', 9),
               ('Ten of Clubs', 10), ('Jack of Clubs', 10),
               ('Queen of Clubs', 10), ('King of Clubs', 10),
               ('Ace of Clubs', 11), ('Two of Spades', 2),
               ('Three of Spades', 3), ('Four of Spades', 4),
               ('Five of Spades', 5), ('Six of Spades', 6),
               ('Seven of Spades', 7), ('Eight of Spades', 8),
               ('Nine of Spades', 9), ('Ten of Spades', 10),
               ('Jack of Spades', 10), ('Queen of Spades', 10),
               ('King of Spades', 10), ('Ace of Spades', 11)]

    def __init__(self):
        print 'CardDeck created'
        random.shuffle(CardDeck.content)
        print 'CardDeck shuffled'

    def pop_card(self, amount=1):
        draw = []
        while amount > 0:
            try:
                draw.append(self.content.pop())
                amount -= 1
                return draw
            except:
                print 'No Cards left'
                return

class Game(object):
    players = []
    rounds = []
    game_running = True

    def __init__(self):
        print 'Starting Game ...'
        self.players.append(Player('Dealer', 100000, isdealer=True))
        player_count = 0
        create_users = True
        while create_users:
            print 'Create a new Player.'
            self.players.append(Player(raw_input('Playername: '), 200))
            if raw_input('Create another Player? (y/n)') == 'y':
                continue
            else:
                create_users = False

        print 'This are the participating players:'
        for player in self.players:
            if player.isdealer == False:
                print player.name,

    def game_menu(self):
        print '''
        ******************************
        **   1) Start Round         **
        **   2) Player Join         **
        **   3) Player Quit         **
        **   4) Show Player Stats   **
        **   5) Quit Game           **
        ******************************
        '''
        selection = int(raw_input('Select an option (1-5) > '))     # Exception if selection not int
        print 'Selection: %d'%selection
        if selection == 1:
            self.start_round()
        elif selection == 2:
            self.add_player()
        elif selection == 3:
            self.remove_player()
        elif selection == 4:
            self.show_playerstats()
        if selection == 5:
            self.quit_game()

        return

    def start_round(self):
        self.rounds.append(Round())
        for player in self.players[1:]:
            self.rounds[-1].hit_or_stand(player)
        self.rounds[-1].calculate_dealer_turn()
        self.rounds[-1].the_winner_is()

    def add_player(self):
        self.players.append(Player(raw_input('Playername: '), 200))

    def remove_player(self):
        print 'Which Player will quit the Game?'
        i = 1
        for player in self.players[1:]:
            print '%d) %s' %(i,player.name)
            i += 1
        leaving_player = self.players.pop(int(raw_input('Going Player #')))
        print 'Bye %s, thanks for playing. You take %d Bucks with you'%(leaving_player.name, leaving_player.bankroll)

    def show_playerstats(self):
        for player in self.players[1:]:
            print 'Name: %s, Bankroll: %s.'%(player.name,player.bankroll)
            print '-----------------------------------------------------'

    def quit_game(self):
        print 'Thanks for playing. Goodbye'
        quit()

class Round(Game):
    playing_deck = CardDeck()

    def __init__(self):
        print 'Starting Round ...'

        for player in self.players[1:]:
            player.bet = int(raw_input('%s, set your bet: ' % player.name))
            player.bankroll -= player.bet
            print '%s, your bet is %s.' % (player.name, player.bet)

        for player in self.players:
            player.hand = []
            player.hand += self.playing_deck.pop_card(1)

        for player in self.players[1:]:
            player.hand += self.playing_deck.pop_card(1)

    def deal_card(self, player, amount=1):
        player.hand += self.playing_deck.pop_card(amount)

    def player_hand_value(self, player):
        hand_value = 0
        for item in player.hand:
            hand_value += item[1]
        return hand_value

    def hit_or_stand(self, player):
        """ deals a player a new card to his hand until the player dont wants a new card.
        """
        more_cards = True
        while more_cards:
            print '%s, your hand: %s, its Value is: %s.' % (player.name, player.hand, self.player_hand_value(player))
            hos = raw_input('%s, do you want to Hit or to Stand (h/s): ' % player.name).lower()
            if hos == 's':
                print 'You stand at %s' % (self.player_hand_value(player))
                more_cards = False
            elif hos == 'h':
                self.deal_card(player, 1)
                if self.player_hand_value(player) < 21:
                    continue
                elif self.player_hand_value(player) > 21:
                    print 'You draw a %s and with %s points you are busted' % (
                        player.hand[-1], self.player_hand_value(player))
                    break
                elif self.player_hand_value(player) == 21:
                    print 'You now have 21 Points. You stand automatically'
                    more_cards = False
                    break
            else:
                'Not a valid Selection, repeat'
                continue

    def calculate_dealer_turn(self):
        print 'The dealer hand is %s' % self.players[0].hand
        while self.player_hand_value(self.players[0]) <= 16:
            self.deal_card(self.players[0])
            print 'The dealer draws a %s.' % (self.players[0].hand[-1][0])
        print 'The Dealer stops his turn with a handvalue of %s.' % (self.player_hand_value(self.players[0]))

    def the_winner_is(self):
         for player in self.players:
            if self.player_hand_value(player) <= 21:
                player.handvalue = self.player_hand_value(player)
            players_sorted = sorted(self.players, key=lambda player: player.handvalue, reverse=True)
            best_hand_value = players_sorted[0].handvalue
            print 'Best Hand Value is %s'%best_hand_value
            winnerlist = []
            for player in players_sorted:
                if player.handvalue == best_hand_value:
                    winnerlist.append(player)
                    print "Player %s, Value %d" % (player.name, player.handvalue)
            if len(winnerlist) == 1 and winnerlist[0].isdealer:
                print 'Dealer wins, Rest looses'
                for player in self.players:
                    print 'Set bet to 0 for %s' % player.name
                    player.bet = 0
            elif len(winnerlist) == 1 and not winnerlist[0].isdealer:
                print '%s wins, Rest looses' %winnerlist[0].name
                print 'Player %s wins %d' % (winnerlist[0].name, (2 * winnerlist[0].bet))
                winnerlist[0].bankroll += (2 * winnerlist[0].bet)
                for player in self.players:
                    print 'Set Bet to 0 for %s' % player.name
                    player.bet = 0
            elif len(winnerlist) > 1 and not winnerlist[0].isdealer:
                print 'Multiple Winners'
                for winner in winnerlist:
                    print 'Player %s wins %d' % (winner.name, (2*winner.bet))
                    winner.bankroll += (2 * winner.bet)
                for player in self.players:
                    print 'Set bet to 0 for %s' % player.name
                    player.bet = 0
            elif len(winnerlist) > 1 and winnerlist[0].isdealer:
                print 'Tie'
                for winner in winnerlist[1:]:
                    print 'Set bet back %s'%winner.name
                    winner.bankroll += winner.bet
                for player in self.players:
                    print 'Set bet to 0 for %s' % player.name
                    player.bet = 0