# ------ Auxiliares -----

import copy
import itertools
def clona(obj):
    """ Atajo para crear copias de objetos recursivamente. """
    return copy.deepcopy(obj)

def _lista_a_dict(l):
    """ Pone a todos los elementos de la lista en un diccionario cuya
    llave es el nombre del objeto.
    Sólo sirve para listas de objetos con atributo 'nombre'.
    """
    d = {}
    for o in l:
        d[o.nombre] = o
    return d

# ------ Dominio -----

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


class Variable:
    """ Variable tipada. """
    def __init__(self, nombre, tipo, valor=None):
        """
        :param nombre: símbolo nombre de esta variable.  Los nombres de variables inician con ?
        :param tipo: tipo de la variable, debe estar registrado en la descripción del dominio
        :param valor: objeto vinculado a esta variable, si es None la variable está libre
        """
        self.nombre = nombre
        self.tipo = tipo
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor_nuevo):
        """
        Permite asignar None o un valor de tipo de esta variable.
        """
        if valor_nuevo and valor_nuevo.tipo != self.tipo:
            raise Exception(f"{valor_nuevo} no es de tipo {self.tipo}")
        self._valor = valor_nuevo

    @valor.deleter
    def valor(self):
        self._valor = None

    def __str__(self):
        if self.valor:
            return self.valor.nombre
        return "{} - {}".format(self.nombre, self.tipo)
    
    def __eq__(self, variable):
        if self.tipo == variable.tipo:
            if self.valor:
                return self.valor.nombre == variable.valor.nombre
            return self.nombre == variable.nombre
        return False
        
        
class Formula:
    """
    Predicado o fórmula generada.
    """
    pass


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
                temp_v = clona(var)
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


# ------ Problema -----

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

