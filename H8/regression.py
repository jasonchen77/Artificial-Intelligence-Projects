import numpy as np
import random
import csv
import math

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_dataset(filename):
    """
    TODO: implement this function.

    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    
    dataset = []
    
    f = open(filename, "r")
    dReader = csv.DictReader(f)
    for row in dReader:
        dataRow = [float(row['BODYFAT']), float(row['DENSITY']), float(row['AGE']), float(row['WEIGHT']), float(row['HEIGHT']), float(row['ADIPOSITY']), float(row['NECK']), float(row['CHEST']), float(row['ABDOMEN']), float(row['HIP']), float(row['THIGH']), float(row['KNEE']), float(row['ANKLE']), float(row['BICEPS']), float(row['FOREARM']), float(row['WRIST'])]
        dataset.append(dataRow)
    
    datasetArray = np.array(dataset)
    
    return datasetArray


def print_stats(dataset, col):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    numDataPoints = len(dataset)
    colSum = 0
    for row in dataset:
        colSum += row[col]
    colMean = colSum / numDataPoints
    colSD = 0
    for row in dataset:
        rowSD = (row[col] - colMean) ** 2
        colSD += rowSD
    colSDev = math.sqrt(colSD / (numDataPoints -1))
    
    print('{:d}'.format(numDataPoints))
    print('{:.2f}'.format(colMean))
    print('{:.2f}'.format(colSDev))


def regression(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    
    mseRowSum = 0
    for row in dataset:
        bx = betas[0]
        for col in range(len(cols)):
            bx += (betas[col+1]*row[cols[col]])
        bx -= row[0]
        mseRow = (bx) ** 2
        mseRowSum += mseRow
    mse =  mseRowSum / len(dataset)
        
    return mse


def gradient_descent(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []
    
    mseRowSum = 0
    for row in dataset:
        bx = betas[0]
        for col in range(len(cols)):
            bx += (betas[col+1]*row[cols[col]])
        bx -= row[0]
        mseRowSum += bx
    mse =  mseRowSum * (2 / len(dataset))
    grads.append(mse)
    
    mse1m = 0
    for colOuter in range(len(cols)):
        mseRowSum = 0
        for row in dataset:
            bx = betas[0]
            for col in range(len(cols)):
                bx += (betas[col+1]*row[cols[col]])
            bx -= row[0]
            mseRow = bx * row[cols[colOuter]]
            mseRowSum += mseRow
        mse1m =  mseRowSum * (2 / len(dataset))
        grads.append(mse1m)
        
    gradsArray = np.array(grads)
    
    return gradsArray


def iterate_gradient(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    gradsIter = gradient_descent(dataset, cols, betas)
    betaTemp = betas
    
    i = 1
    while (i <= T):
        bTempList = []
        for b in range(len(gradsIter)):
            bTemp = betaTemp[b] - (eta * gradsIter[b])
            bTempList.append(bTemp)
        betaTemp = bTempList
        mseTemp = regression(dataset, cols, betaTemp)
        gradsIter = gradient_descent(dataset, cols, betaTemp)
        print(i, '{:.2f}'.format(mseTemp), end=' ')
        for bts in betaTemp:
            print('{:.2f}'.format(bts), end=' ')
        print()
              
        i += 1
        


def compute_betas(dataset, cols):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    betas = []
    mse = None
    
    b0 = np.ones((252,1))
    y = []
    colsData = []
    for row in dataset:
        y.append(row[0])
        cData = []
        for col in cols:
            cData.append(row[col])
        colsData.append(cData)
    yArray = np.array(y)
    yArray = yArray.reshape(252, 1)
    colsDataArray = np.array(colsData)
    colsDataArrayTrans = np.transpose(colsDataArray)
    allCols = np.append(b0, colsDataArray, 1)
    
    xTx = np.dot(np.transpose(allCols), allCols)
    xTxI = np.linalg.inv(xTx)
    IxT = np.dot(xTxI, np.transpose(allCols))
    IxTy = np.dot(IxT, yArray)
    
    betasList = IxTy.tolist()
    for bl in betasList:
        for ble in bl:
            betas.append(ble)
    
    mse = regression(dataset, cols, betas)
    
    return (mse, *betas)


def predict(dataset, cols, features):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    result = None
    
    cBetas = compute_betas(dataset, cols)
    cBetasFiltered = []
    for cb in range(len(cBetas)):
        if cb == 0:
            continue
        else:
            cBetasFiltered.append(cBetas[cb])
            
    cBetasArray = np.array(cBetasFiltered)
    featuresList = [1] + features
    featuresArray = np.array(featuresList)
    result = np.dot(np.transpose(cBetasArray), featuresArray)
    
    return result


def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)


def sgd(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.
    You must use random_index_generator() to select individual data points.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    
    betaTemp = betas
    randNum = random_index_generator(0, 252)
    
    i = 1
    while (i <= T):
        bTempList = []
        randNumTemp = next(randNum)
        gradsIter = sgdHelper(dataset[randNumTemp], cols, betaTemp)
        for b in range(len(gradsIter)):
            bTemp = betaTemp[b] - (eta * gradsIter[b])
            bTempList.append(bTemp)
        betaTemp = bTempList
        mseTemp = regression(dataset, cols, betaTemp)
        print(i, '{:.2f}'.format(mseTemp), end=' ')
        for bts in betaTemp:
            print('{:.2f}'.format(bts), end=' ')
        print()
              
        i += 1
        
    
def sgdHelper(dataRow, cols, betas):
    grads = []
    
    mseRowSum = 0
    bx = betas[0]
    for col in range(len(cols)):
        bx += (betas[col+1]*dataRow[cols[col]])
    bx -= dataRow[0]
    mseRowSum += bx
    mse =  mseRowSum * 2
    grads.append(mse)
    
    mse1m = 0
    for colOuter in range(len(cols)):
        mseRowSum = 0
        bx = betas[0]
        for col in range(len(cols)):
            bx += (betas[col+1]*dataRow[cols[col]])
        bx -= dataRow[0]
        mseRow = bx * dataRow[cols[colOuter]]
        mseRowSum += mseRow
        mse1m =  mseRowSum * 2
        grads.append(mse1m)
        
    gradsArray = np.array(grads)
    
    return gradsArray

if __name__ == '__main__':
    # Your debugging code goes here.
    pass