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
