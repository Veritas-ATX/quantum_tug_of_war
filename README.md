# quantum_tug_of_war
This is a repository to store tug of war playing bots for the Columbia University course: COMS 4281 Intro. to Quantum Computing.
## Current Leaderboard
1. Austin Basic Bot

Below table is for performance tracking.
Expand into table for further bot comparisons!

| Bot Name | File | vs. Bot | Team $\ket{0}$ Win % | Team $\ket{1}$ Win % |
| --- | --- | --- | --- | --- |
| Austin Basic Bot | austin_basic_bot.py | Random Bot | 85.69 | 85.67 |

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
