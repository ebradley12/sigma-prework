# Import Modules
import random
from collections import deque

# Constant Global Variables
WILD_4 = 'Wild 4'
WILD = 'Wild'
RED = 'Red'
BLUE = 'Blue'
GREEN = 'Green'
YELLOW = 'Yellow'
PLUS_2 = '+2'
SKIP = 'Skip'
REVERSE = 'Reverse'

# Build Deck
def build_deck():
  colours = [RED, BLUE, GREEN, YELLOW]
  values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, PLUS_2, SKIP, REVERSE]
  cards = []
  for colour in colours:
    for value in values:
      card = f'{colour} {value}'
      if value != 0:
        cards.append(card)
        cards.append(card)
      else:
        cards.append(card) 
  wild_cards = [WILD_4, WILD_4, WILD_4, WILD_4, WILD, WILD, WILD, WILD]
  deck = cards + wild_cards
  return deck

# Shuffle deck
def shuffle_deck(deck):
  return random.sample(deck, len(deck))

# Create list of players
def create_players():
  players = []
  no_of_players = int(input('How many players?: '))
  while no_of_players < 2 or no_of_players > 6:
    no_of_players = int(input('INVALID! Please enter a number between 2 and 4: '))
  for i in range(no_of_players):
    player = input(f'Enter player {i+1} name: ').title()
    players.append(player)
  return players

# Deal x cards 
def deal_cards(x_cards):
  cards_dealt = []
  for i in range(x_cards):
    card = uno_deck.pop(0)
    cards_dealt.append(card)
  return cards_dealt

# View player's hand of cards
def view_hand(player):
  return print(f"{player}'s hand: {players_dict[player]}")

# Determine whether player can go
def can_play(player):
  if WILD in players_dict[player] or WILD_4 in players_dict[player]:
    return True 
  else:
    if discarded_pile[-1] == WILD or discarded_pile[-1] == WILD_4:
      return False
    else:
      split_topcard = discarded_pile[-1].split(' ')
      split_card_list = []
      if len(split_topcard) == 2:
        colour = split_topcard[0]
        value = split_topcard[1]
      else:
        colour = split_topcard[2]
        value = None
      for card in players_dict[player]:
        split_card = card.split(' ')
        split_card_list += split_card   
      if value in split_card_list or colour in split_card_list:
        return True
      return False
      
# Choose card from deck
def choose_card(player):
  card = input(f'{player}, which card would you like to play? : ').title()
  return card
  
# Play card and ask player to choose colour if Wild card played
def play_card(card, player):
  if card in players_dict[player]:
    players_dict[player].remove(card)
    discarded_pile.append(card)
    if card == WILD:
      new_colour = input('What colour do you choose?: ').title()
      discarded_pile[-1] += f' {new_colour}'
      print(f'{player} played a {card}. The new colour is {new_colour}.')
    elif card == WILD_4:
      new_colour = input('What colour do you choose?: ').title()
      discarded_pile[-1] += f' {new_colour}'
      print(f'{player} played a {card}. The new colour is {new_colour}. Next player must draw 4 cards.')
    else:
      print(f'{player} played a {card}')
  else:
    print('Invalid card! Please try again')
    return False

# Check for special card on the discarded pile
def check_for_special_card(card, play_direction, current_player):
  if WILD_4 in card:
      print(f'{current_player} must draw 4 cards.')
      players_dict[current_player] += deal_cards(4)
  elif card != WILD and card != WILD_4:
    split_card = card.split(' ')
    value = split_card[1]
    if value == PLUS_2:
      print(f'{current_player} must draw 2 cards.')
      players_dict[current_player] += deal_cards(2)
    elif value == REVERSE:
      play_direction *= -1
      current_player = skip_player(players, play_direction)
      current_player = skip_player(players, play_direction)
      print('Direction of play has been reversed!')
      print(f"It's now {current_player}'s turn!")
    elif value == 'Skip':
      print(f'{current_player} has been skipped!')
      print("Move on to the next player.")
      current_player = skip_player(players, play_direction)
    return current_player, play_direction
    
# Skip player 
def skip_player(players, play_direction):
  if play_direction == 1:
    players.rotate(-1)
  else:
    players.rotate(1)
  current_player = players[0]
  return current_player

# Reshuffle the discarded pile
def reshuffle_discarded_pile(uno_deck):
  uno_deck.extend(discarded_pile)
  discarded_pile.clear()
  uno_deck = shuffle_deck(uno_deck)
  return uno_deck

# Valdidate card played
def validate_play(card):
  if card == WILD or WILD_4:
    return True
  else:
    split_topcard = discarded_pile[-1].split(' ')
    if len(split_topcard) == 2:
      colour = split_topcard[0]
      value = split_topcard[1]
    else:
      colour = split_topcard[-1]
      value = split_topcard[0]
    if value in str(card) or colour in str(card):
      return True
    return False 

# Main Game
uno_deck = build_deck()
uno_deck = shuffle_deck(uno_deck)
players = create_players()
players = deque(players)
all_players_hands = []
for player in players:
  players_hand = deal_cards(7)
  all_players_hands.append(players_hand)
players_dict = dict(zip(players, all_players_hands))
discarded_pile = []
discarded_pile.append(uno_deck.pop(0))
current_player = players[0]
play_direction = 1
playing = True

while playing:
  print(f'Card on top is: {discarded_pile[-1]}')
  print('---------------')
  print(f"It's {current_player}'s turn")
  current_player, play_direction = check_for_special_card(discarded_pile[-1], play_direction, current_player)
  view_hand(current_player)
  if len(uno_deck) < 4:
    reshuffle_discarded_pile(uno_deck)
  if can_play(current_player):
    card = choose_card(current_player)
    while not validate_play(card):
      print("Invalid card - try again!")
      card = choose_card(current_player)
    play_card(card, current_player)
    if len(players_dict[current_player]) == 1:
      print('---------------')
      print(f'{current_player} has UNO!')
      print('---------------')
    elif len(players_dict[current_player]) == 0:
      playing = False
      print('---------------')
      print(f'{current_player} has won! Game over!')
      print('---------------')
      break
  else:
    print("Sorry, you can't play! Draw 1 card.")
    players_dict[current_player] += deal_cards(1)
  print('---------------')
  if play_direction == 1:
    players.rotate(-1)
  else:
    players.rotate(1)
  current_player = players[0]