import argparse
import pandas as pd
import numpy as np
import random

def shuffle_array(arr: list, start: int, end: int):
    """
    Shuffle a subset of an array between specified start and end indices.

    Parameters:
        arr (list): The original array to be shuffled.
        start (int): The inclusive starting index of the sublist to be shuffled.
        end (int): The exclusive end index of the sublist to be shuffled.

    Returns:
        list: The array with the shuffled subset.

    Raises:
        ValueError: If the start index is negative, the end index is beyond the array's length, or if start >= end.
    """

    # Ensure start and end are within the bounds of the array
    if start < 0 or end > len(arr) or start >= end:
        raise ValueError("Invalid start or end indices.")
    
    # Shuffle the sublist from start to end-1
    sublist = arr[start:end]
    random.shuffle(sublist)
    
    # Re-insert the shuffled sublist into the original array
    arr[start:end] = sublist
    
    return arr


def get_controlled_random_order(seeds: list):
    """
    Generate a controlled random order of a list with specific shuffling patterns based on group sizes.

    Parameters:
        seeds (list): The initial list of seeds or players to be shuffled.

    Returns:
        list: The list with specific sections shuffled based on group sizes and given patterns.

    Raises:
        None
    """
    shuffled_seeds = [s for s in seeds]
    num_players = len(seeds)

    # If there are less than 6 players there is no need to shuffle anything
    if num_players < 6:
        return shuffled_seeds
    
    index = 4
    group_size = 2
    group_size_increase = False
    while index < num_players:
        next_index = min(index + group_size, num_players)
        if group_size_increase:
            group_size *= 2

        
        shuffle_array(shuffled_seeds, index, next_index)

        # Book keeping for next loop
        group_size_increase = not group_size_increase
        index = next_index

    return shuffled_seeds


parser = argparse.ArgumentParser(description='Test Word.')
parser.add_argument("--seed-file", type=str)
parser.add_argument("--seed-out-file", type=str, default="rand_seeds.txt")
#parser.add_argument("--bracket-type", type=str, default="double-elimination", nargs="+")


args = parser.parse_args()


# Convert the contents of the file to an array
original_seeding = pd.read_csv(args.seed_file)

players_array = np.array([x for x in original_seeding["Player GamerTag"] ])

shuffled_player_array = get_controlled_random_order(players_array)

f = open(args.seed_out_file, "w")
for i, player in enumerate(shuffled_player_array):
	f.write(f"{i+1}\t{player}\n")
	
f.close()
