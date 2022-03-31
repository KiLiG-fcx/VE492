import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        k=self.iterations  # times of iteration
        for i in range(k):
            value_count=util.Counter()
            # store all the max q-values for states
            for state in self.mdp.getStates():
                curr_max=-float('inf')
                # find the max Q-value
                for action in self.mdp.getPossibleActions(state):
                    # for all the actions in that state, compute the Q-values
                    q_value=self.computeQValueFromValues(state,action)
                    if(q_value>curr_max): # has a larger Q-value
                        curr_max=q_value 
                        # update the current max
                    value_count[state]=curr_max 
                    # store current max to state, for all actions
            self.values=value_count


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qvalue=0
        gamma=self.discount
        for next_state,prob in self.mdp.getTransitionStatesAndProbs(state,action):
            # compute possible results for state r+g*v
            qvalue+=prob*(self.mdp.getReward(state,action,next_state)
                          +gamma*self.values[next_state])
        return qvalue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        curr_max=-float('inf')
        action=None
        # all actions in this state
        for actions in self.mdp.getPossibleActions(state):
            qvalue=self.computeQValueFromValues(state, actions)
            if qvalue>curr_max:
                # larger q-value with this action
                curr_max=qvalue
                action=actions # take this action
        return action
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        all_state=self.mdp.getStates()
        for i in range(self.iterations):
            state=all_state[i%len(all_state)]
            # iterate by all states in order
            if not self.mdp.isTerminal(state):
                state_qvalue=list()
                # store q-values for this state
                for actions in self.mdp.getPossibleActions(state):
                    qvalue=self.computeQValueFromValues(state,actions)
                    # add q-value for this state list
                    state_qvalue.append(qvalue)
                # choose the maximum
                self.values[state]=max(state_qvalue)
                

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessor={}
        # for all the states find the predecessor
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                # terminal state, do not have a predecessor
                continue
            else:
                for action in self.mdp.getPossibleActions(state):
                    for next_state,prob in self.mdp.getTransitionStatesAndProbs(state,action):
                        # not in predecessor dict, add state
                        if next_state not in predecessor:
                            predecessor[next_state]={state}
                        else:
                            predecessor[next_state].add(state)
        priqueue=util.PriorityQueue() # create a priority queue
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            qvalues=list()
            # to find the largest qvalue
            for action in self.mdp.getPossibleActions(state):
                qvalue=self.computeQValueFromValues(state,action)
                qvalues.append(qvalue)
            diff=abs(self.values[state]-max(qvalues)) 
            # compute the difference
            priqueue.update(state,-diff)
        
        for k in range(self.iterations):
            if(priqueue.isEmpty()):
                break
            s=priqueue.pop()
            if not self.mdp.isTerminal(s):
                # update s value if not terminal
                qvalues=list()
                for action in self.mdp.getPossibleActions(s):
                    qvalue=self.computeQValueFromValues(s,action)
                    qvalues.append(qvalue)
                self.values[s]=max(qvalues)
            for pre in predecessor:
                if self.mdp.isTerminal(pre):
                    continue
                qvalues=list()
                # comput diff of max(qvalue) self.values
                for action in self.mdp.getPossibleActions(pre):
                    qvalue=self.computeQValueFromValues(pre,action)
                    qvalues.append(qvalue)
                diff=abs(self.values[pre]-max(qvalues))
                if diff>self.theta:
                    # push pre into pq
                    priqueue.update(pre,-diff)