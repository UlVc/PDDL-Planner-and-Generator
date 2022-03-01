from domain import Domain
from predicate import Fact, Not, Object
from action import Action
from planner import Planner
from problem import Problem
from bfs import BFS
from variable import Variable

def load():
    """Makes the domain and the problem and returns both."""
    # Variables
    container = Variable('?c', 'container')
    containter_2 = Variable('?otro', 'container')
    arm = Variable('?k', 'arm')
    stack = Variable('?p', 'stack')

    # Predicates
    predicates = [Fact('holding', [arm, container]),
                    Fact('free', [arm]),
                    Fact('on', [container, stack]),
                    Fact('at_the_top', [container, stack]),
                    Fact('on_top', [Variable('?k1', 'container'), Variable('?k2', 'container')])]

    # -----[ Pick up Action ]-----

    # Preconditions
    preconditions_pup = [predicates[1](arm), predicates[2](container, stack),
                            predicates[3](container, stack), predicates[4](container, containter_2)]

    # Effects
    effects_pup = [predicates[0](arm, container), predicates[3](containter_2, stack),
                        Not(predicates[2](container, stack)), Not(predicates[3](container, stack)),
                        Not(predicates[4](container, containter_2)), Not(predicates[1](arm))]

    action_pup = Action('pick-up', [arm, container, stack], [containter_2],
                            preconditions_pup, effects_pup)

    # -----[ Put down Action ]-----

    # Preconditions
    preconditions_pd = [predicates[0](arm, container), predicates[3](containter_2, stack)]

    # Effects
    effects_pd = [predicates[2](container, stack), predicates[3](container, stack),
                    predicates[4](container, containter_2), Not(predicates[3](containter_2, stack)),
                    Not(predicates[0](arm, container)), predicates[1](arm)]

    action_pd = Action('put-down', [arm, container, stack], [containter_2],
                            preconditions_pd, effects_pd)

    # ------ Defining the domain ------

    domain = Domain('platform-worker-robot',
                    ['container', 'stack', 'arm'],
                    predicates,
                    [action_pup, action_pd])

    # ------ Defining the problem ------

    # Objetos
    ca = Object('ca', 'container')
    cb = Object('cb', 'container')
    cc = Object('cc', 'container')
    cd = Object('cd', 'container')
    ce = Object('ce', 'container')
    cf = Object('cf', 'container')
    pallet = Object('pallet', 'container')
    k1 = Object('k1', 'arm')
    k2 = Object('k2', 'arm')
    p1 = Object('p1', 'stack')
    p2 = Object('p2', 'stack')
    q1 = Object('q1', 'stack')
    q2 = Object('q2', 'stack')

    objects = [ca, cb, cc, cd, ce, cf, pallet,
                k1, k2,
                p1, q1, p2, q2]

    # Predicates
    initial_state = [predicates[2](ca, p1), predicates[2](cb, p1), predicates[2](cc, p1),
                        predicates[2](cd, q1), predicates[2](ce, q1), predicates[2](cf, q1),
                        predicates[4](ca, pallet), predicates[4](cb, ca), predicates[4](cc, cb),
                        predicates[4](cd, pallet), predicates[4](ce, cd), predicates[4](cf, ce),
                        predicates[3](cc, p1), predicates[3](cf, q1), predicates[3](pallet, p2), predicates[3](pallet, q2),
                        predicates[1](k1), predicates[1](k2)]

    #goal = [predicates[2](ca, p2), predicates[2](cb, q2), predicates[2](cc, p2),
    #                    predicates[2](cd, q2), predicates[2](ce, q2), predicates[2](cf, q2)]

    goal = [predicates[2](cf, p2), predicates[2](ce, q2)]

    # Definición del problema
    problem = Problem('dwrpb1', domain, objects, initial_state, goal)

    return domain, problem

def main():
    domain, problem = load()

    txt = open('./domain.txt', 'w')
    txt.write(str(domain))
    txt.close()
    txt = open('./problem.txt', 'w')
    txt.write(str(problem))
    txt.close()

    # Definición del planificador
    planner = Planner(domain, problem)

    print('\nSegunda parte: Búsqueda por amplitud\n')
    # Ejecutamos una búsqueda por amplitud pero usando una meta más ligera.
    bfs = BFS(planner)
    p = bfs.busqueda_por_amplitud()
    # Guardamos las acciones a aplicar para llegar al problema obtuvido.
    p.write_actions('./actions.txt')

if __name__ == '__main__':
    main()
