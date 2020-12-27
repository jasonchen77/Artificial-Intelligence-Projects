'''
Created on Oct 23, 2020

@author: Jason Chen
'''

from scipy.linalg import eigh  
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')

def load_and_center_dataset(filename):
    x = np.load(filename)
    x = np.reshape(x, (2000, 784))
    xcent = x - np.mean(x, axis=0)
    return xcent

def get_covariance(dataset):
    x = dataset
    cov = (1/(2000-1)) * np.dot(np.transpose(x), x)
    return cov

def get_eig(S, m):
    val, vec = eigh(S, eigvals = (len(S)-m, len(S)-1))
    valDesc = val[::-1]
    vecDesc = np.fliplr(vec)
    valDescDiag = np.diag(valDesc)
    return valDescDiag, vecDesc

def get_eig_perc(S, perc):
    val, vec = eigh(S)
    valDesc = val[::-1]
    vecDesc = np.fliplr(vec)
    sumPerc = np.sum(valDesc)
    cutNum = 0
    for i in range(len(valDesc)):
        if ((valDesc[i]/sumPerc) <= perc):
            cutNum = i
            break
    eValFinal, eVecFinal = eigh(S, eigvals = (len(S)-cutNum, len(S)-1))
    
    eValFinalDesc = eValFinal[::-1]
    eVecFinalDesc = np.fliplr(eVecFinal)
    
    eValFinalDescDiag = np.diag(eValFinalDesc)
    
    return eValFinalDescDiag, eVecFinalDesc

def project_image(image, U):
    xProjA = np.dot(np.transpose(U), image)
    xProjFinal = np.dot(U, xProjA)
    return xProjFinal
        
def display_image(orig, proj):
    origReshaped= np.reshape(orig, (28,28))
    projReshaped= np.reshape(proj, (28,28))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3))
    ax1.set_title('Original')
    ax2.set_title('Projection')
    origCB = ax1.imshow(origReshaped, aspect='equal', cmap='gray')
    projCB = ax2.imshow(projReshaped, aspect='equal', cmap='gray')
    fig.colorbar(origCB, ax=ax1)
    fig.colorbar(projCB, ax=ax2)
    plt.show()
    #plt.savefig("hw5output.png")
    










