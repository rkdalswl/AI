#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    listX = x.split()
    feature = {}
    for i in listX:
        if i in feature:
            feature[i] = feature[i]+1
        else:
            feature[i] = 1
    return feature
    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    weights = {}  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
    for iter in range(numIters):
        for x, y in trainExamples:
            FeatureVector = featureExtractor(x)
            feature = FeatureVector.keys()
            score = 0
            for fi in feature:
                if fi not in weights:
                    weights[fi] = 0
                else:
                    score = score + FeatureVector[fi]*weights[fi]
            if score*y >= 1:
                continue
            else:
                for fi in feature:
                    weights[fi] = weights[fi] + eta*FeatureVector[fi]*y
    
    trainError = evaluatePredictor(trainExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    testError = evaluatePredictor(testExamples, lambda x : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print("Official: train error = %s, test error = %s" % (trainError, testError))
    # END_YOUR_CODE
    return weights

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        phi = {}
        score = 0
        for fi in weights.keys():
            phi[fi] = random.randint(1,10)
            score = score + phi[fi]*weights[fi]
        if score >= 0:
            y = 1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        x1 = x.replace(" ", "")
        x2 = x1.replace("\t", "")
        featureVector = {}
        for i in range(len(x2)-n+1):
            if x2[i:i+n] not in featureVector:
                featureVector[x2[i:i+n]] = 1
            else: featureVector[x2[i:i+n]] += 1
        return featureVector
        # END_YOUR_CODE
    return extract

############################################################
# Problem 4: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 32 lines of code, but don't worry if you deviate from this)
    # import numpy as np
    # print(examples[0:5])
    centers = []
    while len(centers) < K:
        c = random.choice(examples)
        if c not in centers:
            centers.append(c)
   
    for i in range(maxIters):
        assign = {}
        for x in range(len(examples)):
            if examples[x] in centers:
                assign[x] = centers.index(examples[x])
                continue
            xi = examples[x].keys()
            dist = {}
            for c in range(K):
                d = 0
                for xii in xi:
                    d = d + (examples[x][xii]-centers[c][xii])**2
                dist[d] = c
            assign[x] = dist[min(dist.keys())]
        # update center
        centers = []
        cluster = {}
        for x in range(len(examples)):
            if assign[x] not in cluster:
                cluster[assign[x]] = [x]
            else:
                cluster[assign[x]].append(x)
        for c in range(K):
            sum_0=0
            sum_1=0
            count=0
            for x in cluster[c]:
                sum_0 += examples[x][0]
                sum_1 += examples[x][1]
                count += 1
            centers.append({0:sum_0/count, 1:sum_1/count})

    loss = 0
    for c in range(K):
        for x in cluster[c]:
            for xii in xi:
               loss = loss + (examples[x][xii]-centers[c][xii])**2 

    return centers, assign, loss
    # END_YOUR_CODE
