'''
Created on Sep 25, 2020

@author: Jason Chen
'''

import random


#Generates successors
def succ(state, static_x, static_y):
    succStates = []
    if (state[static_x] != static_y):
        return succStates
    for s in range(len(state)):
        if s == static_x:
            continue
        tempState = state.copy()
        if ((state[s]-1) >= 0):
            tempState[s] = state[s]-1
            succStates.append(tempState)
        tempState = state.copy()
        if ((state[s]+1) < len(state)):
            tempState[s] = state[s]+1
            succStates.append(tempState)
    succStatesSorted = sorted(succStates)
    return succStatesSorted

#Get the f score of a state
def f(state):
    f = 0
    for s in range(len(state)):
        
        horizontalAttack = False
        leftDiagnalAttack = False
        
        #check horizontal queens
        for s1 in range(len(state)):
            if s == s1:
                continue
            if state[s] == state[s1]:
                f += 1
                horizontalAttack = True
                break
        
        #check left diagonal queens
        if horizontalAttack == False:
            for s2 in range(len(state)):
                if s == s2:
                    continue
                if ((state[s]-s) == (state[s2]-s2)):
                    f += 1
                    leftDiagnalAttack = True
                    break
        
        #check right diagonal queens
        if ((horizontalAttack == False) and (leftDiagnalAttack == False)):
            for s3 in range(len(state)):
                if s == s3:
                    continue
                if ((state[s]+s) == (state[s3]+s3)):
                    f += 1
                    break
                
    return f

#Select the next state
def choose_next(curr, static_x, static_y):
    if (curr[static_x] != static_y):
        return None
    succStates = succ(curr, static_x, static_y)
    nextStates = []
    currentState = {"state": curr, "fScore": f(curr)}
    nextStates.append(currentState)
    for s in succStates:
        nextStates.append({"state": s, "fScore": f(s)})
    nextStatesSorted = sorted(nextStates, key=lambda i : (i["fScore"], i["state"]), reverse=False)
    return nextStatesSorted[0]["state"]

#Runs the Hill Climbing algorithm for n-queens
def n_queens(initial_state, static_x, static_y, print_path=True):
    stop = False
    statesList = []
    currentS = initial_state
    
    while stop == False:
        nextS = choose_next(currentS, static_x, static_y)
        currentFScore = f(currentS)
        nextFScore = f(nextS)
        statesList.append({"state": currentS, "fScore": currentFScore})
        if nextFScore >= currentFScore:
            if ((nextFScore == currentFScore) and (nextS != currentS)):
                statesList.append({"state": nextS, "fScore": nextFScore})
            stop = True
        currentS = nextS
        
    #Prints the states
    if print_path:
        for s in statesList:
            print(s["state"], "-", "f=" + str(s["fScore"]))
        
    return statesList[-1]["state"]
            
#N-queens with random restarts on N*N board
def n_queens_restart(n, k, static_x, static_y):
    random.seed(1)
    allGStates = []
    optimalFound = False
    iteK = 0
    while (iteK < k-1):
        state = []
        iteNum = 0
        while (iteNum < n-1):
            if iteNum == static_x:
                state.append(static_y)
            state.append(random.randint(0, n-1))
            iteNum += 1
            
        stateReturned = n_queens(state, static_x, static_y, print_path=False)
        stateReturnedFScore = f(stateReturned)
        allGStates.append({"state": stateReturned, "f": stateReturnedFScore})
        if stateReturnedFScore == 0:
            print(stateReturned, "-", "f=" + str(stateReturnedFScore))
            optimalFound = True
            break
        iteK += 1
        
    if optimalFound == False:
    
        #Sort the states
        allGStatesSorted = sorted(allGStates, key=lambda i : (i["f"], i["state"]), reverse=False)
        
        #Find lowest f score at the end of k iteration
        minF = allGStatesSorted[0]["f"]
        
        #Print states with best solutions
        for iState in allGStatesSorted:
            if iState["f"] == minF:
                print(iState["state"], "-", "f=" + str(iState["f"]))
            if iState["f"] > minF:
                break
    
        
        
        
        
        