class Acción:
    """ Función de transición con su acción correspondiente. """
    def __init__(self, nombre, parámetros, variables, precondiciones, efectos):
        """
        Inicializa definición de la función de transición para esta acción.
        :param nombre: nombre de la acción
        :param parámetros: lista de variables tipadas
        :param variables: lista de variables libres que pueden tomar su valor de cualquier objeto del domino siempre que
               sus valores satisfagan las restriciones de las precondiciones.
        :param precondiciones: lista de predicados con variables libres
        :param efectos: lista de predicados con variables libres
        """
        self.nombre = nombre
        self.parámetros = parámetros
        self.vars = variables
        self.precondiciones = precondiciones
        self.efectos = efectos

    def __str__(self):
        dic = {'name':      self.nombre,
               'params':    " ".join(str(p) for p in self.parámetros),   # Podrían reunirse 1o los de tipos iguales
               'prec':      " ".join(str(p) for p in self.precondiciones),
               'efec':      " ".join(str(p) for p in self.efectos)
               }

        if self.vars:
            dic['vars'] = "\n        :vars         ({})".format(" ".join(str(v) for v in self.vars))
        else:
            dic['vars'] = ""

        if len(self.precondiciones) >= 2:
            dic['prec'] = "(and " + dic['prec'] + ")"

        if len(self.efectos) >= 2:
            dic['efec'] = "(and " + dic['efec'] + ")"

        return """(:action {name}
        :parameters   ({params}) {vars}
        :precondition {prec}
        :effect       {efec}
    )""".format(**dic)
