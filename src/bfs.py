class BFS:
    """Implementation of BFS for the planner."""
    def __init__(self, planner):
        self.planner = planner

    def busqueda_por_amplitud(self):
        """Executes BFS on the planner.
           It returns the planner with the problem already on the goal. Otherwise it will return -1."""
        queue = []
        queue.append(self.planner)
        self.planner.explorado = True
        previous_level = -1

        while len(queue) != 0:
            v = queue.pop(0)

            if previous_level != v.level:
                print('Level of exploration:', v.level)
                previous_level = v.level

            if v.is_goal():
                return v

            actions = v.applicable_actions()

            for a in actions:
                for pred in actions[a]:
                    p = v.apply_action(a, pred)
                    if not(p.explored):
                        p.explored = True
                        queue.append(p)

        return -1
