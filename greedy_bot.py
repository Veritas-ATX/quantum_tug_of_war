from typing import List, Optional
import numpy as np
import random
from GamePlayer import *

'''
Insert high-level explanation of your strategy here. Why did you design this strategy?
When should it work well, and when should it have trouble?

- order of a turn
-- team 0 makes move
-- team 1 makes move
-- new cards are dealt
-- rotation is applied

- keep track of
-- current state
-- anticipated next round state only based on rotation
-- projected state in round 99 / last round, based on rotation

---

- in each round decide to keep/let go card if anticipated new card will benefit anticipated end state
- in each round decide to play cards if anticipated end state having played card is higher than without


- random bot strategy: 
-- basic: only keep Xs, apply X in ultimate round iff our winning prob is lower than half
-- advanced: anticipate final state a few rounds before end, and apply gates to maximize our chances

- if we could measure in the (3rd last) penultimate round, and have X (2xH and Z) then can change to our state

- a) if we have last turn: can turn any state to our favor if we have X or Z
- b) if we do not have last turn: ?
-- could predict what the other team will do, and do what we can to maximize our probability

- overtime: see what current state is, if it is favorable for us do nothing, if not wait until opponent plays their last action and act afterwards (if still possible)
-- somehow anticipate what for how many rounds in each round we can state turn to our favor, 
'''
class GreedyBot(GameBot):

    '''
        Initialize your bot here. The init function must take in a bot_name.
        You can use this to initialize any variables or data structures
        to keep track of things in the game
    '''
    def __init__(self,bot_name):
        self.bot_name = bot_name        #do not remove this
        self.basis_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        self.state = self.basis_state
        self.anticipated_state = self.basis_state
        self.direction = 1
        self.theta = 2*np.pi/100.0
        self.X = np.array([[0, 1], [1, 0]])
        self.Z = np.array([[1, 0], [0, -1]])
        self.H = np.array([[np.sqrt(1/2), np.sqrt(1/2)], [np.sqrt(1/2), -np.sqrt(1/2)]])
        self.action_dict = {"X": GameAction.PAULIX, 
                        "Z": GameAction.PAULIZ,
                        "H": GameAction.HADAMARD, 
                        "R": GameAction.REVERSE, 
                        "M": GameAction.MEASURE, }
        
        self.state = np.array([np.sqrt(0.5), np.sqrt(0.5)])
        self.direction = 1
        self.theta = float(2*np.pi/100.0)
        self.test_state = np.array([np.sqrt(0.5), np.sqrt(0.5)])
        self.test_direction = 1
        self.round = 0
        self.dealt_count = 0
        self.hand_size = 0
        
    ## OLD
    def get_rotation(self, sign):
        return np.array([[np.cos(sign*self.theta / 2), -np.sin(sign*self.theta / 2)], [np.sin(sign*self.theta / 2), np.cos(sign*self.theta / 2)]])
    
    def update_state_old(self, prev_turn):
        #print(prev_turn)            
        keys = ["team0_action", "team1_action"]
        for key in keys:
            #print("update:",type(prev_turn[key]), prev_turn[key]=="X", prev_turn[key] is GameAction.PAULIX)
            action = None
            if prev_turn[key] == GameAction.PAULIZ:
                print(" doing Z")
                action = self.Z
            elif prev_turn[key] == GameAction.PAULIX:
                #print(" doing X")
                action = self.X
            elif prev_turn[key] == GameAction.HADAMARD:
                #print(" doing H")
                action = self.H
            elif prev_turn[key] == GameAction.REVERSE:
                #print("reversed direction from ", self.direction, " to ",-1*self.direction)
                self.direction = -1 * self.direction
                
            elif prev_turn[key] == GameAction.MEASURE:
                print(" doing M, setting:",prev_turn[key.split("_")[0]+"_measurement"])
                self.state = prev_turn[key.split("_")[0]+"_measurement"]
                
            if type(action) is not None and not np.any(action==None):
                #print(action)
                self.state = action @ self.state
        
        self.state = self.get_rotation(self.direction) @ self.state
        self.anticipated_state = self.get_rotation(self.direction) @ self.state
    
    ## AMENDMENDTS
    
    # anticipate the state at the beginning of the next round based on rotation and optional gates before and after
    def anticipate_next_state(self, before_rotation=None, rotation=True, after_rotation=None):
        ant_state = self.state.copy()
        ant_direction = self.direction
        if before_rotation is not None:
            ant_state, ant_direction = self.update_state(before_rotation, ant_state, ant_direction, verbose=False)
        if rotation is True:
            ant_state = self.rotate(ant_state, ant_direction)
            #print(ant_state)
        if after_rotation is not None:
            ant_state, ant_rotation = self.update_state(after_rotation, ant_state, ant_direction, verbose=False)
        self.anticipated_state = ant_state
    
    # pick best 
    #def 
    
    ## AUSTIN's code
    def rotate(self, state, direction):
        theta = float(self.theta * direction)
        rotate = np.array([[np.cos(theta / 2), -np.sin(theta / 2)], 
                           [np.sin(theta / 2), np.cos(theta / 2)]])
        state = np.dot(rotate, state)
        return state

    def update_state(self, action, state, direction, verbose=False):
        print("\t action:", action) if verbose is True else ""
        if action == GameAction.PAULIX:
            X = np.array([[0, 1], [1, 0]])
            state = np.dot(X, state)
            #print("\t", state)
        elif action == GameAction.PAULIZ:
            Z = np.array([[1, 0], [0, -1]])
            state = np.dot(Z, state)
            #print("\t", state)
        elif action == GameAction.HADAMARD:
            H = np.array([[np.sqrt(1/2), np.sqrt(1/2)], [np.sqrt(1/2), -np.sqrt(1/2)]])
            state = np.dot(H, state)
            #print("\t", state)
        elif action == GameAction.REVERSE:
            #print("\t reversing")
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
    
    
    
    def try_action(self, action, team, assume_last=True):
        # Update test state/direction depending on action tried
        # If a measurement, pretends equivalent to passing
        self.anticipate_next_state(before_rotation=action)
        #self.test_state, self.test_direction = self.update_state(action, self.test_state, self.test_direction)
        # Rotate test qubit (this assumes your opponent does nothing if you are team 0)
        #self.test_state = self.rotate(self.test_state, self.test_direction)
        # Get the 0 state probability p if team 0, 1-p for team 1
        probability = self.anticipated_state[team]**2
        if probability > 1:
            probability = 1
        return probability
    # MAIN
    def play_action(self,
                    team: int,
                    round_number: int,
                    hand: List[GameAction],
                    prev_turn: List) -> Optional[GameAction]:
        


        ##### IMPLEMENT AWESOME STRATEGY HERE ##################
        # 0. params
        last = 99
        
        # 1. update state
        if round_number == 0 and team == 1:
            self.update_team(prev_turn, 0)
        elif round_number > 0:
            self.update_with_prev(prev_turn, team)
        self.anticipate_next_state()
        #self.round += 1
        
        #####print(f"comp: beginning of {round_number}", self.state)
        #####print(f"ant: beginning of* {round_number+1}", self.anticipated_state)
        
        if len(hand) > self.hand_size:
            self.dealt_count += len(hand) - self.hand_size
            self.hand_size = len(hand)
            ####print(self.dealt_count)
        
        # 2. accumulate cards according to strategy
        if round_number < 98: # playe not needed cards
            #print(hand)
            min_target_hand = {"X": 2, 
                        "Z": 1,
                        "H": 1,
                        "R": 0,
                        "M": 1 }
            hand_dict = {"X": hand.count(GameAction.PAULIX), 
                        "Z": hand.count(GameAction.PAULIZ),
                        "H": hand.count(GameAction.HADAMARD), 
                        "R": hand.count(GameAction.REVERSE), 
                        "M": hand.count(GameAction.MEASURE), }
            #print(hand_dict.items())
            if hand_dict["M"] > 0:
                #print(">>>>>> M", hand_dict["M"])
                pass
            droppable = [self.action_dict[key] for key,value in hand_dict.items() if value > min_target_hand[key]] # cards of wich we have more than we need
            #droppable = droppable + [GameAction.REVERSE,GameAction.PAULIZ] # cards we dont need
            #print("droppable", droppable)
            droppable_indices = [k for k in range(len(hand)) if hand[k] in droppable]
            #print("droppable_indices", droppable_indices)
            if len(droppable_indices)>0:
                drop_index = droppable_indices[np.random.randint(len(droppable_indices))]
            if len(hand)==5 and self.dealt_count < 20:
                #print("dropping", hand[drop_index])
                self.anticipate_next_state(before_rotation=hand[drop_index])
                #####print(f"ant after {hand[drop_index]}: beginning of* {round_number+1}", self.anticipated_state)
                self.hand_size -= 1
                return hand[drop_index]
        
        # 3. play cards 
        elif round_number == last-1: 
            for k in range(len(hand)):
                if hand[k] == self.action_dict["M"]:
                    #####print("> MEASURING")
                    self.hand_size -= 1
                    return hand[k] 
              
        elif round_number == last:
            #####print(f"round = {last}")
            #####print("hand:", hand)
            #print("ACTUAL:",round_number, np.round(self.state,3))
            #print("ANTICIPATED:",round_number+1, np.round(self.anticipated_state,3))
            
            target_component = team
            #####print("target",target_component)
            
            ##if abs(self.anticipated_state[target_component]**2) <= 0.5: # NOTE: this does not anticipate what team 1 will do in the same round / team 0 has done in same round
                # include =0.5 because then if we flip, the rotation will be opposite
                ##print("want to flip")
                ##if GameAction.PAULIX in hand:
                ##    print("flipped")
                ##    print("ANTICIPATED X:",round_number+1, np.round(self.get_rotation(self.direction)@(self.X @ self.state),3))
                ##    return GameAction.PAULIX
                
                
            best_prob = 0
            best_action = None
            for i in range(len(hand)+1):
                if i == len(hand):
                    action = None
                else:
                    action = hand[i]
                self.test_state = np.copy(self.state)
                self.test_direction = self.direction
                temp_prob = self.try_action(action, team)
                #####print(temp_prob)
                if temp_prob > best_prob:
                    best_prob = temp_prob
                    best_action = action
            if best_action is not None:
                self.hand_size -= 1
            return best_action
                    

        #######################################################
        return None
