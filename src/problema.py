class Problema:
    """ Definicion de un problema en un dominio particular. """
    def __init__(self, nombre, dominio, objetos, predicados, predicados_meta):
        """
        Problema de planeación en una instancia del dominio.
        :param nombre: nombre del problema
        :param dominio: referencia al objeto con la descripción genérica del dominio
        :param objetos: lista de objetos existentes en el dominio, con sus tipos
        :param predicados: lista de predicados con sus variables aterrizadas, indicando qué cosas son verdaderas en el
               estado inicial.  Todo aquello que no esté listado es falso.
        :param predicados_meta: lista de predicados con sus variables aterrizadas, indicando aquellas cosas que deben
               ser verdaderas al final.  Para indicar que algo debe ser falso, el predicado debe ser negativo.
        """
        self.nombre = nombre
        self.dominio = dominio # ref a objeto Dominio
        d_objetos = {}
        for objeto in objetos:
            if objeto.tipo not in d_objetos:
                d_objetos[objeto.tipo] = [objeto]
            else:
                d_objetos[objeto.tipo].append(objeto)
        self.d_objetos = d_objetos
        self.estado = predicados
        self.meta = predicados_meta

    def __str__(self):
        dic = {'name':          self.nombre,
               'domain_name':   self.dominio.nombre,
               'objects':       "\n      ".join(" ".join(o.nombre for o in self.d_objetos[tipo]) + " - " + tipo for tipo in self.d_objetos),
               'init':          "\n      ".join(str(p) for p in self.estado),
               'goal':          "\n      ".join(str(p) for p in self.meta)}
        if len(self.meta) >= 2:
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
