class Action:
    """ Función de transición con su acción correspondiente. """
    def __init__(self, name, parameters, variables, preconditions, effects):
        """
        :param name: Name of the action.
        :param parameters: List of variables.
        :param variables: List of free variables. They can take whatever object of the domain as long as
            their values ​​satisfy the constraints of the preconditions.
        :param preconditions: List of predicates with free variables. The state of the world must have the same
            predicates in order to apply this action.
        :param effects: List of predicates with free variables. It represents the effects that occur after 
            applying this action.
        """
        self.name = name
        self.parameters = parameters
        self.vars = variables
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        dic = {'name':      self.name,
               'params':    ' '.join(str(p) for p in self.parameters),
               'prec':      ' '.join(str(p) for p in self.preconditions),
               'efec':      ' '.join(str(p) for p in self.effects)
               }

        if self.vars:
            dic['vars'] = f'\n        :vars         ({" ".join(str(v) for v in self.vars)})'
        else:
            dic['vars'] = ''

        if len(self.preconditions) >= 2:
            dic['prec'] = '(and ' + dic['prec'] + ')'

        if len(self.effects) >= 2:
            dic['efec'] = '(and ' + dic['efec'] + ')'

        return """(:action {name}
        :parameters   ({params}) {vars}
        :precondition {prec}
        :effect       {efec}
    )""".format(**dic)
