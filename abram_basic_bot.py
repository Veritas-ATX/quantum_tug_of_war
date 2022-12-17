from typing import List, Optional
import numpy as np
import random
from GamePlayer import *

'''
Finds which basic state (ket 0,1,+,-) the current state is closest to
Based on the closest state, the strategy will play specific cards based on getting the state closer to the team state
For example, if we're on team 0 and current state is closest to 1, play X card if we have one
Percent win as team 0: 55.41%
Percent win as team 1: 54.37%
'''

class AbramStrategy(GameBot):
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
        self.round = 0
        self.dealt_count = 0
        self.hand_size = 0
        
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
        if self.round == 0 and team == 1:
            self.update_team(prev_turn, 0)
        elif self.round > 0:
            self.update_with_prev(prev_turn, team)
        # Increment round counter
        self.round += 1
        # Check if we were dealt cards and update counters
        if len(hand) > self.hand_size:
            self.dealt_count += len(hand) - self.hand_size
            self.hand_size = len(hand)
        # If not near end of game or at hand limit, hoard cards
        if self.hand_size < 5 and self.round <= 100:
            return None
        
        # burn off duplicates
        if self.hand_size == 5 and self.round <= 100:
            if hand.count(GameAction.REVERSE) > 1:
                return GameAction.REVERSE
            elif hand.count(GameAction.PAULIZ) > 1:
                return GameAction.PAULIZ
            elif hand.count(GameAction.HADAMARD) > 1:
                return GameAction.HADAMARD   
            elif hand.count(GameAction.PAULIX) > 1:
                return GameAction.PAULIX
            elif hand.count(GameAction.MEASURE) > 1:
                return GameAction.MEASURE
        
        best_action = None
        
        # calculating closeness to all of the corner states
        # closeness = [zero, one, plus, minus]
        closeness = [0,0,0,0]
        closeness[0] = (self.state[0]-1)**2+(self.state[1]-0)**2
        closeness[1] = (self.state[0]-0)**2+(self.state[1]-1)**2
        closeness[2] = (self.state[0]-np.sqrt(0.5))**2+(self.state[1]-np.sqrt(0.5))**2
        closeness[3] = (self.state[0]-np.sqrt(0.5))**2+(self.state[1]+np.sqrt(0.5))**2
        
        # get index of smallest distance
        closest = closeness.index(min(closeness))
        
        # if current state is nearest to ket 0
        if closest == 0:
            
            if team == 0:
                # do nothing
                pass 
            elif team == 1:
                # If we have an X, play it
                if GameAction.PAULIX in hand:
                    best_action = GameAction.PAULIX
                # As a backup play Hadamard
                elif GameAction.HADAMARD in hand:
                    best_action = GameAction.HADAMARD
                    
        # if current state is nearest to ket 1
        elif closest == 1:
            
            if team == 0:
                # If we have an X, play it
                if GameAction.PAULIX in hand:
                    best_action = GameAction.PAULIX
                # As a backup play Hadamard
                elif GameAction.HADAMARD in hand:
                    best_action = GameAction.HADAMARD
            elif team == 1:
                # do nothing
                pass 
            
        # if current state is nearest to ket plus
        elif closest == 2:
            
            if team == 0:
                # If we have a Hadamard, play it
                if GameAction.HADAMARD in hand:
                    best_action = GameAction.HADAMARD
            elif team == 1:
                # if we have a Z, play it
                if GameAction.PAULIZ in hand:
                    best_action = GameAction.PAULIZ
                # if we have a Hadamard and a X, play the Hadamard
                if GameAction.HADAMARD in self.hand and GameAction.PAULIX in self.hand:
                    best_action = GameAction.HADAMARD
         
        # if current state is nearest to ket minus
        else:
            if team == 0:
                # if we have a Z, play it
                if GameAction.PAULIZ in hand:
                    best_action = GameAction.PAULIZ
                # if we have a Hadamard and a X, play the Hadamard
                if GameAction.HADAMARD in self.hand and GameAction.PAULIX in self.hand:
                    best_action = GameAction.HADAMARD
            elif team == 1:
                # If we have a Hadamard, play it
                if GameAction.HADAMARD in hand:
                    best_action = GameAction.HADAMARD
        
        return best_action
