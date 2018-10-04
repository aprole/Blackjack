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
    print("Dealer hits")
    hand.append(deck.pop())

def dealer_stand():
    print("Dealer stands")

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

        # Single Round
        while True:
            # Clear screen
            print('\n'*100, title)
            
            # Print the dealer's hand
            print("Dealer:")
            dealer_hand.print(not player_turn)

            # Print dealer hand value if it's the dealer's turn
            #if not player_turn:
            #    print('Hand Value: ', ':'.join(str(p) for p in dealer_hand.point_value()))

            print("You:")
            player_hand.print()

            # Print player hand value
            #print('Hand Value: ', ':'.join(str(p) for p in player_hand.point_value()))

            # Player's turn
            if player_turn:
                # Check for bust
                if player_hand.is_bust():
                    print('You Bust!')
                    sleep(1.5)
                    player_turn = False
                    continue  
                elif player_hand.is_blackjack():
                    print('Black Jack!')
                    sleep(1.5)
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
                    print('You stand')
                    sleep(1)
                    print('Dealer\'s turn...')
                    sleep(1.5)
                    player_turn = False
                    continue

            # Dealer's turn
            else:
                # If player has blackjack and dealer does too, it's a push, otherwise player wins
                if player_hand.is_blackjack():
                    break

                # Check for bust
                if dealer_hand.is_bust():
                    print('Dealer Busts!')
                    break

                elif dealer_hand.is_blackjack():
                    print('Dealer has Black Jack!')
                    break       

                sleep(1.5)

                # If soft hand
                if dealer_hand.point_value()[1] > 0:
                    if max(dealer_hand.point_value()) < 19:
                        dealer_hit(dealer_hand, deck)
                    else:
                        dealer_stand()
                        break # Stand

                # If hand value is 17 or higher, then stand
                elif max(dealer_hand.point_value()) >= 17:
                    dealer_stand()
                    break # Stand

                # Check player's upcard
                elif player_hand.cards[0].point_value() <= 6 and dealer_hand.point_value()[0] >= 13:
                    dealer_stand()
                    break # Stand
                
                else:
                    dealer_hit(dealer_hand, deck)

        # End of round. Determine winner

        # 0 = dealer win
        # 1 = player win
        # 2 = push
        result = 0

        if player_hand.is_blackjack():
            # If dealer has blackjack, it's a push
            if dealer_hand.is_blackjack():
                result = 2
            else:
                result = 1
        elif not dealer_hand.is_blackjack():
            if max(dealer_hand.point_value()) > max(player_hand.point_value()):
                result = 0
            elif max(player_hand.point_value()) > max(dealer_hand.point_value()):
                result = 1
            elif max(player_points) == max(dealer_points):
                result = 2

        if result == 0:
            print("You lose!")
            print(troll)
        elif result == 1:
            print("You won!")
        else:
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
