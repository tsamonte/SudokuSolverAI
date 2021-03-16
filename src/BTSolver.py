import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Return: true is assignment is consistent, false otherwise
    """
    def forwardChecking ( self ):
        # for each assigned variable, check the direct neighbors
        # returns true if assignment is consistent
        # returns false if assignment is not consistent
        # or assignment causes neighbors' domain sizes to be zero.

        for var in self.network.getVariables():
            if var.isAssigned(): # we only do forward checking on assigned variables
                neighbors = self.network.getNeighborsOfVariable(var) # neighbors is a list of variables
                varValue = var.getAssignment()
                for neighbor in neighbors:
                    if varValue in neighbor.getValues():
                        self.trail.push(neighbor)
                        neighbor.removeValueFromDomain(varValue)
                        if neighbor.size() == 0:
                            return False
        return True

    """
        Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Return: true is assignment is consistent, false otherwise
    """
    def norvigCheck ( self ):
        # (1) Eliminate value from assigned square's neighbors
        for var in self.network.getVariables():
            if var.isAssigned():
                val = var.getAssignment()
                for neighbor in self.network.getNeighborsOfVariable(var):
                    if val in neighbor.getValues():
                        self.trail.push(neighbor)
                        neighbor.removeValueFromDomain(val)
                        if neighbor.size() == 0:
                            return False

        # (2) Only one possible place for a value, then put the value there
        # each constraint is a list of variables
        # counterList is a list counting how many times a value appears per constraint
        counterList = [0] * self.gameboard.N # Allocate an array Counter[N]
        for constraint in self.network.getConstraints():
            for i in range(len(counterList)): # Zero Counter
                counterList[i] = 0

            for var in constraint.vars:
                for val in var.getValues():
                    counterList[val-1] += 1

            for i in range(len(counterList)):
                if counterList[i] == 1:
                    for var in constraint.vars:
                        if not var.isAssigned():
                            for val in var.getValues():
                                if val == i+1:
                                    self.trail.push(var)
                                    var.assignValue(val)


        return True

    """
         Optional TODO: Implement new heuristics
     """
    def getTournCC ( self ):
        return None

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        variables = []
        for v in self.network.getVariables():
            if not v.isAssigned():
                variables.append(v)
        if len(variables) <= 0:
            return None
        # variables = self.network.getVariables()
        minVarDegree = variables[0].size()
        minVar = variables[0]
        for var in variables[1:]:
            if var.size() < minVarDegree:
                minVarDegree = var.size()
                minVar = var
        return minVar

    """
        Minimum Remaining Value Heuristic with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with, first, the smallest domain
                and, second, the most unassigned neighbors
    """
    def MRVwithTieBreaker ( self ):
        variables = []
        for v in self.network.getVariables():
            if not v.isAssigned():
                variables.append(v)
        if len(variables) <= 0:
            return None
        minDict = {}
        for var in variables:
            degree = var.size()
            if degree in minDict:
                minDict[degree].append(var)
            else:
                minDict[degree] = [var]

        mrvVal = min(minDict.keys())
        if len(minDict[mrvVal]) == 1:
            return minDict[mrvVal][0]
        else:
            maxDegree = 0
            maxVar = None
            for var in minDict[mrvVal]:
                currentDegree = len(self.network.getNeighborsOfVariable(var))
                if currentDegree > maxDegree:
                    maxDegree = currentDegree
                    maxVar = var
            return maxVar

    """
         Optional TODO: Implement new heuristics
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        # returnList = list()
        returnDict = dict()
        currentValues = v.getValues()
        neighbors = self.network.getNeighborsOfVariable(v)

        for value in currentValues:
            returnDict[value] = 0 # initialize dict so every val starts by constraining 0 neighbors

        for neighbor in neighbors:
            neighborValues = neighbor.getValues()
            for nVal in neighborValues:  #for each value in neighbor
                if nVal in returnDict: # if the value is equal to a value in the current node's domain
                    returnDict[nVal] += 1  # neighbor value is constrained, so increase current's counter

        # sorts dict by ascending dictValue (LCV first), then makes list from only the dictKeys (domain values)
        return list(i for (i, _) in sorted(returnDict.items(), key = lambda t: (t[1], t[0])))

        #to sort by values (ascending): sorted(a.items(), key = lambda t: (t[1],t[0]))

    """
         Optional TODO: Implement new heuristics
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
