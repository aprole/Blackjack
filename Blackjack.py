import random
from PlayingCards import *
from time import sleep

title = """
██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝ 
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ 
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""

troll = """
░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄
░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄
░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█
░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░█
░▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░█
█▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒█
█▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█
░█▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█
░░█░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█
░░░█░░██░░▀█▄▄▄█▄▄█▄████░█
░░░░█░░░▀▀▄░█░░░█░███████░█
░░░░░▀▄░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█
░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░█
░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░█
░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░█
"""

class Player():
    def __init__(self, name):
        self.name = name
        self.bankroll = Bankroll()
        self.hand = []

class InsufficientFundsExceptions(Exception):
    pass

class Bankroll():
    def __init__(self, bal=0):
            self._bal = bal

    def deposit(self, amt):
        self._bal += amt

    def withdraw(self, amt):
        if amt > self._bal:
            raise InsufficientFundsException
        else:
            self._bal -= amt

    def balance(self):
        return self._bal

def dealer_hit(hand, deck):
    hand.append(deck.pop())

def print_dealer_stand():
    print_status('Dealer stands')

def print_status(status, sleep_time = 1.5):
    print(status)
    sleep(sleep_time)

if __name__== '__main__':
    
    # Create player
    dealer = Player("Dealer")

    #name = input('Please enter your name: ')
    #player = Player(name)
    
    # Create deck
    deck = generate_deck()

    # Game
    while True:
        random.shuffle(deck)

        assert(len(deck) == 52)

        # Deal
        hands = deal(deck, 2, 2)

        dealer_hand = hands[0]
        player_hand = hands[1]

        player_turn = True
        dealer_hit_last_turn = False

        # Single Round
        while True:
            # Clear screen
            print('\n'*100, title)
            
            print("Dealer:")
            dealer_hand.print(not player_turn)

            print("You:")
            player_hand.print()

            # Print if dealer hit in last turn
            if not player_turn and dealer_hit_last_turn:
                print_status('Dealer hits!')

            # Player's turn
            if player_turn:
                # Check for bust
                if player_hand.is_bust():
                    print_status('You Bust!')
                    player_turn = False
                    continue  
                elif player_hand.is_blackjack():
                    print_status('You have Blackjack!')
                    player_turn = False
                    continue     

                while True:
                    ans = input('(H)it or (S)tand? ')
                    if ans.lower() in ('h', 's'):
                        break
                    else:
                        print('invalid response. Please pick \'h\' for hit or \'s\' for stand')

                # Hit
                if ans == 'h':
                    player_hand.append(deck.pop())
                
                # if stand, let dealer take turn
                else:
                    print_status('You stand')
                    print_status('Dealer\'s turn...')
                    player_turn = False
                    continue

            # Dealer's turn
            else:
                dealer_hit_last_turn = False

                # If player has blackjack
                if player_hand.is_blackjack():
                    break

                # Check for bust
                elif dealer_hand.is_bust():
                    print_status('Dealer Busts!')
                    break

                elif dealer_hand.is_blackjack():
                    print_status('Dealer has Blackjack!')
                    break       

                # If soft hand
                if dealer_hand.point_value()[1] > 0:
                    if max(dealer_hand.point_value()) < 19:
                        dealer_hit(dealer_hand, deck)
                        dealer_hit_last_turn = True
                    else:
                        print_dealer_stand()
                        break # Stand

                # If hand value is 17 or higher, then stand
                elif max(dealer_hand.point_value()) >= 17:
                    print_dealer_stand()
                    break # Stand

                # Check player's upcard
                elif player_hand.cards[0].point_value() <= 6 and dealer_hand.point_value()[0] >= 13:
                    print_dealer_stand()
                    break # Stand
                
                else:
                    dealer_hit(dealer_hand, deck)
                    dealer_hit_last_turn = True

        

        if not (dealer_hand.is_bust() or player_hand.is_bust()):
            # End of round. Determine winner
            # 0 = dealer win
            # 1 = player win
            # 2 = push
            if player_hand.is_blackjack():
                # If dealer has blackjack, it's a push
                if dealer_hand.is_blackjack():
                    result = 2
                else:
                    result = 1

            elif dealer_hand.is_blackjack():
                result = 0

            else:
                if max(dealer_hand.point_value()) > max(player_hand.point_value()):
                    result = 0
                elif max(player_hand.point_value()) > max(dealer_hand.point_value()):
                    result = 1
                elif max(player_points) == max(dealer_points):
                    result = 2

            if result == 0:
                print("Dealer wins!")
                print(troll)
            elif result == 1:
                print("You win!")
            elif result == 2:
                print("Push!")

        # Print new line
        print()

        # Ask to play again
        while True:
            ans = input("Play again (y/n)? ")
            if ans.lower() in ('y', 'n'):
                break

        if ans == 'n':
            break

        else:
            # Add cards back to deck
            deck += player_hand.cards
            del player_hand
            deck += dealer_hand.cards
            del dealer_hand
