import numpy as np
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Test Word.')
parser.add_argument("--seed-file", type=str)
parser.add_argument("--seed-out-file", type=str, default="rand_seeds.txt")
#parser.add_argument("--bracket-type", type=str, default="double-elimination", nargs="+")


args = parser.parse_args()


# Convert the contents of the file to an array
original_seeding = pd.read_csv(args.seed_file)

players_array = np.array([x for x in original_seeding["Player GamerTag"] ])

num_players = len(players_array)
winners_rounds = int(np.ceil(np.log(num_players)/np.log(2)))
rounds_remaining = winners_rounds

remaining_players = len(players_array)

placement_ties = [1, 1, 1, 1]

while sum(placement_ties) < remaining_players:
	if placement_ties[-1] == placement_ties[-2]:
		placement_ties.append(2*placement_ties[-1])
	else:
		placement_ties.append(placement_ties[-1])
		
		
count = 0

placements = []

for p in placement_ties:
	placements.append(count + p)
	count += p
	
players = list(range(1, num_players + 1))

for i in range(4, len(placements)):
	a = placements[i-1]
	b = min(placements[i],  num_players)
	group = players[a: b]
	np.random.shuffle(group)
	players[a: b] = group

f = open(args.seed_out_file, "w")
for i, player in enumerate(players_array):
	f.write(players_array[players[i]-1] + "\n")
	
f.close()
