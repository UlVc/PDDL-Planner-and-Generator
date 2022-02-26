def _lista_a_dict(l):
    """ Pone a todos los elementos de la lista en un diccionario cuya
    llave es el nombre del objeto.
    Sólo sirve para listas de objetos con atributo 'nombre'.
    """
    d = {}
    for o in l:
        d[o.nombre] = o
    return d

class Dominio:
    """ Clase para definir el dominio, o espacio de estados en el cual se plantearán problemas de planeación. """
    def __init__(self, nombre, tipos, predicados, acciones):
        """
        Inicializa un dominio
        :param nombre:
        :param tipos:
        :param predicados:
        :param acciones:
        """
        self.nombre = nombre
        self.tipos = tipos
        self.predicados = predicados
        self.acciones = acciones

        self._predicados = _lista_a_dict(predicados)

    def __str__(self):
        dic = {'name':          self.nombre,
               'types':         "\n        ".join(self.tipos),
               'predicates':    "\n        ".join(str(p) for p in self.predicados),
               'actions':       "\n    ".join(str(a) for a in self.acciones)
               }
        return """
(define (domain {name})
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
