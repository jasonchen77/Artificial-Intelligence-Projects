'''
Created on Sep 18, 2020
This program solves the 8 Puzzle
@author: Jason Chen
'''
import numpy as np
import heapq

#Prints the successor states with helper succStates method
def print_succ(state):
    succStatesList = succStates(state)
    
    for ss in succStatesList:
        print(ss["sState"], "h=" + str(int(ss["h"])))

#Solves the 8 Puzzle
#Uses A* and priority queue implementation
def solve(state):
    goalState = [1,2,3,4,5,6,7,8,0]
    openpq = []
    closed = []
    h = manhattan_distance(state)
    heapq.heappush(openpq, (h, state, ( 0, h, -1), None))
    fPath = []
    while (openpq):
        b = heapq.heappop(openpq)
        closed.append(b)
        
        #if goal is found
        if (b[1] == goalState):
            current = b
            while (not (current == None)):
                fPath.append(current)
                current = current[3]
            break
                
        succS = succStates(b[1])
        for ss in succS:
            ssG = b[2][0] + 1
            ssHeuristic = manhattan_distance(ss["sState"])
            ssParent = b[2][2] + 1
            ssF = ssG + ssHeuristic
            found = False
            
            #check if successor is in the Open
            for ssOpen in openpq:
                if (ss["sState"] == ssOpen[1]):
                    found = True
                    if ssG < ssOpen[2][0]:
                        del ssOpen
                        heapq.heappush(openpq, (ssF, ss["sState"], (ssG, ssHeuristic, ssParent), b))
            
            #check if successor is in the Closed
            for ssClosed in closed:
                if (ss["sState"] == ssClosed[1]):
                    found = True
                    if ssG < ssClosed[2][0]:
                        del ssClosed
                        heapq.heappush(openpq, (ssF, ss["sState"], (ssG, ssHeuristic, ssParent), b))
            
            #If neither in Open or Closed
            if found == False:
                heapq.heappush(openpq, (ssF, ss["sState"], (ssG, ssHeuristic, ssParent), b))
                
    #Path printing
    fP = fPath[::-1]
    for f in fP:
        print(f[1], "h=" + str(int(f[2][1])), "moves:", f[2][0])
    

#Calculate Manhattan Distance from current state to the goal state    
def manhattan_distance(state):
    distanceSum = 0
    stateA = np.array(state)
    stateReshaped = stateA.reshape(3,3)
    
    correctState = np.array([1,2,3,4,5,6,7,8,0])
    correctState = correctState.reshape(3,3)
    
    num = 1
    while (num<9):
        numi, numj = np.where(stateReshaped==num)
        correctNumi, correctNumj = np.where(correctState==num)
        dnumi = abs(numi - correctNumi)
        dnumj = abs(numj - correctNumj)
        distanceSum += (dnumi + dnumj)
        num += 1
        
    return distanceSum

#Find the successor states    
def succStates(state):
    stateA = np.array(state)
    stateReshaped = stateA.reshape(3,3)
    succStates = []
    
    zi, zj = np.where(stateReshaped==0)
    
    #1st position
    if (zi == 0 and zj == 0):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #2nd position
    if (zi == 0 and zj == 1):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #3rd position
    if (zi == 0 and zj == 2):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
    
    #4th position
    if (zi == 1 and zj == 0):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #5th position
    if (zi == 1 and zj == 1):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #6th position
    if (zi == 1 and zj == 2):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi+1, zj] = stateReshaped[zi+1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #7th position
    if (zi == 2 and zj == 0):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
    
    #8th position
    if (zi == 2 and zj == 1):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj+1] = stateReshaped[zi, zj+1], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
        
    #9th position
    if (zi == 2 and zj == 2):
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi-1, zj] = stateReshaped[zi-1, zj], stateReshaped[zi, zj]
        succStates.append(tempState)
        tempState = stateReshaped.copy()
        tempState[zi, zj], tempState[zi, zj-1] = stateReshaped[zi, zj-1], stateReshaped[zi, zj]
        succStates.append(tempState)
    
    succStatesList = []    
    for ss in succStates:
        heuristic = manhattan_distance(ss)
        succStatesList.append({"sState": ss.reshape(-1).tolist(), "h": heuristic})
    
    succStatesListSorted = sorted(succStatesList, key=lambda i : i["sState"], reverse=False)
    return succStatesListSorted
    
    
