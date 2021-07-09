import random
from itertools import product

MAX_PLAYER_CARD = 3
MAX_CARD_DRAWN = 5
SUITES = ['heart', 'diamond', 'spade', 'club']
# VALUES = ['2', 'Q', 'K']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def create_deck(exclude=''):
    deck = []
    for suite, value in product(SUITES, VALUES):
        card = f'{suite[0].upper()}{value}'
        if card != exclude:
            deck.append(card)
    return deck


def ask_player_for_card():
    print(
        '\nYou can enter your card choice as "SV"'
        '\nWhere S is the suite (H - Heart, D - Diamond, C - Club, S - Spade)'
        '\nWhere V is the value from (2 to 10 and J - Jack, Q - Queen, K - King, A - Ace)'
        '\nEg.'
        '\n > you want 3 of Diamond your input would be D3'
        '\n > you want Ace of Club your input would be CA'
        '\nso if you are given 3 cards you need to input as `H2,DK,SQ`'
    )
    while True:
        cards = input(f'Please enter your {MAX_PLAYER_CARD} card choice/s: ')
        cards = cards.split(',')
        if len(cards) == MAX_PLAYER_CARD:
            # do some whitespace clean up
            cards = [c.strip() for c in cards]
            break

    return cards


def main():
    player_cards = ask_player_for_card()
    print('\n----------------------------------------------------')
    print(f'Your Cards: {player_cards}')

    # deck = create_deck()
    deck = create_deck(exclude=random.choice(player_cards))
    drawn_cards = []

    for counter in range(MAX_CARD_DRAWN):
        random.shuffle(deck)
        drawn_card = deck.pop()
        drawn_cards.append(drawn_card)

        print(f'draw {counter + 1} is {drawn_card} {"matched" if drawn_card in player_cards else "nope"}')

    print('You Lose')


if __name__ == '__main__':
    main()
