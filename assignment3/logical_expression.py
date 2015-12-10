#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

import copy
# actualModel = {}

def getSymbols(expression):
    symbols = []

    if expression.symbol[0]: # If it is a base case (symbol)
        symbols.append(expression.symbol[0])

    else: # Otherwise it is a subexpression
        for subexpression in expression.subexpressions:
            for symbol in getSymbols(subexpression):
                if symbol not in symbols:
                    symbols.append(symbol)
    return symbols

def getModel(statement):
    model = {};
    for expression in statement.subexpressions:
        if expression.symbol[0]:                            #true symbols
            model[expression.symbol[0]] = True
        elif expression.connective[0].lower() == 'not':     #false symbols
            if expression.subexpressions[0].symbol[0]:
                model[expression.subexpressions[0].symbol[0]] = False
        # else:
        #     newModel = getModel(expression)
        #     for x in newModel:
        #         model[x] = newModel[x]
    return model

def extendModel(model,symbol,value):
    newModel = copy.deepcopy(model)
    newModel[symbol] = value
    return newModel

def plTrue(statement,model):
    # print_expression(statement," ")
    # print
    if statement.symbol[0]:
        return model[statement.symbol[0]]
        # if statement.symbol[0] in model:
        #     return model[statement.symbol[0]]
        # elif statement.symbol[0] in model:
        #     return actualModel[statement.symbol[0]]

    elif statement.connective[0].lower() == 'and':
        result = True
        for exp in statement.subexpressions:
            result = result and plTrue(exp,model)
        return result

    elif statement.connective[0].lower() == 'or':
        result = False
        for exp in statement.subexpressions:
            result = result or plTrue(exp,model)
        return result

    elif statement.connective[0].lower() == 'xor':
        result = False
        for exp in statement.subexpressions:
            isExpTrue = plTrue(exp,model)
            result = (result and not isExpTrue) or (not result and isExpTrue)
        return result

    elif statement.connective[0].lower() == 'if':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]
        isLeftTrue = plTrue(left,model)
        isRightTrue = plTrue(right,model)
        if( isLeftTrue and not isRightTrue ):
            return False
        else:
            return True

    elif statement.connective[0].lower() == 'iff':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]
        isLeftTrue = plTrue(left,model)
        isRightTrue = plTrue(right,model)
        if( isLeftTrue == isRightTrue ):
            return True
        else:
            return False

    elif statement.connective[0].lower() == 'not':
        return not plTrue(statement.subexpressions[0],model)


def check_true_false(knowledge_base, statement):
    model = getModel(knowledge_base)

    symbols = getSymbols(knowledge_base)
    for symbol in getSymbols(statement):
        symbols.append(symbol)

    # remove symbols that are already present in the model
    for symbol in model:
        if symbol in symbols:
            symbols.remove(symbol)
    # print symbols

    truthOfStatement = TTCheckAll(knowledge_base, statement, symbols, model)
    # print "Statement is : %s" % truthOfStatement

    negation = logical_expression()
    negation.connective[0] = 'not'
    negation.subexpressions.append(statement)

    truthOfNegation = TTCheckAll(knowledge_base, negation, symbols, model)
    # print "Negation is : %s" % truthOfNegation

    result = open("result.txt","w+")
    if truthOfStatement and not truthOfNegation:
        result.write("definitely true")
    elif not truthOfStatement and truthOfNegation:
        result.write("definitely false")
    elif not truthOfStatement and not truthOfNegation:
        result.write("possibly true, possibly false")
    elif truthOfStatement and truthOfNegation:
        result.write("both true and false")


def TTCheckAll(KB, statement, symbols, model):
    if not symbols:
        # print "truth of statement is : %s" % plTrue(statement,model)
        if plTrue(KB,model):
            # print "KB is true"
            return plTrue(statement, model)
        else:
            return True
    else:
        p = symbols.pop(0)

        # model[p] = True
        # isTrueIfPTrue = TTCheckAll(KB,statement,symbols,model)
        #
        # model[p] = False
        # isTrueIfPFalse = TTCheckAll(KB,statement,symbols,model)
        #
        # return isTrueIfPTrue and isTrueIfPFalse

        return TTCheckAll(KB, statement, symbols, extend(model,p,True)) and TTCheckAll(KB, statement, symbols, extend(model,p,False))

def extend(model,symbol,value):
    model[symbol]=value
    return model

