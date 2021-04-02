# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# 
# To POSTECH CS442 student, as you see from the above comment, this assignment 
# comes from the berkeley. I'd like to appreciate their work. I change some code
# to correctly work in python3. If you have any question, please contact to Seonghyeon
# Lee (sh0416@postech.ac.kr).

import itertools
from functools import reduce
from bayesNet import Factor
import operator as op
import util

def joinFactorsByVariableWithCallTracking(callTrackingList=None):
    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]
        # print("yesjrbv")
        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        joinedFactor = joinFactors(currentFactorsToJoin)
        # print(joinedFactor)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """
    factors = list(factors)
    # print("length", len(factors))
    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factors)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"
    # if len(factors)<2: return
    if len(factors)<2: return factors[0]
    condition = set()
    uncondition = set()
    variableDomainsDict = {}

    # factor1 = factors[0]
    # condition = condition.union(factor1.conditionedVariables())
    # uncondition = uncondition.union(factor1.unconditionedVariables())
    # variableDomainsDict.update(factor1.variableDomainsDict())
    # print(uncondition, condition)
    # # for factor2 in factors[1:]:
    # #     condition = condition.union(factor2.conditionedVariables())
    # #     uncondition = uncondition.union(factor2.unconditionedVariables())
    # #     variableDomainsDict.update(factor2.variableDomainsDict())        
    # # condition = condition.difference(uncondition)
    # # NewFactor = Factor(uncondition, condition, variableDomainsDict)

    # AssignmentDict1 = factor1.getAllPossibleAssignmentDicts() ##list of dictionary
    
    # for factor2 in factors[1:]:
    #     condition = condition.union(factor2.conditionedVariables())
    #     uncondition = uncondition.union(factor2.unconditionedVariables())
    #     variableDomainsDict.update(factor2.variableDomainsDict())
    #     condition = condition.difference(uncondition)
    #     NewFactor_join = Factor(uncondition, condition, variableDomainsDict)
    #     print(uncondition, condition)
    #     AssignmentDict2 = factor2.getAllPossibleAssignmentDicts()
    #     #Assignment table        
    #     key1 = AssignmentDict1[0].keys()
    #     key2 = AssignmentDict2[0].keys()
    #     samekey = list(set(key1).intersection(set(key2)))
    #     for assn1 in AssignmentDict1:
    #         for assn2 in AssignmentDict2:
    #             # samekey의 value가 일치하는지 확인
    #             samekey_val_assn1 = set()
    #             samekey_val_assn2 = set()
    #             for key in samekey:
    #                samekey_val_assn1.add(assn1[key]) 
    #                samekey_val_assn2.add(assn2[key])

    #             if samekey_val_assn1 != samekey_val_assn2: continue
    #             else:
    #                 NewAssignment = {**assn1, **assn2}
    #                 NewProbability = factor1.getProbability(assn1)*factor2.getProbability(assn2)
    #                 NewFactor_join.setProbability(NewAssignment, NewProbability)
        
    #     factor1 = NewFactor_join
    
    for factor in factors:
        condition = condition.union(factor.conditionedVariables())
        uncondition = uncondition.union(factor.unconditionedVariables())
        variableDomainsDict.update(factor.variableDomainsDict())
    condition = condition.difference(uncondition)
    NewFactor_join = Factor(uncondition, condition, variableDomainsDict)

    for assn in NewFactor_join.getAllPossibleAssignmentDicts():
        prob = 1
        for factor in factors:
            for entry in factor.getAllPossibleAssignmentDicts():
                if len(set(entry.items())-set(assn.items())) == 0:
                    prob = prob*factor.getProbability(entry)
                    break
        NewFactor_join.setProbability(assn, prob)
    return NewFactor_join
    "*** YOUR CODE END ***"


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        uncondition = factor.unconditionedVariables() #set
        condition = factor.conditionedVariables() #set
        variableDomainsDict = factor.variableDomainsDict() #dict
        uncondition.remove(eliminationVariable)
        NewFactor = Factor(uncondition, condition, variableDomainsDict)

        # AssignmentDictList = factor.getAllPossibleAssignmentDicts()
        # print(NewFactor.getAllPossibleAssignmentDicts())
        # print(NewFactor)
        
        import copy
        for newAssn in NewFactor.getAllPossibleAssignmentDicts():
            probSum = 0
            for OldAssn in factor.getAllPossibleAssignmentDicts():
                temp = copy.deepcopy(OldAssn)
                del temp[eliminationVariable]
                if newAssn.items() == temp.items():
                    probSum = probSum + factor.getProbability(OldAssn)
            NewFactor.setProbability(newAssn, probSum)
        # print("elimination is end for %s" % eliminationVariable)
        return NewFactor
        "*** YOUR CODE END ***"

    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """
    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print("Factor failed normalize typecheck: ", factor)
            raise ValueError("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    # print(factor)
    # print(factor.unconditionedVariables())
    # print(factor.conditionedVariables())
    # print(factor.variableDomainsDict())
    # print(factor.getAllPossibleAssignmentDicts())

    unconditions = factor.unconditionedVariables()
    conditions = factor.conditionedVariables()
    variableDomainsDict = factor.variableDomainsDict()

    for var in factor.unconditionedVariables():
        if len(variableDomainsDict[var]) == 1:
            unconditions.remove(var)
            conditions.add(var)

    NewFactor = Factor(unconditions, conditions, variableDomainsDict)
    AssnDictList = factor.getAllPossibleAssignmentDicts()
    probSum = 0
    for assn in AssnDictList:
        probSum = probSum + factor.getProbability(assn)
    for assn in AssnDictList:
        NewFactor.setProbability(assn, factor.getProbability(assn)/probSum)
    return NewFactor
    "*** YOUR CODE END ***"

