'''
Created on Nov 4, 2020

@author: Jason Chen
'''

import csv
import math
import numpy

def load_data(filepath):
    f = open(filepath, "r")
    dReader = csv.DictReader(f)
    dataSet = []
    includedKeys = ['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    intKeys = ['#', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    for row in dReader:
        rowData = dict((k, row[k]) for k in includedKeys)
        for key in intKeys:
            rowData[key] = int(rowData[key]) 
        dataSet.append(rowData)
    dataSetCut = dataSet[:20]
    return dataSetCut

def calculate_x_y(stats):
    x = stats['Attack'] + stats['Sp. Atk'] + stats['Speed']
    y = stats['Defense'] + stats['Sp. Def'] + stats['HP']
    xyTuple = (x, y)
    return xyTuple
    
def hac(dataset):
    
    distanceTable = []
    rowCount = 0
    for row in dataset:
        distRow = []
        colCount = 0
        for col in dataset:
            if rowCount == colCount:
                distRow.append(-1)
            elif colCount < rowCount:
                distRow.append(-1)
            else:
                dist = math.sqrt((row[0]-col[0])**2 + (row[1]-col[1])**2)
                distRow.append(dist)
            colCount += 1
        distanceTable.append(distRow)
        rowCount += 1
    
    
    distanceDictList = []
    for row in range(len(distanceTable)):
        for col in range(len(distanceTable[0])):
            if distanceTable[row][col] == -1:
                    continue
            else:
                if row < col:
                    index1 = row
                    index2 = col
                else:
                    index1 = col
                    index2 = row
                distanceDictList.append({'index1': index1, 'index2': index2, 'dist': distanceTable[row][col]})
    distanceDictListSorted = sorted(distanceDictList, key=lambda i : (i['dist'], i['index1'], i['index2']), reverse=False)             
    
    m = len(dataset)
    clusters = []
    z = []
    for dista in distanceDictListSorted:
        bothInCluster = False
        index1InCluster = False
        index2InCluster = False
        index1Cluster = []
        index2Cluster = []
        clusterNum = 0
        for clu in clusters:
            if (dista['index1'] in clu) and (dista['index2'] in clu):
                bothInCluster = True
                break
            elif (dista['index1'] in clu) and (dista['index2'] not in clu):
                index1InCluster = True
                index1Cluster = clu.copy()
                index1ClusterNum = clusterNum
            elif (dista['index2'] in clu) and (dista['index1'] not in clu):
                index2InCluster = True
                index2Cluster = clu.copy()
                index2ClusterNum = clusterNum
            clusterNum += 1
                
        if (bothInCluster == False) and (index1InCluster == True) and (index2InCluster == True):
            if index1ClusterNum < index2ClusterNum:
                zIndex1 = index1ClusterNum + m
                zIndex2 = index2ClusterNum + m
            else:
                zIndex1 = index2ClusterNum + m
                zIndex2 = index1ClusterNum + m
            newCluster = index1Cluster + index2Cluster
            clusters.append(newCluster)
            numOrigObs = len(newCluster)
            z.append([zIndex1, zIndex2, dista['dist'], numOrigObs])
        elif (bothInCluster == False) and (index1InCluster == True) and (index2InCluster == False):
            zIndex1 = dista['index2']
            zIndex2 = index1ClusterNum + m
            index2ListSingle = [dista['index2']]
            newCluster = index2ListSingle + index1Cluster
            clusters.append(newCluster)
            numOrigObs = len(newCluster)
            z.append([zIndex1, zIndex2, dista['dist'], numOrigObs])
        elif (bothInCluster == False) and (index1InCluster == False) and (index2InCluster == True):
            zIndex1 = dista['index1']
            zIndex2 = index2ClusterNum + m
            index1ListSingle = [dista['index1']]
            newCluster = index1ListSingle + index2Cluster
            clusters.append(newCluster)
            numOrigObs = len(newCluster)
            z.append([zIndex1, zIndex2, dista['dist'], numOrigObs])
        elif (bothInCluster == False) and (index1InCluster == False) and (index2InCluster == False):
            if dista['index1'] < dista['index2']:
                zIndex1 = dista['index1']
                zIndex2 = dista['index2']
            else:
                zIndex1 = dista['index2']
                zIndex2 = dista['index1']
            index1ListSingle = [dista['index1']]
            index2ListSingle = [dista['index2']]
            newCluster = index1ListSingle + index2ListSingle
            clusters.append(newCluster)
            numOrigObs = len(newCluster)
            z.append([zIndex1, zIndex2, dista['dist'], numOrigObs])
      
    zNumPyMatrix = numpy.array(z)
    
    return zNumPyMatrix
      

    
    
def feat_vect(dataset):
    mnArray = []
    for data in dataset:
        mnArray.append(calculate_x_y(data))
    return mnArray
    
    
    
    
    
    
    