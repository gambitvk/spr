# spr - Scissor Paper Rock game

## Requirements

* Tested with python 3.8.3
* Unix terminal

## Directory structure

* configs - bunch of json config files that get used by spr
* test - autmated test for spr
* spr - spr module including main.py

## To run standard Scissor Paper Rock game with 1 human vs 1 computer

In the root folder of spr:

```sh
python -m spr.main ./config/spr_standard.json
```

## To run the extended Scissor Paper Rock Lizard Spock game with 1 human vs 1 computer

In the root folder of spr:

```sh
python -m spr.main ./config/sprls_comp_vs_human.json
```

## To watch a bunch of computers (2+) playing themselves

In the root folder of spr:

```sh
python -m spr.main ./config/sprls_comp_only_3_player_demo.json

or

python -m spr.main ./config/spr_comp_only_3_player_demo.json
```

## Custom game

Should be able to vary the game via config file without modifying the code(up to a certain extend^^)..Have fun!!
