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

BET_AMOUNTS = (100, 200, 500, 1000)

class Player():
    def __init__(self):
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
    dealer_hand.print()
    print()

    print("You:")
    player.hand.print()

    print()
    sys.stdout.write(status)
    sys.stdout.flush()

def prompt_bet(player):
    
    bet_choices = [b for b in BET_AMOUNT if b < player.bankroll.balance]
    bet_choices.append('Max')

    # Construct bet choice menu
    bet_menu = 'Possible bets: '
    i = 0
    # Only add choices that the player can afford
    for b in BET_AMOUNT:
        if (player.bankroll.balance < b):
            bet_choice_string += '({}....{}    '.format(i+1, b)

    bet_choice_string += '({}){}'.format(len(b_))

    bet_prompt_str = 'Place Bet: 
    while True:
        ans = input('Place Bet: ')
        if ans.lower() in ('h', 's'):
            break
        else:
            print('invalid response. Please pick \'h\' for hit or \'s\' for stand')

if __name__== '__main__':
    
    # Create player
    player = Player()
    
    # Create deck
    deck = generate_deck()

    # Begin Round
    while True:
        random.shuffle(deck)

        assert(len(deck) == 52)

        # Deal
        hands = deal(deck, 2, 2)

        dealer_hand = hands[0]
        dealer_hand.hide_last_card = True

        player.hand = hands[1]

        # Player's turn
        while True:
            print_round_info()

            # Collect bet
            # Find out which bet amounts are available
            # 1000, 500 200, 100
            bet = prompt_bet(player)

            # Ask to hit or stand
            while True:
                ans = input('(H)it or (S)tand? ')
                if ans.lower() in ('h', 's'):
                    break
                else:
                    print('invalid response. Please pick \'h\' for hit or \'s\' for stand')

            # Hit
            if ans == 'h':
                player.hand.append(deck.pop())
            
            # if stand, end turn
            else:
                print_round_info('You stand')
                sleep(SLEEP_TIME)
                break

            # Turn ending conditions
            if player.hand.is_bust():
                print_round_info('You Bust!')
                sleep(SLEEP_TIME)
                break

            elif player.hand.is_blackjack():
                print_round_info('You have Blackjack!')
                sleep(SLEEP_TIME)
                break

        # Dealer's turn
        dealer_hand.hide_last_card = False
        print_round_info('Dealer\'s turn...')
        sleep(SLEEP_TIME)
        while True:
            # Dealer decision logic
            # If player has blackjack
            if player.hand.is_blackjack():
                sleep(2)
                break

            if max(dealer_hand.point_value()) > max(player.hand.point_value()):
                print_dealer_stand()
                break

            # Check for bust
            elif dealer_hand.is_bust():
                print_round_info('Dealer Busts!')
                sleep(SLEEP_TIME)
                break

            elif dealer_hand.is_blackjack():
                print_round_info('Dealer has Blackjack!')
                sleep(SLEEP_TIME)
                break       

            # If soft hand
            if dealer_hand.point_value()[1] > 0:
                if max(dealer_hand.point_value()) < 19:
                    dealer_hit(dealer_hand, deck)
                else:
                    print_dealer_stand()
                    break

            # If hand value is 17 or higher, then stand
            elif max(dealer_hand.point_value()) >= 17:
                print_dealer_stand()
                break

            # Check player's upcard
            elif player.hand.cards[0].point_value() <= 6 and dealer_hand.point_value()[0] >= 13:
                print_dealer_stand()
                break
            
            else:
                dealer_hit(dealer_hand, deck)
        
        # End of round. Determine winner
        # 0 = dealer win
        # 1 = player win
        # 2 = push
        if not (dealer_hand.is_bust() or player.hand.is_bust()):
            
            if player.hand.is_blackjack():
                # If dealer has blackjack, it's a push
                if dealer_hand.is_blackjack():
                    result = 2
                else:
                    result = 1

            elif dealer_hand.is_blackjack():
                result = 0

            else:
                if max(dealer_hand.point_value()) > max(player.hand.point_value()):
                    result = 0
                elif max(player.hand.point_value()) > max(dealer_hand.point_value()):
                    result = 1
                elif max(player.hand.point_value()) == max(dealer_hand.point_value()):
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
            deck += dealer_hand.cards
            del dealer_hand
