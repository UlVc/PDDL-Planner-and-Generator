from copy import deepcopy
from itertools import combinations
from predicate import Not, Predicate

class Planner:
    """Generates a plan for the given problem."""
    def __init__(self, domain, problem):
        """
        :param domain: Domain of the world.
        :param problem: Problem to solve.
        """
        self.domain = domain
        self.problem = problem
        self.explored = False
        self.action_taken = None # Action taken to arrive at this plan. It's a tuple of the form (action, predicates).
        self.father = None # Father of this planner. Applying the action taken stored in the variable action_taken with the parent, we got this planner.
        self.level = 0 # Level from where the problem of this planner was generated in the BFS algorithm. The root has level 0.

    def applicable_actions(self):
        """Returns all the actions that can be applied to this planner's problem."""
        return {action : self.applicable_action(action) for action in self.domain.actions}

    def applicable_action(self, action):
        """Checks whether an action is applicable or not.
        :param action: Action to check if is applicable.
        """
        preds = [] # List that will contain the possible predicates to use for the given action.
    
        # We get form all the possible combinations using the state of the problem and then, filter those that we don't want.
        for subset in combinations(self.problem.state, len(action.preconditions)):
            if self.verify_action(action, subset):
                preds.append(subset)

        return preds

    def apply_action(self, action, predicates):
        """Applies an action to the current problem using the given predicates.
        The given action is assumed to be applicable.
        :param action: Action to apply.
        :param predicates: Predicates to use with the action.
        """
        dicc = {} # Dictionary that maps the variable names of the action's preconditions to the names of the given predicates.
        new_planner = Planner(self.domain, deepcopy(self.problem)) # New planner that will contain the effects of the given action.
        new_predicates = deepcopy(action.effects)

        # We form the dictionary with the mapped variables.
        for pred in action.preconditions:
            temp = [x for x in predicates if x.declaration.name == pred.declaration.name][0]
            for i in range(len(pred.variables)):
                dicc[pred.variables[i].name] = temp.variables[i]

        # We form the new predicates using the effects of the action.
        for e in new_predicates:
            if type(e) is Not:
                variables = e.predicate.variables
            else:
                variables = e.variables

            for i in range(len(variables)):
                variables[i] = dicc[variables[i].name]

        # We eliminate the preconditions of the action of the new planner.
        for p in predicates:
            new_planner.problem.state.remove(p)

        # We add the predicates caused by action effects to the new planner.
        for p in new_predicates:
            new_planner.problem.state.append(p)

        new_planner.action_taken = (action, predicates)
        new_planner.father = self
        new_planner.level = self.level + 1

        return new_planner

    def is_goal(self):
        """"
        Checks if the state is the same as the goal.
        """
        for predicado in self.problem.goal:
            if not(predicado in self.problem.state):
                return False

        return True

    def obtain_actions(self):
        """Returns, in the form of a chain, the actions that were done to reach the problem of this planner."""
        if self.father == None:
            return 'Actions to take, starting from the top:'

        return self.father.obtain_actions() + f'\n\n{self.action_taken[0].name}: {[str(p) for p in self.action_taken[1]]}'

    def verify_action(self, action, predicates):
        """"Checks if the given action can be applied using the given predicates.
        :param dic: Action to work with.
        :param predicates: List of predicates to verify in the action.
        """
        dicc_pred     = {0 : [x for x in predicates if type(x) is Not], 
                         1 : [x for x in predicates if type(x) is Predicate]}
        dicc_pred_acc = {0 : [x for x in action.preconditions if type(x) is Not], 
                         1 : [x for x in action.preconditions if type(x) is Predicate]}
        aux = {}

        if len(dicc_pred) != len(dicc_pred_acc):
            return False
        for i in range(len(dicc_pred)):
            if len(dicc_pred[i]) != len(dicc_pred_acc[i]):
                return False
        for i in range(len(dicc_pred)):
            temp = [x.declaration.name for x in dicc_pred[i]]
            for pred in dicc_pred_acc[i]:
                if not(pred.declaration.name in temp):
                    return False
                else:
                    temp.remove(pred.declaration.name)
            if len(temp) != 0:
                return False

        for a in action.preconditions:
            pos = 0
            for v in a.variables:
                var = None
                for pred in predicates:
                    if pred.declaration.name == a.declaration.name:
                        var = pred.variables[pos]
                        if v.name not in aux:
                            aux[v.name] = var.value.name
                        else:
                            if pred.variables[pos].value.name != aux[v.name]:
                                return False
                pos += 1
        return True

    def write_actions(self, path):
        """Write the actions it takes to reach this planner in a given text file.
        :param path: Path to write.
        """
        f = open(path, 'w')
        f.write(self.obtain_actions())
        f.close()
