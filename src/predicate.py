from copy import deepcopy
from variable import Variable

class Formula:
    """Generalized formula."""
    pass

class Fact:
    """Representation of a fact."""
    def __init__(self, name, variables):
        """
        :param name: Name of the predicate.
        :param variables: List of the typed variables.
        """
        self.name = name
        self.variables = variables

    def __str__(self):
        return '({0} {1})'.format(self.name, ' '.join(str(v) for v in self.variables))

    def _verifica_tipos(self, variables):
        """Check if the variables given have the same type, in the same order, as this predicate."""
        for dec, var in zip(self.variables, variables):
            if (dec.type != var.type):
                raise Exception(f'The types of {dec} y {var} are not te same!')

    def __call__(self, *args):
        """Creates a predicate with the indicated variables or values ​​and verifies that 
        they are of the same type corresponding to this statement.

        When used inside an action, the variables must be the same instances for all
        predicates within the same action.
        :param args: Variables or values for the predicate.
        """
        variables = []
        for var, arg in zip(self.variables, args):
            if isinstance(arg, Object):
                temp_v = deepcopy(var)
                temp_v.value = arg
                variables.append(temp_v)
            elif isinstance(arg, Variable):
                variables.append(arg)
            else:
                raise Exception('Check the types of the variables!')

        return Predicate(self, variables)

class Object:
    """Representation of an object."""
    def __init__(self, name, type):
        """
        :param name: Symbol of the object.
        :param type: Type of the object.
        """
        self.name = name
        self.type = type

    def __str__(self):
        return f'{self.name} - {self.type}'

class Predicate(Formula):
    """Representation of a predicate."""
    def __init__(self, declaration, variables):
        """
        :param declaration: Types of the variables.
        :param variables: List of variables.
        """
        self.declaration = declaration
        self.variables = variables

    def __str__(self):
        return '({0} {1})'.format(self.declaration.name, 
                                    ' '.join(v.value.name if v.value else v.name for v in self.variables))

    def __eq__(self, predicate):
        if type(predicate) is Not:
            return False
        if self.declaration.name == predicate.declaration.name:
            if len(self.variables) == len(predicate.variables):
                for i in range(len(self.variables)):
                    if self.variables[i] != predicate.variables[i]:
                        return False
            return True
        return False

class Not(Formula):
    """Negation of a predicate."""
    def __init__(self, predicate):
        super().__init__()
        self.predicate = predicate
        self.variables = self.predicate.variables
        self.declaration = self.predicate.declaration

    def __str__(self):
        return f'(not {str(self.predicate)})'

    def __eq__(self, predicate):
        if type(predicate) is Not:
            return self.predicate == predicate.predicate

        return self.predicate == predicate
