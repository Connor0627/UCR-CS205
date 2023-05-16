from copy import deepcopy
import time
import matplotlib.pyplot as plt

history = []


class Node:
    width = 0
    length = 0

    def __init__(self, puzzle, gn, hn):
        self.puzzle = puzzle
        self.gn = gn
        self.hn = hn
        self.goal = []
        i, j, num = 0, 0, 1
        self.width = len(self.puzzle)
        self.length = len(self.puzzle[0])
        for i in range(self.width):
            line = []
            for j in range(self.length):
                line.append(num)
                num += 1
            self.goal.append(line)
        self.goal[i][j] = 0

    def get_fn(self):
        return self.gn + self.hn

    def get_blank(self):
        for i in range(self.width):
            for j in range(self.length):
                if self.puzzle[i][j] == 0:
                    return i, j

    def print_puzzle(self):
        for i in range(self.width):
            print(self.puzzle[i])
        print("\n")

    def is_goal(self):
        if self.puzzle == self.goal:
            return True
        return False


def expand(node):
    kids = []
    move = [-1, 1, -1, 1]
    for i in range(0, 4):
        kid = deepcopy(node)
        kid.gn += 1
        x, y = node.get_blank()
        if i < 2:
            new_x = x + move[i]
            new_y = y
        else:
            new_x = x
            new_y = y + move[i]
        if 0 <= new_x < node.width and 0 <= new_y < node.length:
            temp = kid.puzzle[x][y]
            kid.puzzle[x][y] = kid.puzzle[new_x][new_y]
            kid.puzzle[new_x][new_y] = temp
            kids.append(kid)
    return kids


def general_search(problem, queueing_function):  # function general-search(problem, QUEUEING-FUNCTION)
    nodes = [Node(problem, 0, 0)]  # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    history.append(problem)
    start_time = time.time()
    count = 0
    while True:  # loop do
        if len(nodes) == 0:  # if EMPTY(nodes) then return "failure"
            return False
        nodes.sort(reverse=True, key=my_compare)
        node = nodes.pop()  # node = REMOVE-FRONT(nodes)
        node.print_puzzle()
        count += 1
        print("current depth = " + str(node.gn) + '\n')
        if node.is_goal():  # if problem.GOAL-TEST(node.STATE) succeeds then return node
            end_time = time.time()
            return node, end_time - start_time, count
        nodes = queueing_function(nodes, expand(node))  # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node,
        # problem.OPERATORS))


def my_compare(node):
    return node.get_fn()


def uniformCostSearch(nodes, expand_nodes):
    for i in expand_nodes:
        i.hn = 0
        if i.puzzle not in history:
            index = expand_nodes.index(i)
            nodes.insert(index, i)
            history.append(i.puzzle)
    return nodes


def misplacedTileHeuristic(nodes, expand_nodes):
    for node in expand_nodes:
        if node.puzzle in history:
            continue
        node.hn = 0
        for i in range(node.width):
            for j in range(node.length):
                if node.puzzle[i][j] != 0 and node.puzzle[i][j] != node.goal[i][j]:
                    node.hn = node.hn + 1
        nodes.append(node)
        history.append(node.puzzle)
    return nodes


def manhattanDistanceHeuristic(nodes, expand_nodes):
    for node in expand_nodes:
        if node.puzzle in history:
            continue
        node.hn = 0
        for i in range(node.width):
            for j in range(node.length):
                if node.puzzle[i][j] == 0:
                    continue
                goal_i, goal_j = divmod(node.puzzle[i][j] - 1, node.width)
                node.hn += abs(goal_i - i) + abs(goal_j - j)
        nodes.append(node)
        history.append(node.puzzle)
    return nodes


def plot_runtimes():
    uniform_times = [0.000010967, 0.000512123, 0.001635074, 0.01843476, 0.3876869, 8.23961305]
    misplaced_times = [0.000000810623, 0.0001778602, 0.00029706, 0.00107598, 0.0078821, 0.0771467, 0.5133092, 20.94980]
    manhattan_times = [0.000000715256, 0.00017261505, 0.000356912, 0.000593185, 0.00188493728, 0.00835514, 0.0350348,
                       1.09268999]
    uniform_count = [1, 4, 23, 209, 1763, 9462]
    misplaced_count = [1, 3, 5, 16, 103, 615, 2049, 15012]
    manhattan_count = [1, 3, 5, 9, 27, 103, 339, 3220]
    depth1 = ['0', '2', '4', '8', '12', '16']
    depth2 = ['0', '2', '4', '8', '12', '16', '20', '24']

    plt.plot(depth1, uniform_times, label="Uniform Cost Search")
    plt.plot(depth2, misplaced_times, label="Misplaced Tile Heuristic")
    plt.plot(depth2, manhattan_times, label="Manhattan Distance Heuristic")
    plt.xlabel("Depth")
    plt.ylabel("Runtime (s)")
    plt.title("Runtime Comparison of Search Algorithms")
    plt.legend()
    plt.show()

    plt.plot(depth1, uniform_count, label="Uniform Cost Search")
    plt.plot(depth2, misplaced_count, label="Misplaced Tile Heuristic")
    plt.plot(depth2, manhattan_count, label="Manhattan Distance Heuristic")
    plt.xlabel("Depth")
    plt.ylabel("Count of Visited Nodes")
    plt.title("Count Comparison of Search Algorithms")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    pp = [[1, 2, 3, 4], [5, 10, 6, 8], [9, 0, 7, 12], [13, 14, 11, 15]]
    p0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Depth 0
    p2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]  # Depth 2
    p4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]  # Depth 4
    p8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]  # Depth 8
    p12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]  # Depth 12
    p16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]  # Depth 16
    p20 = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]  # Depth 20
    p24 = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]  # Depth 24
    p = []
    width = input("Enter the width of puzzle(e.g. type \"3 for a 3*n puzzle): ")
    for i in range(0, int(width)):
        p.append([int(s) for s in input("input the row " + str(i + 1) + ": ").split()])

    # p = pp

    print("result of uniformCostSearch:")
    uniform_search_result, uniform_search_time, uniform_search_count = general_search(p, uniformCostSearch)
    print("uniform_search_time: " + str(uniform_search_time))
    print("uniform_search_count: " + str(uniform_search_count))

    history.clear()
    print("\n\n----------------------------")
    print("result of misplacedTileHeuristic:")
    misplaced_search_result, misplaced_search_time, misplaced_search_count = general_search(p,
                                                                                            misplacedTileHeuristic)
    print("misplaced_search_time: " + str(misplaced_search_time))
    print("misplaced_search_count: " + str(misplaced_search_count))

    history.clear()
    print("\n\n----------------------------")
    print("result of manhattanDistanceHeuristic:")
    manhattan_search_result, manhattan_search_time, manhattan_search_count = general_search(p,
                                                                                            manhattanDistanceHeuristic)
    print("manhattan_search_time: " + str(manhattan_search_time))
    print("manhattan_search_count: " + str(manhattan_search_count))
    plot_runtimes()
