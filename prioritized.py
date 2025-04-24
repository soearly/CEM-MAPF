import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals, time_max=None):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time = 0

        self.time_max = time_max if time_max else float('inf')
        self.num_of_expanded = 0
        self.num_of_generated = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []
        constraints = []

        # # 1.2 testing
        # constraints.append({
        #                     'agent': 0,
        #                     'loc': [(1,5)],
        #                     'timestep': 4,
        #                     'final' : False,
        #                     # 'positive': False,
        #                 })

        # # 1.3 testing
        # constraints.append({
        #                     'agent': 1,
        #                     'loc': [(1,2) , (1,3)],
        #                     'timestep': 1,
        #                     'final' : False,
        #                     'positive': False,
        #                 })

        # # 1.4 testing
        # constraints.append({
        #                     'agent': 0,
        #                     'loc': [(1,5)],
        #                     'timestep': 10,
        #                     'final' : False,
        #                     'positive': False,
        #                 })
        
        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i], i, constraints)
            if timer.time() - start_time >= self.time_max:
                raise BaseException("Time limit exceeded")
            if path is None:
                raise BaseException('No solutions')
            result.append(path)

            ##############################
            # 2: Add constraints here
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches

            ##############################

            for time, loc in enumerate(path):
                # create a new constraint whith the current path location for all agents except the current one
                for x in range(self.num_of_agents):
                    if x != i:
                        # vertex constraint
                        # if this is the last location in the path, we add a final constraint
                        constraints.append({
                            'agent': x,
                            'loc': [loc],
                            'timestep': time,
                            'final': time == len(path) - 1
                        })
                        # edge constraint
                        # the agent can't be at the last position to add an edge constraint
                        if time < len(path) - 1:
                            # next location in path
                            nextloc = path[path.index(loc) + 1]
                            constraints.append({
                                'agent': x,
                                'loc': [nextloc, loc],
                                'timestep': time + 1,
                                'final': False
                            })

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        print(result)
        return result
