# quantum_tug_of_war - Team EPR Triplet

## Explanation of chosen strategy

On the high level, this bot is designed such that it accumulates a desired set of cards, in which cards are ranked by their power, as measured by their potential to rotate a non-favorable into our favor, and then plays the card starting in the last round of regular time whenever it would benefit our winning probability if the game ended after that round.

We designate X and H the most powerful cards.

We decompoose our strategy into two components. Card accumulation behavior and playing behavior playing behavior at the end of the game.

### 1) Card accumulation behavior
The card accumulation behavior is informed by curating a set of desired cards. Starting from the first hand dealt, cards of which more are on the hand than required by the target distribution are played at random in order to make more space for new cards. This behavior is applied every round, except

While playing these cards has an effect on the state, we anticipate the opponent to behave similarly and rely on being able to completely overwrite the state produced at time of playing the card at the end of the game through cards being played then.

The desired set of cards is a five-X hand. The reasoning behind this choice is that the Pauli X matrix applied on any non-favorable state, i.e. a state whose squared amplitude for the one-qubit state desired to win as given by the team allocation, can rotate such state such that the target probability is at least 0.5. Thus, having as many of them as possible allows for the greatest flexibility in responding to the opponent's behavior at the end of the game.

While the dropping undesired card behavior is applied every round, we stop discarding second most desired cards, which is Hadmard, after a certain round:

The reason for the choice of Hadamard is its ability to rotate some states closer to our desired state or, like in the case of a perfect computationa basis state, at least reduce the amplitude of the opponent's desired state. 
Conversely, we disregard the R gate because its effect of changing the direction of rotation will only start to be significant after a high number of round, depending on the original state, which is not given in the end phase of the game, and because this effect can easily be overwritten by a subequent card.
Similarly, we disregard the Z gate because a Z gate would only be helpful to change a state closer to the target state in combination with a Hadmard gate, effectively making it bitflip rotation in a different basis. This would require to expect the next card to be played to be a Hadamard, which we cannot at any time due to our deck and the opponents behavior.

The reason for regarding Hadamard in addition to PauliX that is that the probability for getting at least 5 Xs over 20, expecting 20 cards to be dealt over the 100 rounds, is

$1-P[x<=4] == 1-\sum_{x=0}^4 begin{pmatrix}20\\ x\end{pmatrix}0.15^x0.85^{20-x} = 0.1702$

where x is the number of X gates dealt. 
However, the probability of getting at least a full hand of either H or X using the same model gives a probability of 0.9651.

Consequently, we decide to stop playing Hadmard cards for the potential benefit of receiving another X in round 70, since then the probability of receiving another X is lower than 0.5.
The probability of getting at least 5 more cards in the last 30 rounds, where 5 are required to have a probability of getting at least one X being larger than 0.5, assuming we have not reached our limit in the first 70 rounds, is given by 

$1-P[c<=4] == 1-\sum_{x=0}^4 begin{pmatrix}30\\ c\end{pmatrix}0.2^c0.8^{30-c} = 0.7448$,

where c is the number of cards dealt.

Then the probability of getting at least one X among 5 trials is 

$1-P[x=0] == 1-\begin{pmatrix}5\\ 0\end{pmatrix}0.85^{5} = 0.5563$,

so that the total probability of getting another X is $P[x\geq 1]P[c\geq 5]=0.414$, which shows that it is rather unlikely to get another X. In turn, in round 60 the same probability is $0.506$. This shows that from approx. round 70 onwards it is preferable to keep the Hadamard in question. If it was a completely undesired card, we would continue to drop them for the prospect of receiving another X or H.


### 2) Playing behavior at the end of the game

Starting at round 99, the bot plays whatever card is one his hand that maximizes the winning probability, including the option to pass if the state is already desirable and none of the cards would further improve it.

We select this card by calculating the winning probability as squared amplitude of the state in concern, respectively, resulting from applying each card on the current state and accounting for the rotation happening and the order of the teams.


### Further explorations

This bot was chosen as the best performing one among different and similar strategies we designed.

We implemented these related strategies that did not lead to performance improvements or were not compatible with this strategy.
* Accumulating measurement(s) in addition to X and playing them in or just before round 100 to, for a state already desirable, maximize the actual probability of having this state measured in the end. This, however, comes at cost of a potential X or Hadmard, while the measurement itself in expectation does not change an undesired state into a desired one. If instead we played the measurement sufficiently before the end of the game to replace it the with X/H cards, it loses its effect.
* Playing cards before round 99 such that the state in state 99 is desirable, forcing the opponent that starts to play in that round to change the state first, so that given we have the same cards, we have an advantage into overtime. This however, is not compatible with accumulating a desired mix of cards because then we could only play cards/discard cards before round 99, that help that purpose, but not any others that we would simply like to replace with better cards for the end period.
* Anticipating opponents behavior in the next round and playing our cards accordingly. That strategy to be lower performing than this strategy mostly because we cannot expect to have the same deck of cards.


---------

## Our bots


This is a repository to store tug of war playing bots for the Columbia University course: COMS 4281 Intro. to Quantum Computing.
## Current Leaderboard
1. Smart All X Bot
2. All X Bot
3. HXM Bot
4. Austin Basic Bot
5. Lennart Bot
6. Abram Bot
7. Random Bot

Below table is for performance tracking.
Expand into table for further bot comparisons!

| Bot Name | vs. Bot | Team $\ket{0}$ Win % | Team $\ket{1}$ Win % |
| --- | --- | --- | --- |
| Austin Basic Bot | Random Bot | 85.69 | 85.67 |
| HXM Bot | Random Bot | 90.32 | 89.1 |
| HXM Bot | Austin Basic Bot | 50.2 | 54.64 |
| All X Bot | Random Bot | 81.85 | 82.1 |
|  All X Bot | Austin Basic Bot | 54.9 | 60.68 |
|  All X Bot |  HXM Bot | 57.07 | 60.25 |
|  Smart All X Bot |  All X Bot | 48.64 | 54.35 |
|  Smart All X Bot |  HXM Bot | 62.14 | 65.51 |
|  Smart All X Bot | Austin Basic Bot | 56.99 | 61.89 |
|  Smart All X Bot | Random Bot | 84.2 | 84.98 |
| Abram Basic Bot | Random Bot | 55.41 | 54.37 |
| Lennart Greedy Bot | Random Bot | 76.32 | 80.32
| Lennart Greedy Bot | Austin Basic Bot (no overtime) | 20 | 100 

NOTE: All stats generated using the following:
```python
win_counter = 0
for i in range(10000):
    stratbot = MyStrategy("MyStrat")
    randombot = RandomBot("The Randos")
    gp = GamePlayer(stratbot, randombot)
    winning_state = gp.play_rounds()
    if winning_state[0] == 1:
        win_counter += 1
print(f'Percent win as team 0: {win_counter/100.0}%')

win_counter = 0
for i in range(10000):
    stratbot = MyStrategy("MyStrat")
    randombot = RandomBot("The Randos")
    gp = GamePlayer(randombot, stratbot)
    winning_state = gp.play_rounds()
    if winning_state[0] == 0:
        win_counter += 1
print(f'Percent win as team 1: {win_counter/100.0}%')
```
