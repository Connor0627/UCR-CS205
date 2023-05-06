class Node:
    def __init__(self, puzzle, g, h):
        self.puzzle = puzzle
        self.g = g
        self.h = h


def general_search(problem, queueing_function):
    nodes = [Node(problem, 0, 0)]  # nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    while True:
        if len(nodes) == 0:
            return False
        node = nodes.pop();
        if is_goal(node.puzzle):
            return node
        # nodes = queueing_function(nodes, expand(node))


# check if the current puzzle is goal puzzle
def is_goal(puzzle):
    num = 1;
    i = 0
    j = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] == num:
                num += 1
            else:
                break
    if num == len(puzzle) * len(puzzle[0]) and puzzle[i][j] == 0:
        return True
    return False


def print_puzzle(puzzle):
    for i in range(len(puzzle)):
        print(puzzle[i])
    print("\n")


if __name__ == "__main__":
    p = [[3, 1, 2], [4, 5, 6], [7, 8, 0]]
    res = general_search(p, "print()")
    if not res:
        print("failll")
    else:
        print_puzzle(res.puzzle)
