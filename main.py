from copy import deepcopy
class Node:
    def __init__(self, puzzle, gn, hn):
        self.puzzle = puzzle
        self.gn = gn
        self.hn = hn
        self.goal = []
        i = 0
        j = 0
        num = 1
        for i in range(len(self.puzzle)):
            line = []
            for j in range(len(self.puzzle[0])):
                line.append(num)
                num += 1
            self.goal.append(line)
        self.goal[i][j] = 0

    def get_fn(self):
        return self.gn + self.hn

    def get_blank(self):
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[0])):
                if self.puzzle[i][j] == 0:
                    return i, j

    def print_puzzle(self):
        for i in range(len(self.puzzle)):
            print(self.puzzle[i])
        print("\n")

    def is_goal(self):
        if self.puzzle == self.goal:
            return True
        return False

def expand(node):
    kidsnode = []
    for i in range(0, 4):
        kid = deepcopy(node)
        kid.gn += 1
        moveBlankTile(node.puzzle, kid.puzzle, i)

def moveBlankTile():
    a
def general_search(problem, queueing_function):
    nodes = [Node(problem, 0, 0)]  # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    while True:
        if len(nodes) == 0:
            return False
        node = nodes.pop();
        if node.is_goal():
            return node
        nodes = queueing_function(nodes, expand(node))
# check if the current puzzle is goal puzzle


if __name__ == "__main__":
    p = [[3, 1, 2], [4, 5, 6], [7, 8, 0]]
    q = [[3, 1, 2], [4, 5, 6], [7, 8, 0]]
    n = Node(p, 0 ,0)
    print(n.goal)
