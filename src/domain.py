def _lista_a_dict(l):
    """ Pone a todos los elementos de la lista en un diccionario cuya
    llave es el nombre del objeto.
    Sólo sirve para listas de objetos con atributo 'nombre'.
    """
    d = {}
    for o in l:
        d[o.name] = o
    return d

class Domain:
    """ Clase para definir el dominio, o espacio de estados en el cual se plantearán problemas de planeación. """
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
        self._predicados = _lista_a_dict(predicates)

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

    def declaración(self, nombre):
        """ 
        Devuelve la declaración del predicado con el nombre indicado.
        """
        return self._predicados[nombre]
