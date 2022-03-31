from collections import deque
from Interface import *


# = = = = = = = QUESTION 1  = = = = = = = #


def consistent(assignment, csp, var, value):
    """
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var.
    Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned,
    then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
    """
    # TODO: Question 1
    for constraint in csp.binaryConstraints: # all binary constraints
        if constraint.affects(var):
            alter=constraint.otherVariable(var)
            # check the other variable is assigned
            if not constraint.isSatisfied(value,assignment.assignedValues[alter]) and alter in assignment.assignedValues.keys():
                return False
    return True
    #raise_undefined_error()


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
    """
    Recursive backtracking algorithm.
    A new assignment should not be created.
    The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect,
    the inferences made along the way should be reversed.
    See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>):
            a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable):
            a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>):
            a function to specify what type of inferences to use
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
    """
    # TODO: Question 1
    # assignment is complete
    if assignment.isComplete():
        return assignment
    var=selectVariableMethod(assignment,csp)
    if not var:
        return assignment
    dom=orderValuesMethod(assignment, csp, var)
    # all value in domain
    for value in dom:
        # value is consistent with assignment
        if consistent(assignment, csp, var, value):
            inference = inferenceMethod(assignment, csp, var, value)
            if inference!=None:
                # add value to assignment
                assignment.assignedValues[var]=value
                result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
                if result!=None:
                    return result
                # remove var=value from assignment
                assignment.assignedValues[var]=None
                for infr in inference:
                    assignment.varDomains[infr[0]].add(infr[1])
    return None
    #raise_undefined_error()


def eliminateUnaryConstraints(assignment, csp):
    """
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
    """
    domains = assignment.varDomains
    for var in domains:
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
                domains[var].remove(value)
                # Failure due to invalid assignment
                if len(domains[var]) == 0:
                    return None
    return assignment


def chooseFirstVariable(assignment, csp):
    """
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
    """
    for var in csp.varDomains:
        if not assignment.isAssigned(var):
            return var


# = = = = = = = QUESTION 2  = = = = = = = #

# degree heuristic
# choose largest number of connstraints
def degree_heu(assignment,csp,var):
    degree=0
    for cb in csp.binaryConstraints:
        if cb.affects(var):
            alter=cb.otherVariable(var)
            if not assignment.assignedValues[alter]:
                degree+=1
    return degree


def minimumRemainingValuesHeuristic(assignment, csp):
    """
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
    """
    nextVar = None
    domains = assignment.varDomains
    # TODO: Question 2
    var_dict = dict()
    # dict store the degree heuristic values
    for dom in domains.items():
        if not assignment.isAssigned(dom[0]):
            var_dict[dom[0]] =(len(dom[1]),-degree_heu(assignment, csp, dom[0]))
    var_lst= sorted(var_dict.items(), key=lambda dict:dict[1])
    # sort by degree
    if len(var_dict):
        nextVar = var_lst[0][0]
    return nextVar
    #raise_undefined_error()


def orderValues(assignment, csp, var):
    """
    Trivial method for ordering values to assign.
    Uses no heuristics.
    """
    return list(assignment.varDomains[var])


# = = = = = = = QUESTION 3  = = = = = = = #


def leastConstrainingValuesHeuristic(assignment, csp, var):
    """
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
    """
    # TODO: Question 3
    domain = assignment.varDomains[var]
    result=list()
    var_dict=dict()
    for value in domain:
        cons_num = 0
        assignment.assignedValues[var] =value
        for cv in csp.varDomains:
            if cv!= var:
                for n_value in assignment.varDomains[var]:
                    if consistent(assignment,csp, var, n_value):
                        cons_num += 1
        var_dict[value]=cons_num
        assignment.assignedValues[var] = None
    if len(var_dict)!=0:
        var_lst = sorted(var_dict.items(), key = lambda dict:dict[1], reverse = True)
        for v in var_lst:
            result.append(v[0])
        return result
    return None


