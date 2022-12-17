# quantum_tug_of_war
This is a repository to store tug of war playing bots for the Columbia University course: COMS 4281 Intro. to Quantum Computing.
## Current Leaderboard
1. Austin Smart All X Bot
2. Austin All X Bot
3. Austin HXM Bot
4. Austin Basic Bot
5. Random Bot

Below table is for performance tracking.
Expand into table for further bot comparisons!

| Bot Name | vs. Bot | Team $\ket{0}$ Win % | Team $\ket{1}$ Win % |
| --- | --- | --- | --- |
| Austin Basic Bot | Random Bot | 85.69 | 85.67 |
| Austin HXM Bot | Random Bot | 90.32 | 89.1 |
| Austin HXM Bot | Austin Basic Bot | 50.2 | 54.64 |
| Austin All X Bot | Random Bot | 81.85 | 82.1 |
| Austin All X Bot | Austin Basic Bot | 54.9 | 60.68 |
| Austin All X Bot | Austin HXM Bot | 57.07 | 60.25 |
| Austin Smart All X Bot | Austin All X Bot | 48.64 | 54.35 |
| Austin Smart All X Bot | Austin HXM Bot | 62.14 | 65.51 |
| Austin Smart All X Bot | Austin Basic Bot | 56.99 | 61.89 |
| Austin Smart All X Bot | Random Bot | 84.2 | 84.98 |
| Abram Basic Bot | Random Bot | 55.41 | 54.37 |

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
