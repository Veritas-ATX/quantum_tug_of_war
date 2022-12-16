# quantum_tug_of_war
This is a repository to store tug of war playing bots for the Columbia University course: COMS 4281 Intro. to Quantum Computing.
## Current Leaderboard
1. Austin Basic Bot

Below table is for performance tracking.
Expand into table for further bot comparisons!

| Bot Name | vs. Bot | Team $\ket{0}$ Win % | Team $\ket{1}$ Win % |
| --- | --- | --- | --- |
| Austin Basic Bot | Random Bot | 85.69 | 85.67 |
| Austin HXM Bot | Random Bot | 90.32 | 89.1 |
| Austin HXM Bot | Austin Basic Bot | 50.2 | 54.64 |

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
