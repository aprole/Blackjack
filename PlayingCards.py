import random

class Card():
	point_map = {
		'2': 2,
		'3': 3,
		'4': 4,
		'5': 5,
		'6': 6,
		'7': 7,
		'8': 8,
		'9': 9,
		'10': 10,
		'J': 10,
		'Q': 10,
		'K': 10,
		'A': 1
	}
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit

	def __str__(self):
		return '{}{}'.format(self.rank, self.suit)

	def point_value(self):
		return Card.point_map[self.rank]

class Hand():
	
	def __init__(self, cards=[]):
		self.cards = []
		self._contains_ace = False
		self._total_points = [0, 0]

		for c in cards:
			self.append(c)

	def append(self, card):
		''' Appends a card to the hand and updates the point value of the hand. 
			The point value can be one of two values if an Ace is involved
		'''

		# Update total points
		self._total_points[0] += card.point_value()

		# If multiple interpretations (ace was already encountered)
		if self._total_points[1] > 0:
			self._total_points[1] += card.point_value()
			
			# Remove point boost since it exceeds 21
			if self._total_points[1] > 21:
				self._total_points[1] = 0


		# First Ace is encountered
		elif card.rank == 'A' and not self._contains_ace:

			self._contains_ace = True

			# Compute second interpretation and store it if it is under 21
			point_boost = self._total_points[0] + 10
			if point_boost <= 21:
				self._total_points[0] = point_boost
			
		# Append the card to the card list
		self.cards.append(card)

	def point_value(self):
		''' Returns a list of two possible point values. 
			If it is a 'soft hand' with an Ace, and the second interpretion will be the second element of the list.
		'''
		return tuple(self._total_points)

	def contains_ace(self):
		return self._contains_ace

	def is_blackjack(self):
		return self._contains_ace and max(self._total_points) == 21

	def is_bust(self):
		return max(self._total_points) > 21

	def print(self, show_last = True):
		''' Prints a visual representation of the cards, side by side overlapping. 
			Last card will be turned over if show_last == True
		 '''

		num_cards = len(self.cards)
		
		if num_cards < 2:
			return

		# Get ranks and suits for first n-1 cards
		ranks = []
		suits = []
		for i in range(len(self.cards)-1):
			ranks.append(self.cards[i].rank)
			suits.append(self.cards[i].suit)

		if show_last:
			last_card = self.cards[-1]
			last_card_lines = ['╭─────────╮',
							   '│{:<2}     {:>2}│'.format(last_card.rank, last_card.rank),
							   '│{}      {} │'.format(last_card.suit, last_card.suit),
							   '│         │',
							   '│    {}    │'.format(last_card.suit),
							   '│         │',
							   '│{}      {} │'.format(last_card.suit, last_card.suit),
							   '│{:<2}     {:>2}│'.format(last_card.rank, last_card.rank),
							   '╰─────────╯']
		else:
			last_card_lines = ['╭─────────╮',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '│░░░░░░░░░│',
							   '╰─────────╯']

		print('╭───' * (num_cards-1) + last_card_lines[0])
		print(('│{:<2} ' * (num_cards-1)).format(*ranks) + last_card_lines[1])
		print(('│{}  ' * (num_cards-1)).format(*suits) + last_card_lines[2])
		print('│   ' * (num_cards-1) + last_card_lines[3])
		print( '│   ' * (num_cards-1) + last_card_lines[4])
		print('│   ' * (num_cards-1) + last_card_lines[5])
		print(('│{}  ' * (num_cards-1)).format(*suits) + last_card_lines[6])
		print(('│{:<2} ' * (num_cards-1)).format(*ranks) + last_card_lines[7])
		print('╰───' * (num_cards-1) + last_card_lines[8])

		# Print hand value
		if show_last:
			print('Hand Value: ', ':'.join(str(p) for p in self.point_value() if p > 0))

		print()
		

# def print_hand(cards, show_last = True):
# 	# print a visual representation of the cards, side by side overlapping 

# 	if len(cards) < 2:
# 		return

# 	num_cards = len(cards)

# 	# Get ranks and suits
# 	ranks = []
# 	suits = []
# 	for i in range(len(cards)-1):
# 		ranks.append(cards[i].rank)
# 		suits.append(cards[i].suit)

# 	if show_last:
# 		last_card = cards[len(cards) - 1]
# 		last_card_lines = ['╭─────────╮',
# 						   '│{:<2}     {:>2}│'.format(last_card.rank, last_card.rank),
# 						   '│{}      {} │'.format(last_card.suit, last_card.suit),
# 						   '│         │',
# 						   '│    {}    │'.format(last_card.suit),
# 						   '│         │',
# 						   '│{}      {} │'.format(last_card.suit, last_card.suit),
# 						   '│{:<2}     {:>2}│'.format(last_card.rank, last_card.rank),
# 						   '╰─────────╯']
# 	else:
# 		last_card_lines = ['╭─────────╮',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '│░░░░░░░░░│',
# 						   '╰─────────╯']

# 	print('╭───' * (num_cards-1) + last_card_lines[0])
# 	print(('│{:<2} ' * (num_cards-1)).format(*ranks) + last_card_lines[1])
# 	print(('│{}  ' * (num_cards-1)).format(*suits) + last_card_lines[2])
# 	print('│   ' * (num_cards-1) + last_card_lines[3])
# 	print( '│   ' * (num_cards-1) + last_card_lines[4])
# 	print('│   ' * (num_cards-1) + last_card_lines[5])
# 	print(('│{}  ' * (num_cards-1)).format(*suits) + last_card_lines[6])
# 	print(('│{:<2} ' * (num_cards-1)).format(*ranks) + last_card_lines[7])
# 	print('╰───' * (num_cards-1) + last_card_lines[8])
	

	
def generate_deck():
	deck = [Card(rank, suit) for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q', 'A'] for suit in ['♠', '♦', '♥', '♣']]
	random.shuffle(deck)
	return deck

def deal(deck, num_hands, num_cards):
	hands = []
	for _ in range(num_hands):
		cards = []
		for _ in range(num_cards):
			cards.append(deck.pop())
		hands.append(Hand(cards))

	return hands
