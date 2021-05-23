#!/bin/bash

## baseline runs
python3 main.py -runs 1 -output stuff/base-internet
python3 main.py -runs 10 -output stuff/base-internet -gif
python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/base-relcave
python3 main.py -graph rel-cave -runs 10 -steps 200 -output stuff/base-relcave -gif

## low information
## random immunization
# python3 main.py -runs 1 -output stuff/random01-internet -immune random -n_immune 1
# python3 main.py -runs 1 -output stuff/random05-internet -immune random -n_immune 5
# python3 main.py -runs 1 -output stuff/random10-internet -immune random -n_immune 10
# python3 main.py -runs 1 -output stuff/random25-internet -immune random -n_immune 25
# python3 main.py -runs 1 -output stuff/random50-internet -immune random -n_immune 50
# python3 main.py -runs 1 -output stuff/random100-internet -immune random -n_immune 100
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random01-relcave -immune random -n_immune 1
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random05-relcave -immune random -n_immune 5
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random10-relcave -immune random -n_immune 10
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random25-relcave -immune random -n_immune 25
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random50-relcave -immune random -n_immune 50
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/random100-relcave -immune random -n_immune 100


## low information
## aquaintance immunization
# python3 main.py -runs 1 -output stuff/acquaint01-internet -immune acquaint -n_immune 1
# python3 main.py -runs 1 -output stuff/acquaint05-internet -immune acquaint -n_immune 5
# python3 main.py -runs 1 -output stuff/acquaint10-internet -immune acquaint -n_immune 10
# python3 main.py -runs 1 -output stuff/acquaint25-internet -immune acquaint -n_immune 25
# python3 main.py -runs 1 -output stuff/acquaint50-internet -immune acquaint -n_immune 50
# python3 main.py -runs 1 -output stuff/acquaint100-internet -immune acquaint -n_immune 100
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint01-relcave -immune acquaint -n_immune 1
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint05-relcave -immune acquaint -n_immune 5
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint10-relcave -immune acquaint -n_immune 10
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint25-relcave -immune acquaint -n_immune 25
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint50-relcave -immune acquaint -n_immune 50
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/acquaint100-relcave -immune acquaint -n_immune 100

## full information
## degree immunization
# python3 main.py -runs 1 -output stuff/degree01-internet -immune degree -n_immune 1
# python3 main.py -runs 1 -output stuff/degree05-internet -immune degree -n_immune 5
# python3 main.py -runs 1 -output stuff/degree10-internet -immune degree -n_immune 10
# python3 main.py -runs 1 -output stuff/degree25-internet -immune degree -n_immune 25
# python3 main.py -runs 1 -output stuff/degree50-internet -immune degree -n_immune 50
# python3 main.py -runs 1 -output stuff/degree100-internet -immune degree -n_immune 100
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree01-relcave -immune degree -n_immune 1
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree05-relcave -immune degree -n_immune 5
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree10-relcave -immune degree -n_immune 10
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree25-relcave -immune degree -n_immune 25
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree50-relcave -immune degree -n_immune 50
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/degree100-relcave -immune degree -n_immune 100

## full information
## population immunization
# python3 main.py -runs 1 -output stuff/population01-internet -immune population -n_immune 1
# python3 main.py -runs 1 -output stuff/population05-internet -immune population -n_immune 5
# python3 main.py -runs 1 -output stuff/population10-internet -immune population -n_immune 10
# python3 main.py -runs 1 -output stuff/population25-internet -immune population -n_immune 25
# python3 main.py -runs 1 -output stuff/population50-internet -immune population -n_immune 50
# python3 main.py -runs 1 -output stuff/population100-internet -immune population -n_immune 100
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population01-relcave -immune population -n_immune 1
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population05-relcave -immune population -n_immune 5
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population10-relcave -immune population -n_immune 10
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population25-relcave -immune population -n_immune 25
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population50-relcave -immune population -n_immune 50
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/population100-relcave -immune population -n_immune 100

## full information
# ## importance immunization
# python3 main.py -runs 1 -output stuff/importance01-internet -immune importance -n_immune 1
# python3 main.py -runs 1 -output stuff/importance05-internet -immune importance -n_immune 5
# python3 main.py -runs 1 -output stuff/importance10-internet -immune importance -n_immune 10
# python3 main.py -runs 1 -output stuff/importance25-internet -immune importance -n_immune 25
# python3 main.py -runs 1 -output stuff/importance50-internet -immune importance -n_immune 50
# python3 main.py -runs 1 -output stuff/importance100-internet -immune importance -n_immune 100
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance01-relcave -immune importance -n_immune 1
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance05-relcave -immune importance -n_immune 5
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance10-relcave -immune importance -n_immune 10
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance25-relcave -immune importance -n_immune 25
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance50-relcave -immune importance -n_immune 50
# python3 main.py -graph rel-cave -runs 1 -steps 200 -output stuff/importance100-relcave -immune importance -n_immune 100
