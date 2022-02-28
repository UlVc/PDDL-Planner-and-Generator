class Problem:
    """Representation of a problem."""
    def __init__(self, name, domain, objects, predicates, goal):
        """
        :param name: Name of the problem.
        :param domain: Domain in which the problem will be defined.
        :param objects: Types of the domain.
        :param predicates: List of predicates indicating that they are true. Anything else is considered to be false.
        :param goal: List of predicates. It indicates the predicates that need to be true at the end.
        """
        self.name = name
        self.domain = domain
        d_objects = {}

        for object in objects:
            if object.type not in d_objects:
                d_objects[object.type] = [object]
            else:
                d_objects[object.type].append(object)

        self.d_objects = d_objects
        self.state = predicates
        self.goal = goal

    def __str__(self):
        dic = {'name':          self.name,
               'domain_name':   self.domain.name,
               'objects':       "\n      ".join(" ".join(o.name for o in self.d_objects[type]) + " - " + type for type in self.d_objects),
               'init':          "\n      ".join(str(p) for p in self.state),
               'goal':          "\n      ".join(str(p) for p in self.goal)}

        if len(self.goal) >= 2:
            dic['goal'] = "(and " + dic['goal'] + ")"

        return """(define (problem {name}
    (:domain {domain_name})
    (:objects
      {objects})
    (:init
      {init})
    (:goal
      {goal})
)
""".format(**dic)
