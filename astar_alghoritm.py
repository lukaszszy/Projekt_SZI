import heapq

class PriorityQueue:
    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item):
        return (self.f(item), item) in self.heap

    def __getitem__(self, key):
        for _, item in self.heap:
            if item == key:
                return item

    def __delitem__(self, key):
        self.heap.remove((self.f(key), key))
        heapq.heapify(self.heap)

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_node = problem.result(self.state, action)
        return Node(next_node, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_node))

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

def best_first_graph_search(problem, f):

    "Zbior wezlow już uwzględnionych"
    closedSet = set()

    "Zbior wezlow jeszcze nie uwzglednioncyh. Na poczatku jeden."
    current = Node(problem.initial)
    openSet = PriorityQueue(f)
	
    if problem.goal_test(current.state):
        return current
    if problem.goal in problem.walls.wallsAll:
        return None
    openSet.append(current)

    "Dopoki openSet nie jest pusty."
    while openSet:

        "Usuń węzel z openSet."
        current = openSet.pop()

        "Jezeli jestestesmy w punkcie docelowym."
        if problem.goal_test(current.state):
            return current

        "Dodaj wezeł do closedSet."
        closedSet.add(current.state)    

        "Dla każdego sąsiada obecnego węzłą."
        for child in current.expand(problem):

            "Sprawdzamy nowy węzeł"
            "w przeciwnym razie gnorujemy sąsiada ponieważ jest on już uwzględniony."
            if child.state not in closedSet and child not in openSet:
                "Dodajemy nowy węzeł do openSet."
                openSet.append(child)    
            elif child in openSet:
                
                "Obliczamy odleglosc obecengo położenia od sąsiada."
                current_path = openSet[child]
                
                tentative_score = f(current_path)
                score = f(child)
                
                "Jezeli znalezliśmy lepszą ścieżkę."
                if tentative_score >= score:
                    "Usuwamy obecną ścieżkę z openSet."
                    del openSet[current_path]
                    "Dodajemy nowy węzeł do openSet."
                    openSet.append(child)
                    
    return None

def astar_search(problem):
    h = problem.h
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

class PlanRoute():
    def __init__(self, initial, goal, walls, dimrow):
        self.initial = initial
        self.goal = goal
        self.walls = walls
        self.dimrow = dimrow

    def actions(self, state):
        """Zbior wszystkich akcji. """
        possible_actions = ['Prosto', 'SkretLewo', 'SkretPrawo']
        """Aktualne położenie agenta."""

        x = state[0]
        y = state[1]
        dir = state[2]

        if x == 0 and dir == 'W':
            if 'Prosto' in possible_actions:
                possible_actions.remove('Prosto')
        if y == 0 and dir == 'N':
            if 'Prosto' in possible_actions:
                possible_actions.remove('Prosto')
        if x == (self.dimrow - 1) and dir == 'E':
            if 'Prosto' in possible_actions:
                possible_actions.remove('Prosto')
        if y == (self.dimrow - 1) and dir == 'S':
            if 'Prosto' in possible_actions:
                possible_actions.remove('Prosto')

        return possible_actions

    def result(self, state, action):
        """ Dla danego stanu i akcji zwracany jest nowy stan, który jest wynikiem danej akcji. """
        x = state[0]
        y = state[1]
        dir = state[2]
        proposed_loc = [x, y]

        # Ruchy agenta
        if action == 'Prosto':
            if dir == 'N':
                proposed_loc = [x, y - 1]
            elif dir == 'S':
                proposed_loc = [x, y + 1]
            elif dir == 'W':
                proposed_loc = [x - 1, y]
            elif dir == 'E':
                proposed_loc = [x + 1, y]
            else:
                raise Exception('InvalidAction')

        elif action == 'SkretLewo':
            if dir == 'N':
                dir = 'W'
            elif dir == 'S':
                dir = 'E'
            elif dir == 'E':
                dir = 'N'
            elif dir == 'W':
                dir = 'S'
            else:
                raise Exception('InvalidAction')

        elif action == 'SkretPrawo':
            if dir == 'N':
                dir = 'E'
            elif dir == 'S':
                dir = 'W'
            elif dir == 'E':
                dir = 'S'
            elif dir == 'W':
                dir = 'N'
            else:
                raise Exception('InvalidAction')

        if (proposed_loc[0], proposed_loc[1]) not in self.walls.wallsAll:
            state = (proposed_loc[0], proposed_loc[1], dir)

        return state

    def goal_test(self, state):
        "Punkt docelowy"
        return (state[0] == self.goal[0]) and (state[1] == self.goal[1])

    def path_cost(self, c, state1, action, state2):
        return c + 1


    def h(self, node):
        """Funkcja heurystyczna """
        x1 = node.state[0]
        y1 = node.state[1]
        x2 = self.goal[0]
        y2 = self.goal[1]
        return abs(x2 - x1) + abs(y2 - y1)