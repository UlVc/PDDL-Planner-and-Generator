from strips import Dominio, Objeto, Variable, Predicado, DeclaracionDePredicado, No, Acción, Problema, Planner, BFS

# Variables
contenedor = Variable('?c', 'contenedor')
otro_contenedor = Variable('?otro', 'contenedor')
grua = Variable('?k', 'grúa')
pila = Variable('?p', 'pila')

# Predicados
predicados = [DeclaracionDePredicado('sostiene', [grua, contenedor]),
                DeclaracionDePredicado('libre', [grua]),
                DeclaracionDePredicado('en', [contenedor, pila]),
                DeclaracionDePredicado('hasta_arriba', [contenedor, pila]),
                DeclaracionDePredicado('sobre', [Variable('?k1', 'contenedor'), Variable('?k2', 'contenedor')])]

# -----[Acción toma]-----

# Precondiciones
precondiciones_toma = [predicados[1](grua), predicados[2](contenedor, pila),
                        predicados[3](contenedor, pila), predicados[4](contenedor, otro_contenedor)]

# Efectos
efectos_toma = [predicados[0](grua, contenedor), predicados[3](otro_contenedor, pila),
                    No(predicados[2](contenedor, pila)), No(predicados[3](contenedor, pila)),
                    No(predicados[4](contenedor, otro_contenedor)), No(predicados[1](grua))]

accion_toma = Acción('toma', [grua, contenedor, pila], [otro_contenedor],
                        precondiciones_toma, efectos_toma)

# -----[Acción pon]-----

# Precondiciones
precondiciones_pon = [predicados[0](grua, contenedor), predicados[3](otro_contenedor, pila)]

# Efectos
efectos_pon = [predicados[2](contenedor, pila), predicados[3](contenedor, pila),
                predicados[4](contenedor, otro_contenedor), No(predicados[3](otro_contenedor, pila)),
                No(predicados[0](grua, contenedor)), predicados[1](grua)]

accion_pon = Acción('pon', [grua, contenedor, pila], [otro_contenedor],
                        precondiciones_pon, efectos_pon)

# ------ Dominio ------

dominio = Dominio('platform-worker-robot',
['contenedor', 'pila', 'grúa'],
predicados,
[accion_toma, accion_pon])

# ------ Problema ------

# Objetos
ca = Objeto('ca', 'contenedor')
cb = Objeto('cb', 'contenedor')
cc = Objeto('cc', 'contenedor')
cd = Objeto('cd', 'contenedor')
ce = Objeto('ce', 'contenedor')
cf = Objeto('cf', 'contenedor')
pallet = Objeto('pallet', 'contenedor')
k1 = Objeto('k1', 'grúa')
k2 = Objeto('k2', 'grúa')
p1 = Objeto('p1', 'pila')
p2 = Objeto('p2', 'pila')
q1 = Objeto('q1', 'pila')
q2 = Objeto('q2', 'pila')

objetos = [ca, cb, cc, cd, ce, cf, pallet,
k1, k2,
p1, q1, p2, q2]

# Predicados
predicados_init = [predicados[2](ca, p1), predicados[2](cb, p1), predicados[2](cc, p1),
                    predicados[2](cd, q1), predicados[2](ce, q1), predicados[2](cf, q1),
                    predicados[4](ca, pallet), predicados[4](cb, ca), predicados[4](cc, cb),
                    predicados[4](cd, pallet), predicados[4](ce, cd), predicados[4](cf, ce),
                    predicados[3](cc, p1), predicados[3](cf, q1), predicados[3](pallet, p2), predicados[3](pallet, q2),
                    predicados[1](k1), predicados[1](k2)]

predicados_meta = [predicados[2](ca, p2), predicados[2](cb, q2), predicados[2](cc, p2),
                    predicados[2](cd, q2), predicados[2](ce, q2), predicados[2](cf, q2)]

predicados_meta_ligero = [predicados[2](cf, p2), predicados[2](ce, q2)]

# Definición del problema
problema = Problema('dwrpb1', dominio, objetos, predicados_init, predicados_meta)

# Guardamos el dominio y el problema en un archivo de texto para fácilidad de manejo
txt = open('./dominio.txt', 'w')
txt.write(str(dominio))
txt.close()
txt = open('./problema.txt', 'w')
txt.write(str(problema))
txt.close()

print('Dominio:')
print(dominio)
print('Problema:')
print(problema)

# Definición del planificador
planner = Planner(dominio, problema)

# Vemos qué acciones son aplicables en el estado actual.
planes = planner.acciones_aplicables()

print('Posibles acciones a ejecutar con sus predicados a usar respectivos:')
for d in planes:
     print(d.nombre)
     for x in planes[d]:
         print([str(c) for c in x])

# ----[Segunda parte del proyecto]----

# Usaremos una meta más ligera por motivos de complejidad. Nada más nos interesa mover el bloque cf a la pila p2 y el bloque ce a la pila q2.
predicados_meta_ligero = [predicados[2](cf, p2), predicados[2](ce, q2)]

# Definición del problema
problema = Problema('dwrpb1', dominio, objetos, predicados_init, predicados_meta_ligero)
planner = Planner(dominio, problema)

print('\nSegunda parte: Búsqueda por amplitud\n')
# Ejecutamos una búsqueda por amplitud pero usando una meta más ligera.
bfs = BFS(planner)
p = bfs.busqueda_por_amplitud() # Plan obtenido tras ejecutar BFS.
# Imprimimos el problema obtenido. Este tiene en su estado los predicados que corresponden a la meta.
print('\nProblema obtenido:\n')
print(p.problema)
# Guardamos las acciones a aplicar para llegar al problema obtuvido.
p.escribir_acciones('./acciones.txt')
