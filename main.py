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
            history.append(node.puzzle)
            kids.append(kid)
    return kids


def general_search(problem, queueing_function):  # function general-search(problem, QUEUEING-FUNCTION)
    nodes = [Node(problem, 0, 0)]  # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    while True:  # loop do
        if len(nodes) == 0:  # if EMPTY(nodes) then return "failure"
            return False
        nodes.sort(reverse=True, key=my_compare)
        node = nodes.pop()  # node = REMOVE-FRONT(nodes)
        node.print_puzzle()
        print("current depth = " + str(node.gn) + '\n')
        if node.is_goal():  # if problem.GOAL-TEST(node.STATE) succeeds then return node
            return node
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


if __name__ == "__main__":
    # p = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
    # p = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]
    p = []
    width = input("Enter the width of puzzle(e.g. type \"3 for a 3*n puzzle): ")
    for i in range(0, int(width)):
        p.append([int(s) for s in input("input the row " + str(i + 1) + ": ").split()])
    print(p)
    print("result of uniformCostSearch:")
    general_search(p, uniformCostSearch)
    print("\n\n----------------------------")
    print("result of misplacedTileHeuristic:")
    history.clear()
    general_search(p, misplacedTileHeuristic)
    print("\n\n----------------------------")
    print("result of manhattanDistanceHeuristic:")
    history.clear()
    general_search(p, manhattanDistanceHeuristic)