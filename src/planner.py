import itertools

from predicado import No, Predicado
from copy import deepcopy

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
        nuevo_planner = Planner(self.dominio, deepcopy(self.problema)) # Nuevo planner que contendrá los efectos de la acción dada.
        nuevos_predicados = deepcopy(accion.efectos)

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
