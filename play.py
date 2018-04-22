from __future__ import division
import itertools
import pprint
import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd
import argparse

def create_deck(num_types=3, num_properties=4):
    cards = []
    for card in itertools.product(range(num_types), repeat=num_properties):
        cards.append(card)
    return cards

def is_set(cards):
    num_types = len(cards)
    num_properties = len(cards[0])
    properties = zip(*cards)
    for p in properties:
        num_distinct = len(set(p))
        is_allowed = (num_distinct==1) or (num_distinct==num_types)
        if not is_allowed:
            return False
    return True

def play_game(num_types=3, num_properties=4, num_shown=12, num_flip=3):
    deck = create_deck(num_types, num_properties)
    random.shuffle(deck)
    shown = set([deck.pop() for i in range(num_shown)])
    rounds = []
    while True:
        allowed = []
        for comb in itertools.combinations(shown, num_types):
            if is_set(comb):
                allowed.append(comb)
        state = {
                'shown': len(shown),
                'sets': len(allowed),
                'deck': len(deck),
        }
        rounds.append(state)

        # game over
        if len(allowed)==0 and len(deck)==0:
            return rounds

        # found a set
        if len(allowed)>0:
            chosen = set(random.choice(allowed))
            shown -= chosen

        # draw cards
        if (len(shown) < num_shown) or len(allowed)==0:
            for i in range(num_flip):
                if len(deck)>0:
                    card = deck.pop()
                    shown.add(card)

def play_games(num_games=10):
    random.seed(123456)
    num_types = 3
    num_properties = 4
    num_shown = 12
    num_flip = 3
    raw_games = []
    for i in range(num_games):
        print(i)
        rounds = play_game(num_types=num_types, num_properties=num_properties, num_shown=num_shown, num_flip=num_flip)
        for j,r in enumerate(rounds):
            r['game'] = i
            r['round'] = j
        raw_games.extend(rounds)
    games = pd.DataFrame(raw_games)
    return games

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='The SET game simulator')
    parser.add_argument('--num-games', type=int, required=True, nargs=1, help='Number of games to play')
    args = parser.parse_args()
    num_games = args.num_games[0]
    games = play_games(num_games=num_games)
    games.to_csv('games.csv', index=False)
