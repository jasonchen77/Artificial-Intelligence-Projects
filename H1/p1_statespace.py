'''
Created on Sep 11, 2020

@author: Jason Chen
'''

#Fill the jug to capacity from faucet 
#state: the current state
#max: max capacity of the jug
#which: which jug to perform operation on, 0 or 1
def fill(state, max, which):
    succState = state.copy()
    succState[which] = max[which]
    return succState

#Empty the jug  
#state: the current state
#max: max capacity of the jug
#which: which jug to perform operation on, 0 or 1  
def empty(state, max, which):
    succState = state.copy()
    succState[which] = 0
    return succState

#Transfer water from one jug to another
#state: the current state
#max: max capacity of the jug
#source: source jug
#dest: destination jug
def xfer(state, max, source, dest):
    succState = state.copy()
    if (state[source] + state[dest] <= max[dest]):
        succState[source] = 0
        succState[dest] = state[source] + state[dest]
    elif (state[source] + state[dest] > max[dest]):
        succState[dest] = max[dest]
        succState[source] = state[source] - (max[dest] - state[dest])
    return succState

#Output the successor states
#state: the current state
#max: max capacity of the jug
def succ(state, max):
    succStates = []
    succStates.append(fill(state, max, 0))
    succStates.append(fill(state, max, 1))
    succStates.append(empty(state, max, 0))
    succStates.append(empty(state, max, 1))
    succStates.append(xfer(state, max, 0, 1))
    succStates.append(xfer(state, max, 1, 0))
    succStatesSet = set(tuple(x) for x in succStates)
    succStatesList = [list(x) for x in succStatesSet]
    print(succStatesList)
    

        