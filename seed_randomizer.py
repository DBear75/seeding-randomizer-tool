from graphqlclient import GraphQLClient
import json
import random
import argparse
import pandas as pd
import numpy as np
import time

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

def get_controlled_random_order_single_elim(seeds: list):
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
    if num_players < 4:
        return shuffled_seeds
    
    index = 2
    group_size = 2
    while index < num_players:
        next_index = min(index + group_size, num_players)
        group_size *= 2

        shuffle_array(shuffled_seeds, index, next_index)

        index = next_index

    return shuffled_seeds

def random_except_topN(seeds: list, N: int):
    """
    Generate a controlled random order of a list with specific shuffling patterns based on group sizes.
        
    Parameters:
        seeds (list): The initial list of seeds or players to be shuffled.
        N (int): The number of top seeds to keep in place.

    Returns:
        list: The list with specific sections shuffled based on group sizes and given patterns.
    """
    shuffled_seeds = [s for s in seeds]
    num_players = len(seeds)
    print(N, num_players)

    # If there are less than 6 players there is no need to shuffle anything
    if num_players <= N:
        return shuffled_seeds
    
    shuffle_array(shuffled_seeds, N, num_players)

    return shuffled_seeds

random.seed(time.time())
parser = argparse.ArgumentParser(description='Test Word.')
parser.add_argument("--phase-id", type=str)
parser.add_argument("--rand-type", type=str, default='default')
args = parser.parse_args()

authToken = ''
# Open the file authToken.txt in read mode
with open('authToken.txt', 'r') as file:
    # Read the first line of the file and strip any leading/trailing whitespace
    authToken = file.readline().strip()


apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)

phaseId = args.phase_id
## Obtain Current Seeding
getSeedsResult = client.execute('''
query getCurrentSeeds($phaseId:ID!){
  phase(id:$phaseId){
    seeds(query:{
      perPage: 100
    }){
      nodes{
        id
        seedNum
      }
    }
  }
}
''',
{
  "phaseId":phaseId
})
resData = json.loads(getSeedsResult)
if 'errors' in resData:
    print('Error:')
    print(resData['errors'])
if not resData['data']['phase']:
    print('Phase not found')
## Shuffle Current Seeding
else:
    print('Current seeding acquired...')
    seedMapping = []
    for key, value in enumerate(resData['data']['phase']['seeds']['nodes']):
        seedId = value['id']
        seedNum = value['seedNum']
        seedMapping.append({
            "seedId": seedId,
            "seedNum": seedNum,
        })
    ## Put the new seeding here
    newSeedMapping = []
    ## Collect the seedIds here and then shuffle them
    seedIds = []
    for key, value in enumerate(seedMapping):
        seedIds.append(value['seedId'])

    if args.rand_type == 'se':
        seedIds = get_controlled_random_order_single_elim(seedIds)
    elif args.rand_type[:3] == 'top':
        seedIds = random_except_topN(seedIds, int(args.rand_type[3:]))
    else:
        seedIds = get_controlled_random_order(seedIds)
    
    ## Build the new seeding map with the shuffled seedIds
    for key, value in enumerate(seedMapping):
        seedNum = key + 1
        newSeedMapping.append({
            "seedId": seedIds[key],
            "seedNum": seedNum
        })
    numSeeds = len(seedMapping)
    print("Randomizing " + str(numSeeds) + " seeds in phase " + str(phaseId) + "...")
    ## Post the shuffled seeding via GQL Mutation
    seedingUpdateResult = client.execute('''
    mutation UpdatePhaseSeeding ($phaseId: ID!, $seedMapping: [UpdatePhaseSeedInfo]!) {
    updatePhaseSeeding (phaseId: $phaseId, seedMapping: $seedMapping) {
        id
    }
    }
    ''',
    {
        "phaseId": phaseId,
        "seedMapping": newSeedMapping,
    })
    resData = json.loads(seedingUpdateResult)
    if 'errors' in resData:
        print('Error:')
        print(resData['errors'])
    else:
        print('Success!')