def noInferences(assignment, csp, var, value):
    """
    Trivial method for making no inferences.
    """
    return set([])


# = = = = = = = QUESTION 4  = = = = = = = #


def forwardChecking(assignment, csp, var, value):
    """
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set< tuple<variable, value> >
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 4
    domain = assignment.varDomains
    
    for constraint in csp.binaryConstraints:
        if constraint.affects(var):
            alter = constraint.otherVariable(var)
            # consider consistency
            if not assignment.isAssigned(alter):
                var_setr = set([])
                for value in domain[alter]:
                    # not consistent value in the domain
                    if not consistent(assignment, csp, alter, value):
                        inferences.add((alter, value))
                        var_setr.add(value)
                if var_setr==domain[alter]:
                    return None
    for infr in inferences:
        assignment.varDomains[infr[0]].remove(infr[1])
    return inferences

    #raise_undefined_error()


# = = = = = = = QUESTION 5  = = = = = = = #


def revise(assignment, csp, var1, var2, constraint):
    """
    Helper function to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 5
    domain = assignment.varDomains
    for v2 in domain[var2]:
        const_s = False
        for v1 in domain[var1]:
            if constraint.isSatisfied(v1,v2):
                const_s = True
        if not const_s:
            inferences.add((var2,v2))
    if len(domain[var2])<=len(inferences):
        return None
    else:
        for infr in inferences:
            domain[infr[0]].remove(infr[1])
    return inferences


def maintainArcConsistency(assignment, csp, var, value):
    """
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    and inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])
    domains = assignment.varDomains

    # TODO: Question 5
    #  Hint: implement revise first and use it as a helper function"""
    q = deque()
    for constarint in csp.binaryConstraints:
        if constarint.affects(var) and assignment.assignedValues[constarint.otherVariable(var)] is None:
            q.append((var,constarint.otherVariable(var),constarint))
    while q:
        # while queue is not empty
        first, last, c = q.pop()
        # binary csp component
        revised = revise(assignment, csp, first, last, c)
        if revised:
            for constr in csp.binaryConstraints:
                if constr.affects(last) and assignment.assignedValues[c.otherVariable(last)] is None:
                    q.append((last, constr.otherVariable(last), constr))
                    # add last, alter to queue
            inferences = inferences.union(revised)
        elif revised is None:
            for var1, v1 in inferences:
                domains[var1].add(v1)
            return None
    return inferences


# = = = = = = = QUESTION 6  = = = = = = = #


def AC3(assignment, csp):
    """
    AC3 algorithm for constraint propagation.
    Used as a pre-processing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 6
    #  Hint: implement revise first and use it as a helper function"""
    q = deque()
    for var in csp.varDomains:
        for constraint in (c for c in csp.binaryConstraints if c.affects(var)):
            q.append((var, constraint.otherVariable(var), constraint))
    # the queue is not empty
    while q:
        xi,xj, constraint = q.pop()
        # pop Xi, Xj, constraint
        revised = revise(assignment, csp, xi, xj, constraint)
        if revised is None:
            for inference in inferences:
                assignment.varDomains[inference[0]].add(inference[1])
            return None
        if len(revised):
            inferences = inferences.union(revised)
            for cb1 in (cb for cb in csp.binaryConstraints if cb.affects(xj)):
                # assigned variable & neighbor
                alter = cb1.otherVariable(xj)
                if not assignment.isAssigned(alter):
                    q.append((xj, alter, cb1))
    return assignment
    #raise_undefined_error()


def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic,
          selectVariableMethod=minimumRemainingValuesHeuristic,
          inferenceMethod=forwardChecking, useAC3=True):
    """
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 pre-processing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
    """
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment is None:
        return assignment

    if useAC3:
        assignment = AC3(assignment, csp)
        if assignment is None:
            return assignment

    assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment is None:
        return assignment

    return assignment.extractSolution()
