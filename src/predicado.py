from copy import deepcopy
from variable import Variable

class Formula:
    """
    Predicado o fórmula generada.
    """
    pass

class Objeto:
    """ Valor concreto para variables en el dominio. """
    def __init__(self, nombre, tipo):
        """
        Crea un objeto existente en el dominio para este problema.
        :param nombre: Símbolo del objeto
        :param tipo: tipo del objeto
        """
        self.nombre = nombre
        self.tipo = tipo

    def __str__(self):
        return "{} - {}".format(self.nombre, self.tipo)


class Predicado(Formula):
    """ Representa un hecho. """
    def __init__(self, declaracion, variables):
        """
        Predicados para representar hechos.
        :param predicado: declaración con los tipos de las variables.
        :param variables: lista de instancias de variables en la acción donde se usa este predicado.
        :param negativo: indica un predicado del tipo "no P", utilizable para especificar efectos o metas.
        """
        self.declaracion = declaracion
        self.variables = variables

    def __str__(self):
        pred = "({0} {1})".format(self.declaracion.nombre, " ".join(v.valor.nombre if v.valor else v.nombre for v in self.variables))
        return pred

    def __eq__(self, predicado):
        if type(predicado) is No:
            return False
        if self.declaracion.nombre == predicado.declaracion.nombre:
            if len(self.variables) == len(predicado.variables):
                for i in range(len(self.variables)):
                    if self.variables[i] != predicado.variables[i]:
                        return False
            return True
        return False

class DeclaracionDePredicado:
    """ Representa un hecho. """
    def __init__(self, nombre, variables):
        """
        Declaración de predicados para representar hechos.
        :param nombre:
        :param variables: lista de variables tipadas
        """
        self.nombre = nombre
        self.variables = variables

    def __str__(self):
        pred = "({0} {1})".format(self.nombre, " ".join(str(v) for v in self.variables))
        return pred

    def _verifica_tipos(self, variables):
        """
        Las variables en la lista deben tener los mismos tipos, en el mismo orden, que este predicado.
        """
        for dec, var in zip(self.variables, variables):
            if (dec.tipo != var.tipo):
                raise Exception(f"Los tipos de las variables {dec} y {var} no coinciden")

    def __call__(self, *args):
        """
        Crea un predicado con las variables o valores indicados y verifica que sean del tipo
        correspondiente a esta declaración.

        Cuando se usa dentro de una acción las variables deben ser las mismas instancias para todos
        los predicados dentro de la misma acción.
        """
        variables = []
        for var, arg in zip(self.variables, args):
            if isinstance(arg, Objeto):
                # print("instancia ", arg)
                temp_v = deepcopy(var)
                temp_v.valor = arg
                variables.append(temp_v)
            elif isinstance(arg, Variable):
                # print("variable ", arg)
                variables.append(arg)
            else:
                print("Ni lo uno ni lo otro ", arg, " tipo ", type(arg))

        return Predicado(self, variables)


class No(Formula):
    """
    Negación de un predicado.
    """
    def __init__(self, predicado):
        super().__init__()
        self.predicado = predicado
        self.variables = self.predicado.variables
        self.declaracion = self.predicado.declaracion

    def __str__(self):
        return "(not {0})".format(str(self.predicado))

    def __eq__(self, predicado):
        if type(predicado) is No:
            return self.predicado == predicado.predicado

        return self.predicado == predicado
