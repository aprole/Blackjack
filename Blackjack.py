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

SLEEP_TIME = 2.5

BET_AMOUNTS = (100, 200, 500, 1000)

class Player():
    def __init__(self):
        self.bankroll = Bankroll(2000)

    # def place_bet(self, bet_amt):
    #     try:
    #         self.bankroll.withdraw(bet_amt)
    #     except:
    #         print('Insufficient funds')
    #         return False
    #     else:
    #         self._bet_amt = bet_amt
    #     return True

    # def bet_amt(self):
    #     return self._bet_amt


class InsufficientFundsException(Exception):
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
    round.print_info('Dealer hits')
    sleep(SLEEP_TIME)

def print_dealer_stand():
    round.print_info('Dealer stands')
    sleep(SLEEP_TIME)

def print_round_info(dealer_hand, player, status = ''):
    # Clear screen
    print('\n'*100, title)
    
    # Print dealer info
    print("Dealer:")
    dealer_hand.print()
    print()

    print("You:")
    player.hand.print()

    print('Balance: ${:.2f}'.format(player.bankroll.balance()))

    print()
    sys.stdout.write(status)
    sys.stdout.flush()

def prompt_bet(player):
    ''' Prompts player for bet. Returns bet amount '''

    # Create a list of betting choices for the player, and a string representation of it
    bet_choices = []
    bet_menu = 'Possible bets:\n'
    for i, b in enumerate(BET_AMOUNTS):
        if b <= player.bankroll.balance():
            bet_choices.append(b)
            bet_menu += '    {}.... ${:.2f}\n'.format(i+1, b)
        else:
            break

    # Add the maximium amount the player can bet. No more than the max(BET_AMOUNTS)
    bet_choices.append(min(player.bankroll.balance(), max(BET_AMOUNTS)))
    bet_menu += '    {}.... Maximum bet: ${:.2f}'.format(len(bet_choices), bet_choices[-1])

    bet_prompt_str = 'Place Bet: '
    choice = 0
    while True:
        print(bet_menu, '\n')
        try:
            choice = int(input('Please choose a betting option: '))
        except:
            print("Invalid response. Choose a number from the betting menu.")
        else:
            if (choice < 1 or choice > len(bet_choices)):
                print('Number is not in the list')
            else:
                break

    return bet_choices[choice - 1]

class Round():
    def __init__(self, dealer_hand, player, bet):
        self.bet = bet
        self.player = player
        self.dealer_hand = dealer_hand

    def print_info(self, status = ''):
        ''' Prints the round info '''
        # Clear screen
        print('\n'*100, title)
        
        # Print dealer info
        print("Dealer:")
        self.dealer_hand.print()
        print()

        print("You:")
        self.player.hand.print()

        print('Bet: ${:.2f}'.format(self.bet))
        print('Balance: ${:.2f}'.format(self.player.bankroll.balance()))

        print()
        sys.stdout.write(status)
        sys.stdout.flush()

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

        # Print title
        print('\n'*100, title, '\n')
        # Print player balance
        print('Balance: ${:.2f}'.format(player.bankroll.balance()), '\n')
    
        # Collect bet
        bet = 0
        while True:
            try:
                bet = prompt_bet(player)
                player.bankroll.withdraw(bet)
            except InsufficientFundsException:
                print('Insufficient funds')
            else:
                break

        round = Round(dealer_hand, player, bet)

        # Player's turn
        while True:
            round.print_info()

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
                round.print_info('You stand')
                sleep(SLEEP_TIME)
                break

            # Turn ending conditions
            if player.hand.is_bust():
                round.print_info('You Bust!')
                sleep(SLEEP_TIME)
                break

            elif player.hand.is_blackjack():
                round.print_info('You have Blackjack!')
                sleep(SLEEP_TIME)
                break

        # Dealer's turn
        dealer_hand.hide_last_card = False

        # If player has blackjack
        if player.hand.is_blackjack():
            # Show dealers card
            round.print_info()
            sleep(2)
        else:
            round.print_info('Dealer\'s turn...')
            sleep(SLEEP_TIME)
            while True:
                # check for turn ending conditions
                if dealer_hand.is_blackjack():
                    round.print_info('Dealer has Blackjack!')
                    sleep(SLEEP_TIME)
                    break 

                elif dealer_hand.is_bust():
                    round.print_info('Dealer Busts!')
                    sleep(SLEEP_TIME)
                    break

                # Dealer decision logic
                # Dealer must hit if below 17
                if max(dealer_hand.point_value()) < 17:
                    dealer_hit(dealer_hand, deck)
                else:
                    print_dealer_stand()
                    break

                # If soft hand
                # if dealer_hand.point_value()[1] > 0:
                #     if max(dealer_hand.point_value()) < 19:
                #         dealer_hit(dealer_hand, deck)
                #     else:
                #         print_dealer_stand()
                #         break

                # If hand value is 17 or higher, then stand
                # elif max(dealer_hand.point_value()) >= 17:
                #     print_dealer_stand()
                #     break

                # # Check player's upcard
                # elif player.hand.cards[0].point_value() <= 6 and dealer_hand.point_value()[0] >= 13:
                #     print_dealer_stand()
                #     break
                
                # else:
                #     dealer_hit(dealer_hand, deck)
        
        # End of round. Determine if the player wins or pushes
        # 0 = nothing
        # 1 = player win
        # 2 = push
        # 3 = player has blackjack

        if player.hand.is_blackjack():
            if dealer_hand.is_blackjack():
                result = 2
                
            else:
                result = 1
                reward = round.bet + round.bet * 3/2
        elif dealer_hand.is_blackjack():
            result = 0

        elif player.hand.is_bust():            
            result = 0

        elif dealer_hand.is_bust():
            result = 1

        else:
            if max(dealer_hand.point_value()) > max(player.hand.point_value()):
                result = 0
            elif max(player.hand.point_value()) > max(dealer_hand.point_value()):
                result = 1
            elif max(player.hand.point_value()) == max(dealer_hand.point_value()):
                result = 2

        if result == 0:
            round.print_info('You lost :(')
        elif result == 1:
            reward = 2*round.bet
            player.bankroll.deposit(reward)
            round.print_info("You win!")
        elif result == 2:
            reward = round.bet
            player.bankroll.deposit(reward)
            round.print_info("Push!")
        elif result == 3:
            reward = round.bet + round.bet * 3/2
            player.bankroll.deposit(reward)
            round.print_info("You win!")

        # Print new line
        print()

        # Ask to play again
        if player.bankroll.balance() == 0:
            print(troll)
            print('You ran out of funds. Game over!')
            break

        while True:
            ans = input("Play another round? (y/n): ")
            if ans.lower() in ('y', 'n'):
                break

        if ans == 'n':
            print('Thanks for playing Blackjack, goodbye!')
            break

        else:
            # Add cards back to deck
            deck += player.hand.cards
            del player.hand
            deck += dealer_hand.cards
            del dealer_hand
