from utils import *

class Problem(object):
    
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def path_cost(self, c, state1, action, state2):
        return c + 1


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

    def reconstruct_path(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def best_first_search(problem, f):

    "Zbior wezlow już uwzględnionych"
    closedSet = set()

    "Zbior wezlow jeszcze nie uwzglednioncyh. Na poczatku jeden."
    current = Node(problem.initial)
    openSet = PriorityQueue('min', f)
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
    
    heuristic = problem.heuristic
    function = lambda n: n.path_cost + heuristic(n)

    "Best First Search z funkcją f(n) = g(n)+h(n)."
    return best_first_search(problem, function)


class Plan_Route(Problem):

    def __init__(self, initial, goal, walls):

        Problem.__init__(self, initial, goal)
        self.walls = walls
        
        self.x_size = 30
        self.y_size = 20

    def actions(self, state):

        "Zbior wszystkich akcji."
        actions = ['prawo', 'lewo', 'gora', 'dol']

        "Aktualne położenie agenta."
        x,y = state

        "Zbior wszystkich mozliwych akcji."
        if x == 0:
            if 'lewo' in actions:
                actions.remove('lewo')
        if x == (self.x_size - 1):
            if 'prawo' in actions:
                actions.remove('prawo')
        if y == 0:
            if 'gora' in actions:
                actions.remove('gora')
        if y == (self.y_size - 1):
            if 'dol' in actions:
                actions.remove('dol')

        return actions

    def result(self, state, action):
        x,y = state
        proposed_loc = tuple()

        if action == 'gora':
            proposed_loc = (x, y - 1)
        elif action == 'dol':
            proposed_loc = (x, y + 1)
        elif action == 'lewo':
            proposed_loc = (x - 1, y)
        elif action == 'prawo':
            proposed_loc = (x + 1, y)
        else:
            raise Exception('InvalidAction')

        if proposed_loc not in self.walls:
            state = proposed_loc

        return state


    "Punkt docelowy"
    def goal_test(self, state):
        return state == self.goal


    "Funkcja heurystyczna"
    def heuristic(self, node):
        
        x1,y1 = node.state
        x2,y2 = self.goal

        return abs(x2 - x1) + abs(y2 - y1)
