import random
from PlayingCards import *
from time import sleep
import sys

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

SLEEP_TIME = 2

class Player():
    def __init__(self, name):
        self.name = name
        self.bankroll = Bankroll(2000)

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
    print_round_info('Dealer hits')
    sleep(SLEEP_TIME)

def print_dealer_stand():
    print_round_info('Dealer stands')
    sleep(SLEEP_TIME)

def print_round_info(status = ''):
    # Clear screen
    print('\n'*100, title)
    
    # Print dealer info
    print("Dealer:")
    dealer.hand.print(not player_turn)
    print()

    print("You:")
    player.hand.print()

    print()
    sys.stdout.write(status)
    sys.stdout.flush()

if __name__== '__main__':
    
    # Create player
    dealer = Player("Dealer")

    #name = input('Please enter your name: ')
    player = Player('Player')
    
    # Create deck
    deck = generate_deck()

    # Game
    while True:
        random.shuffle(deck)

        assert(len(deck) == 52)

        # Deal
        hands = deal(deck, 2, 2)

        dealer.hand = hands[0]
        player.hand = hands[1]

        player_turn = True

        # Single Round
        while True:
            print_round_info()

            # Player's turn
            if player_turn:
                # Check for bust
                if player.hand.is_bust():
                    print_round_info('You Bust!')
                    sleep(SLEEP_TIME)
                    player_turn = False

                elif player.hand.is_blackjack():
                    print_round_info('You have Blackjack!')
                    sleep(SLEEP_TIME)
                    player_turn = False

                # If still the player's turn, ask to hit or stand
                if player_turn:
                    while True:
                        ans = input('(H)it or (S)tand? ')
                        if ans.lower() in ('h', 's'):
                            break
                        else:
                            print('invalid response. Please pick \'h\' for hit or \'s\' for stand')

                    # Hit
                    if ans == 'h':
                        player.hand.append(deck.pop())
                    
                    # if stand, let dealer take turn
                    else:
                        print_round_info('You stand')
                        sleep(SLEEP_TIME)
                        player_turn = False
                        
                # End player turn
                if not player_turn:
                    print_round_info('Dealer\'s turn...')
                    sleep(SLEEP_TIME)
                    continue

            # Dealer's turn
            else:
                dealer_hit_last_turn = False

                # If player has blackjack
                if player.hand.is_blackjack():
                    #sleep(2)
                    break

                # Check for bust
                elif dealer.hand.is_bust():
                    print_round_info('Dealer Busts!')
                    sleep(SLEEP_TIME)
                    break

                elif dealer.hand.is_blackjack():
                    print_round_info('Dealer has Blackjack!')
                    sleep(SLEEP_TIME)
                    break       

                # If soft hand
                if dealer.hand.point_value()[1] > 0:
                    if max(dealer.hand.point_value()) < 19:
                        dealer_hit(dealer.hand, deck)
                    else:
                        print_dealer_stand()
                        break # Stand

                # If hand value is 17 or higher, then stand
                elif max(dealer.hand.point_value()) >= 17:
                    print_dealer_stand()
                    break # Stand

                # Check player's upcard
                elif player.hand.cards[0].point_value() <= 6 and dealer.hand.point_value()[0] >= 13:
                    print_dealer_stand()
                    break # Stand
                
                else:
                    dealer_hit(dealer.hand, deck)
        
        # End of round. Determine winner
        # 0 = dealer win
        # 1 = player win
        # 2 = push
        if not (dealer.hand.is_bust() or player.hand.is_bust()):
            
            if player.hand.is_blackjack():
                # If dealer has blackjack, it's a push
                if dealer.hand.is_blackjack():
                    result = 2
                else:
                    result = 1

            elif dealer.hand.is_blackjack():
                result = 0

            else:
                if max(dealer.hand.point_value()) > max(player.hand.point_value()):
                    result = 0
                elif max(player.hand.point_value()) > max(dealer.hand.point_value()):
                    result = 1
                elif max(player.hand.point_value()) == max(dealer.hand.point_value()):
                    result = 2

            if result == 0:
                print_round_info("Dealer wins!")
                print(troll)
            elif result == 1:
                print_round_info("You win!")
            elif result == 2:
                print_round_info("Push!")

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
            deck += player.hand.cards
            del player.hand
            deck += dealer.hand.cards
            del dealer.hand