class Planner:
    """
    Genera un plan para un problema dado.
    """
    def __init__(self, dominio, problema):
        """
        :param dominio: dominio del mundo.
        :param problema: problema a resolver.
        """
        self.dominio = dominio
        self.problema = problema
        self.explorado = False
        self.accion_tomada = None # Acción que se tomó para llegar a este plan. Es un diccionario de la forma (accion, predicados).
        self.padre = None # Padre de este planer. Aplicando la accion tomada almacenada en la variable accion_tomada con el padre se llega a este planner.
        self.nivel = 0 # Nivel a partir donde se generó el problema de este planner en el algoritmo de BFS. La raíz tiene nivel 0.

    def acciones_aplicables(self):
        """Regresa todas las acciones que se pueden aplicar al problema de este planner."""
        return {accion : self.accion_aplicable(accion) for accion in self.dominio.acciones}

    def accion_aplicable(self, accion):
        """
        Verifica si una acción es aplicable o no.
        :param accion: acción a verificar si es aplicable.
        """
        objetos_a_usar = [] # Lista que contiene los posibles predicados a usar para la acción dada.
    
        # Obtenemos los posibles predicados.
        for subset in itertools.combinations(self.problema.estado, len(accion.precondiciones)):
            if self.comprobar_accion(accion, subset):
                objetos_a_usar.append(subset)

        return objetos_a_usar

    def aplicar_accion(self, accion, predicados):
        """
        Aplica una acción al problema actual usando los predicados dados. 
        Se asume que la acción dada es aplicable.
        :param accion: acción a aplicar.
        :param predicados: predicados a usar con la acción.
        """
        dicc = {} # Diccionario que mapea los nombres de las variables de las precondiciones de la acción con los nombres de los predicados dados.
        nuevo_planner = Planner(self.dominio, clona(self.problema)) # Nuevo planner que contendrá los efectos de la acción dada.
        nuevos_predicados = clona(accion.efectos)

        # Formamos el diccionario con las variables mapeadas.
        for pred in accion.precondiciones:
            temp = [x for x in predicados if x.declaracion.nombre == pred.declaracion.nombre][0]
            for i in range(len(pred.variables)):
                dicc[pred.variables[i].nombre] = temp.variables[i]

        # Formamos los nuevos predicados usando los efectos de la acción.
        for e in nuevos_predicados:
            if type(e) is No:
                variables = e.predicado.variables
            else:
                variables = e.variables

            for i in range(len(variables)):
                variables[i] = dicc[variables[i].nombre]

        #print(accion.nombre, [str(x) for x in predicados])
        # Eliminamos las precondiciones de la acción del nuevo planner.
        for p in predicados:
            nuevo_planner.problema.estado.remove(p)

        # Agregamos los predicados causados por los efectos de la acción al nuevo planner.
        for p in nuevos_predicados:
            nuevo_planner.problema.estado.append(p)

        nuevo_planner.accion_tomada = (accion, predicados)
        nuevo_planner.padre = self
        nuevo_planner.nivel = self.nivel + 1

        return nuevo_planner

    def comprobar_accion(self, accion, predicados):
        """"
        Verifica que la acción se pueda aplicar usando los predicados dados.
        :param dic: acción.
        :param predicados: lista de predicados a verificar en la acción.
        """
        dicc_pred = {0 : [x for x in predicados if type(x) is No], 
                     1 : [x for x in predicados if type(x) is Predicado]}
        dicc_pred_acc = {0 : [x for x in accion.precondiciones if type(x) is No], 
                         1 : [x for x in accion.precondiciones if type(x) is Predicado]}
        aux = {}

        if len(dicc_pred) != len(dicc_pred_acc):
            return False
        for i in range(len(dicc_pred)):
            if len(dicc_pred[i]) != len(dicc_pred_acc[i]):
                return False
        for i in range(len(dicc_pred)):
            temp = [x.declaracion.nombre for x in dicc_pred[i]]
            for pred in dicc_pred_acc[i]:
                if not(pred.declaracion.nombre in temp):
                    return False
                else:
                    temp.remove(pred.declaracion.nombre)
            if len(temp) != 0:
                return False

        for a in accion.precondiciones:
            pos = 0
            for param in a.variables:
                var = None
                for pred in predicados:
                    if pred.declaracion.nombre == a.declaracion.nombre:
                        var = pred.variables[pos]
                        if param.nombre not in aux:
                            aux[param.nombre] = var.valor.nombre
                        else:
                            if pred.variables[pos].valor.nombre != aux[param.nombre]:
                                return False
                pos += 1
        return True

    def satisiface_meta(self):
        """"
        Verifica que si ya se llegó a la meta o no.
        """
        for predicado in self.problema.meta:
            if not(predicado in self.problema.estado):
                return False

        return True

    def obtener_acciones(self):
        """Regresa, en forma de cadena, las acciones que se hicieron para llegar hasta el problema de este planner."""
        if self.padre == None:
            return 'Acciones a tomar empezando desde arriba:'
        return self.padre.obtener_acciones() + f'\n\n{self.accion_tomada[0].nombre}: {[str(p) for p in self.accion_tomada[1]]}'

    def escribir_acciones(self, path):
        """
        Escribe las acciones que conlleva llegar a este planner en un archivo de texto dado.
        :param path: Lugar a guardar las acciones.
        """
        f = open(path, 'w')
        f.write(self.obtener_acciones())
        f.close()

class BFS:
    """Búsqueda por ampliación en un objeto de tipo Planner."""
    def __init__(self, planner):
        self.planner = planner

    def busqueda_por_amplitud(self):
        """Regresa el planner con el problema llegado a la meta. En caso contrario, regresa -1."""
        cola = []
        cola.append(self.planner)
        self.planner.explorado = True
        i = 0
        nivel_anterior = -1

        while len(cola) != 0:
            v = cola.pop(0)
            if nivel_anterior != v.nivel:
                print('Nivel de exploración:', v.nivel)
                nivel_anterior = v.nivel
            if v.satisiface_meta():
                return v
            acciones = v.acciones_aplicables()

            for a in acciones:
                for pred in acciones[a]:
                    p = v.aplicar_accion(a, pred)
                    if not(p.explorado):
                        p.explorado = True
                        cola.append(p)

        return -1
