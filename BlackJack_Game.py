print('\n*************************************************')
print('*********** Welcome to BlackJack Game ***********')
print('*************************************************')

import random

# Defining Global Variables

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'six', 'Seven', 'Eight', 'Nine', 'Ten', 'Ace', 'King', 'Queen', 'Jack')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Ace':11, 'King':10, 'Queen':10, 'Jack':10}

playing = True


#################################################################################################################
#######     CLASS DEFINITIONS    ################################################################################
#################################################################################################################


class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck():
    
    def __init__(self):
        self.deck = []  # list to store the card object for each card i.e. 52 cards
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''  # string to store the string value of each card object
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The Deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand():
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips():

    def __init__(self, total = 100):
        self.total = total   # 100 is default value , different value can be taken while creating object
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

    
#################################################################################################################
#######     FUNCTION DEFINITIONS    #############################################################################
#################################################################################################################

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('\nHow many chips would you like to bet ? '))
        except ValueError:
            print('Please input an Integer Value ')
        else:
            if chips.bet > chips.total:
                print('Value can not exceed available Chip balance', chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input("\nWould you like to Hit or stand ? Enter 'h' or 's' ")
        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("\nYou have chosen to stand, Now Dealer will Play")
            playing = False

        else:
            print("Wrong Choice, Please try again ")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("<<Card Hidden>>")        #Dealer's first card will always be hidden
    print('', dealer.cards[1])
    print("\nPlayers Hand:")
    print('', *player.cards, sep = '\n')

def show_all(player, dealer):
    print("\nDelaer's Hand:", *dealer.cards, sep = '\n')
    print("Dealer's Total Value is: ", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep = '\n')
    print("Player's Total Value is: ", player.value)


def player_busts(player, dealer, chips):
    print("\nPlayer Busts")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("\nPlayer wins")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("\nDealer Busts")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("\nDealer Wins")
    chips.lose_bet()

def push(player, dealer):
    print("\nDealer and Player Tie ! It's a Push")

###################################################################################
######      PLAYING THE GAME       ################################################
###################################################################################

while True:

    print("\nWelcome to BlackJack Game !!!\nGet as close as 21 without going over\nDealer will Hit until it reaches 17 or more")
    #create and shuffle the Deck
    deck = Deck()
    deck.shuffle()

    #Getting two cards from shuffled deck for player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    #Getting two cards from shuffled deck for Dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #set up the players chips
    player_chips = Chips()   #Default value is 100, if you want to change it pass arg as player_chips = Chips(1000)

    #Ask for the player's bet value
    take_bet(player_chips)

    # show cards but keep first card of dealer hidden
    show_some(player_hand, dealer_hand)

    
    while playing:    #reaclling the global variable playing from hit_or_stand function
        
        # Ask player for hit or stand
        hit_or_stand(deck, player_hand)

        # show cards but keep first card of dealer hidden
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    #If player has not busted, play dealer's hand until it reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value <=17:
            hit(deck, dealer_hand)

        #show all cards
        show_all(player_hand, dealer_hand)

        #Check different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform player about his chips value
    print("\nPlayer total chips value now stands at ", player_chips.total)

    #Ask to play again
    new_game = input("\nDo you want to play again? Enter 'y' or 'n' ")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing !!!")
        break

