**Status:** Active

# basic_roulette

The [Basic Roulette](https://github.com/faGH/fa.intelligence.notebooks/tree/main/labs/open_ai/environments/basic_roulette) is a multiagent
domain featuring continuous state and action spaces. Currently,
several tasks are supported:

## Observations

The observations that can be made about this environment are as follows.

1. A collection of historical black and red landings.
2. The available balance.

## Actions

The actions that an agent can take on this environment are as follows.

| Index | Name   | Description              |
|-------|--------|--------------------------|
|0      | Black  | Bet on the Black outside.|
|1      | Red    | Bet on the Red outside.  |

## Reward

The reward at this point is simply a function of the profits made by performing a given action.

## Environmental Self-Exit Condition

The environment will exit on it's own when the balance <= 0.

# Installation

```bash
cd basic_roulette
pip install -e .
```
