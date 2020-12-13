from random import shuffle #imports only shuffle() to shuffle the card deck

#GLOBAL VARIABLES 
suits = ('Hearts', 'Spades', 'Clubs', 'Diamonds')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 
        'Queen', 'King', 'Ace')
values = {'Two':2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six':6, 'Seven': 7, 'Eight': 8, 
          'Nine':9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

game_active = True

class Card():
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    
    def __init__(self):
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
                
    def __str__(self):
        
        deck = ''
        
        for card in self.all_cards:
            
            deck += "\n" + card.__str__()
            
        return f"The deck is composed of: {deck}"
    
    def shuffle(self):
        
        shuffle(self.all_cards)
        
    def deal_card(self):
        
        return self.all_cards.pop() #takes a single card from the entire card deck

class Hand:
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        '''
        card passed into function from Deck.deal_card()
        that grabs one of the 52 Card objects: one Card(suit, rank)
        '''
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def ace_adjust(self):
        
        '''
        When the total value of the hand is greater than 21 and there is an ace in the hand, 
        subtract 10 from the total value since the ace can be either a 1 or 11 (starts as an 11).
        Further, take away an ace since this card was used. 
        
        We are treating the self.aces as a Boolean value, although it is an integer. If it refers to zero,
        then that means the while loop does not run. 0 acts as the False Boolean value. 
        '''
        
        while self.value > 21 and self.aces: 
            self.value -= 10
            self.aces -= 1
            
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0 #updated by take_bet() function
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True: 
        
        try: 
            chips.bet = int(input('How much do you want to bet? '))
        
        except:
            print("Need an integer. Try again. ")
        
        else: 
            
            if chips.bet > chips.total:
                print(f"You only have {chips.total}. Try a lower number.")
                
            else:
                break

def hit(deck, hand):
    
    card = deck.deal_card()
    hand.add_card(card)
    hand.ace_adjust()

def hit_or_stand(deck, hand):
    '''
    This function determines if the player hits or stands: takes a card or stops taking cards and let's the dealer 
    have their turn and handles unintended user input 
    '''
    global game_active
    
    while True: 
        
        h_or_p = input('Hit or Stand: enter an h or an s: ')
        
        #CALLS HIT() TO TAKE A CARD FROM THE DECK AND ADD TO THE HAND
        if h_or_p.lower() == 'h':
            hit(deck, hand)
        
        #THE PLAYER DOES NOT DEAL ANY MORE CARDS AND IT IS THE DEALER'S TURN
        elif h_or_p.lower() == 's':
            print("Player 1 stands Dealer's turn")
            game_active = False
            
        else: 
            #SERVES AS THE ERROR MESSAGE THAT CONTINUES TO THE TOP INPUT FUNCTION
            print('Sorry, need an h or an s. Try again.') 
            continue      
            
        break #BREAKS THE LOOP IF NONE OF THE CONDITIONS APPLY

#####These next two functions show the cards hiding one dealer card##########

def show_some(player, dealer):
    print(f'\nDealer cards:\n\tHidden card\n\t{dealer.cards[1]}')
    print('')
    print("Player cards: ", *player.cards, sep='\n\t')
    print(f"\tValue of player hand: {player.value}\n")
    
#the * before player.cards or dealer.cards allow the program to grab each element in the list 
#and prints each element individually

def show_all(player, dealer):
    print('\nDealer cards:', *dealer.cards, sep='\n\t')
    print('')
    print(f'\tValue of dealer hand: {dealer.value} \n')
    print('Player cards: ', *player.cards, sep = '\n\t')
    print(f"\tValue of player hand: {player.value}")

#winner/loser/tie functions

def player_busts(player, dealer, chips):
    print('\nPlayer Busts!')
    chips.lose_bet()
    
def player_wins(player, dealer, chips):
    print('\nPlayer wins!')
    chips.win_bet()
    
def dealer_busts(player, dealer, chips):
    print('\nDealer busts. Player wins!')
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('\nDealer wins!')
    chips.lose_bet()
    
def push(player, dealer):
    print('\nPlayer and Dealer tied: push!')

#GAME LOGIC
while True:
    
    game_active = True
    
    #Introduction to the game 
    print('Welcome to Black Jack!')
    
    
    #Creates the deck and shuffles the deck 
    deck = Deck()
    deck.shuffle()
    
    #Sets up the player's and the dealer's hand
    player_hand = Hand()
    dealer_hand = Hand()
    
    #deals two cards to each the player and the dealer
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        
    #sets up the chips for the human player
    player_chips = Chips()
    
    #prompt the human player to place a bet
    take_bet(player_chips)
    
    #display cards leaving one of the dealer's cards hidden
    show_some(player_hand, dealer_hand)
    
    while game_active:
        
        #prompt player to hit or stand
        hit_or_stand(deck, player_hand)
        
        #show cards with one card of computer dealer hidden
        show_some(player_hand, dealer_hand)
        
        if player_hand.value > 21:
            player_hand.ace_adjust()
            player_busts(player_hand, dealer_hand, player_chips)
        
            break
            
    if player_hand.value <= 21:
        
        player_hand.ace_adjust()
        
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)
            
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21: 
            dealer_busts(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
            
        else:
            push(player_hand, dealer_hand)
            
    print(f"\nPlayer's total chips: {player_chips.total}")
    
    
    #This prompts the user if they want to play again and continues to do so until the correct input
    
    replay = input('Do you want to play again: y for yes, n for no: ').lower()
    
    while replay not in ['y', 'n'] or replay == '':
        replay = input('Sorry, need a y or an n for yes or no')
        
    if replay == 'y':
        game_active = True
        continue
    else: 
        print('Thank you for playing Black Jack programmed in Python 3')
        break
    
        