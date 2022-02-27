class Domain:
    """Representation of the domain."""
    def __init__(self, name, types, predicates, actions):
        """
        :param name: Name of the domain.
        :param types: Types of the domain.
        :param predicates: Predicates of the domain.
        :param actions: Actions of the domain.
        """
        self.name = name
        self.types = types
        self.predicates = predicates
        self.actions = actions

    def __str__(self):
        dic = {'name':          self.name,
               'types':         "\n        ".join(self.types),
               'predicates':    "\n        ".join(str(p) for p in self.predicates),
               'actions':       "\n    ".join(str(a) for a in self.actions)
               }
        return """(define (domain {name})
    (:requirements :strips :typing)
    (:types
        {types}
    )
    (:predicates
        {predicates})
    )
    {actions}
)
""".format(**dic)
