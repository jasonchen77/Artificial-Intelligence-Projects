'''
Created on Sep 11, 2020

@author: Jason Chen
'''
from _operator import itemgetter

#Calculates the Manhattan Distance for data_point1 and data_point2
#PRCP: Precipitation Amount
#TMAX: Maximum Temperature
#TMIN: Minimum Temperature
def manhattan_distance(data_point1, data_point2):
    d = abs(data_point1.get("PRCP") - data_point2.get("PRCP")) \
        + abs(data_point1.get("TMAX") - data_point2.get("TMAX")) \
        + abs(data_point1.get("TMIN") - data_point2.get("TMIN"))
    return d

#Reads the file in the parameter and convert the data
#into a list of dictionaries
def read_dataset(filename):
    f = open(filename, "r")
    dataList = []
    for line in f:
        lineDict = {}
        (DATE, PRCP, TMAX, TMIN, RAIN) = line.split()
        lineDict["DATE"] = DATE
        lineDict["PRCP"] = float(PRCP)
        lineDict["TMAX"] = float(TMAX)
        lineDict["TMIN"] = float(TMIN)
        lineDict["RAIN"] = RAIN
        dataList.append(lineDict)
    f.close()
    return dataList

#Return the string "TRUE" or "FALSE" based on majority vote  
def majority_vote(nearest_neighbors):
    t = 0
    f = 0
    for neighbor in nearest_neighbors:
        if (neighbor.get("RAIN")=="TRUE"):
            t += 1
        if (neighbor.get("RAIN")=="FALSE"):
            f += 1
    if (t >= f):
        return "TRUE"
    else:
        return "FALSE"
 
#The function first reads the text file, then filters the data set 
#within the year interval. If the filtered data set is empty, it will
#return "TRUE". The the Manhattan Distance is calculated between the 
#test point and all the filtered data set. Then k closest neighbors 
#are selected and called by the majority_vote function        
def k_nearest_neighbors(filename, test_point, k, year_interval):
    dataSet = read_dataset(filename)
    dataSetFiltered = []
    (tYear, tMonth, tDay) = test_point["DATE"].split("-")
    tYear = int(tYear)
    for data in dataSet:
        (year, month, day) = data["DATE"].split("-")
        year = int(year)
        if ((year < (tYear + year_interval)) and (year > (tYear - year_interval))):
            dataSetFiltered.append(data)
    if not dataSetFiltered:
        return "TRUE"
    for fData in dataSetFiltered:
        mDistance = manhattan_distance(test_point, fData)
        fData["MD"] = mDistance
    dataSetFilteredSortedByMD = sorted(dataSetFiltered, key=lambda i : i["MD"], reverse=False)
    kClosestNeighbor = []
    n = 1
    for kcn in dataSetFilteredSortedByMD:
        if (n > k):
            break
        kClosestNeighbor.append(kcn)
        n += 1
    if not kClosestNeighbor:
        return "TRUE"
    return majority_vote(kClosestNeighbor)

        
        
        