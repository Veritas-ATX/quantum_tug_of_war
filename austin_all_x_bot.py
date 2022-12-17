from typing import List, Optional
import numpy as np
import random
from GamePlayer import *

'''
Ideal Hand Bot
Attempts to get some defined Ideal Hand (in this case 5 X's)
vs. Random Bot 10000 games:
Percent win as team 0: 81.85%
Percent win as team 1: 89.1%
'''
class MyStrategy_IdealHand(GameBot):
    '''
        Initialize your bot here. The init function must take in a bot_name.
        You can use this to initialize any variables or data structures
        to keep track of things in the game
    '''
    def __init__(self, bot_name):
        self.bot_name = bot_name        #do not remove this
        self.state = np.array([np.sqrt(0.5), np.sqrt(0.5)])
        self.direction = 1
        self.theta = float(2*np.pi/100.0)
        self.test_state = np.array([np.sqrt(0.5), np.sqrt(0.5)])
        self.test_direction = 1
        self.dealt_count = 0
        self.hand_size = 0
        self.action_dict = {'X': GameAction.PAULIX,
                            'Z': GameAction.PAULIZ, 
                            'H': GameAction.HADAMARD, 
                            'R': GameAction.REVERSE, 
                            'M': GameAction.MEASURE}
        
    def rotate(self, state, direction):
        theta = float(self.theta * direction)
        rotate = np.array([[np.cos(theta / 2), -np.sin(theta / 2)], 
                           [np.sin(theta / 2), np.cos(theta / 2)]])
        state = np.dot(rotate, state)
        return state

    def update_state(self, action, state, direction):
        if action == GameAction.PAULIX:
            X = np.array([[0, 1], [1, 0]])
            state = np.dot(X, state)
        elif action == GameAction.PAULIZ:
            Z = np.array([[1, 0], [0, -1]])
            state = np.dot(Z, state)
        elif action == GameAction.HADAMARD:
            H = np.array([[np.sqrt(1/2), np.sqrt(1/2)], [np.sqrt(1/2), -np.sqrt(1/2)]])
            state = np.dot(H, state)
        elif action == GameAction.REVERSE:
            direction *= -1
        return state, direction
            
    def update_team(self, prev_turn, team):
        prev_action = prev_turn[f'team{team}_action']
        prev_measurement = prev_turn[f'team{team}_measurement']
        if prev_action is not None:
            if prev_action == GameAction.MEASURE:
                self.state = prev_measurement
            else:
                self.state, self.direction = self.update_state(prev_action, self.state, self.direction)
        
    def update_with_prev(self, prev_turn, team):
        # Update state array based on previous turn
        if team == 0:
            self.update_team(prev_turn, 0)
            self.update_team(prev_turn, 1)
            self.state = self.rotate(self.state, self.direction)
        else:
            self.update_team(prev_turn, 1)
            self.state = self.rotate(self.state, self.direction)
            self.update_team(prev_turn, 0)
            
    def try_action(self, action, team):
        # Update test state/direction depending on action tried
        # If a measurement, pretends equivalent to passing
        self.test_state, self.test_direction = self.update_state(action, self.test_state, self.test_direction)
        # Rotate test qubit (this assumes your opponent does nothing if you are team 0)
        self.test_state = self.rotate(self.test_state, self.test_direction)
        # Get the 0 state probability p if team 0, 1-p for team 1
        probability = self.test_state[0]**2
        if probability < 0:
            probability = 0
        elif probability > 1:
            probability = 1
        if team == 1:
            probability = 1 - probability
        return probability

    def play_action(self,
                    team: int,
                    round_number: int,
                    hand: List[GameAction],
                    prev_turn: List) -> Optional[GameAction]:
        ##### IMPLEMENT AWESOME STRATEGY HERE ##################
        # Update qubit state based on prev round
        if round_number == 0 and team == 1:
            self.update_team(prev_turn, 0)
        elif round_number > 0:
            self.update_with_prev(prev_turn, team)
        # Check if we were dealt cards and update counters
        if len(hand) > self.hand_size:
            self.dealt_count += len(hand) - self.hand_size
            self.hand_size = len(hand)
        # Specify the Ideal Hand mix of cards
        min_target_hand = {'X': 5, 'Z': 0, 'H': 0, 'R': 0, 'M': 0}
        hand_dict = {'X': hand.count(GameAction.PAULIX),
                     'Z': hand.count(GameAction.PAULIZ),
                     'H': hand.count(GameAction.HADAMARD), 
                     'R': hand.count(GameAction.REVERSE), 
                     'M': hand.count(GameAction.MEASURE)}
        # If not near end of game or at hand limit, hoard cards
        if round_number <= 98 and self.hand_size < 5:
            return None
        # Get the actions that we have too many of
        want_to_play = [self.action_dict[key] for key,value in hand_dict.items() if value > min_target_hand[key]]
        # Test out actions in hand for max win prob (and passing)
        # Treats game as if ending and only plans one step ahead
        # If late in game, play whatever gives best win prob and consider passing
        check_none = False
        if round_number > 98:
            want_to_play = hand
            check_none = True
        # Play measure if more than desired or >98 rounds
        # since below code never picks it over passing
        if GameAction.MEASURE in want_to_play:
            self.hand_size -= 1
            return GameAction.MEASURE
        best_prob = 0
        best_action = None
        for i in range(len(want_to_play)+1):
            if i == len(want_to_play):
                action = None
                if not check_none:
                    continue
            else:
                action = want_to_play[i]
            self.test_state = np.copy(self.state)
            self.test_direction = self.direction
            temp_prob = self.try_action(action, team)
            if temp_prob > best_prob:
                best_prob = temp_prob
                best_action = action
        if best_action is not None:
            self.hand_size -= 1
        return best_action
    #######################################################
